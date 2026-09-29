import os
from functools import lru_cache

import weaviate
from pydantic import BaseModel
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.init import Auth

from config import settings
from pipeline.agent import call_agent
from pipeline.errors import PipelineError
from pipeline.llm import AI_GATEWAY_BASE_URL
from pipeline.models import DEFAULT_MODEL, ModelRef
from pipeline.trace import Trace
from rag.embedding import EMBEDDING_DIM, EMBEDDING_MODEL

# Mem0 would otherwise send usage data to Mem0 and print notices
os.environ.setdefault("MEM0_TELEMETRY", "False")

from mem0 import Memory  # noqa: E402

DASHSCOPE_COMPATIBLE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
# The memories a chat is given, and the ones a new message is compared with
RECALL_LIMIT = 10
COMPARE_LIMIT = 20
# The most memories one message can add, and the longest a memory can be
MAX_NEW_MEMORIES = 5
MAX_MEMORY_LENGTH = 300
# As in mem0/vector_stores/weaviate.py, plus the two a saved memory also has
MEM0_PROPERTIES = [
    *("ids", "hash", "metadata", "data", "created_at", "category", "updated_at", "user_id", "agent_id", "run_id"),
    *("text_lemmatized", "role"),
]


def memory_cluster() -> tuple[str, str]:
    """The Weaviate cluster's URL and API key: the memory cluster when one is set, else the knowledge base's"""
    if settings.memory_weaviate_url:
        return settings.memory_weaviate_url, settings.memory_weaviate_api_key
    return settings.weaviate_url, settings.weaviate_api_key


def connect_memory_cluster() -> weaviate.WeaviateClient:
    url, api_key = memory_cluster()
    return weaviate.connect_to_weaviate_cloud(cluster_url=url, auth_credentials=Auth.api_key(api_key))


def create_collection() -> None:
    """Mem0 creates its collection with an HNSW index, which Weaviate Cloud clusters that only allow hfresh
    refuse. Created here first, the same way as the knowledge base, it gets the cluster's default index,
    and Mem0 uses it as it is. (Mem0's second collection, for entities, is only used with spaCy installed.)"""
    with connect_memory_cluster() as client:
        if client.collections.exists(settings.memory_collection):
            return

        try:
            client.collections.create(
                settings.memory_collection,
                properties=[Property(name=p, data_type=DataType.TEXT) for p in MEM0_PROPERTIES],
                vector_config=Configure.Vectors.self_provided(),
            )
        except Exception as error:
            if "USAGE_LIMIT_EXCEEDED" in str(error):
                raise PipelineError(
                    "The Weaviate cluster has no room for the memories: a free cluster holds one collection, and the "
                    "knowledge base uses it. Set MEMORY_WEAVIATE_URL and MEMORY_WEAVIATE_API_KEY to a second cluster."
                ) from error
            raise


@lru_cache(maxsize=1)
def memory_store() -> Memory:
    """Mem0, keeping each user's memories in Weaviate with the knowledge base's Qwen embeddings.
    Mem0's own LLM is never called: the memory agent decides what to add, update or delete."""
    create_collection()
    url, api_key = memory_cluster()

    return Memory.from_config(
        {
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": EMBEDDING_MODEL,
                    "embedding_dims": EMBEDDING_DIM,
                    "api_key": settings.dashscope_api_key,
                    "openai_base_url": DASHSCOPE_COMPATIBLE_URL,
                },
            },
            "vector_store": {
                "provider": "weaviate",
                "config": {
                    "collection_name": settings.memory_collection,
                    "embedding_model_dims": EMBEDDING_DIM,
                    "cluster_url": url,
                    "auth_client_secret": api_key,
                },
            },
            "llm": {
                "provider": "openai",
                "config": {"model": DEFAULT_MODEL.id, "api_key": settings.ai_gateway_api_key, "openai_base_url": AI_GATEWAY_BASE_URL},
            },
        }
    )


def search_memories(user_id: str, text: str, limit: int) -> list[dict]:
    found = memory_store().search(text, filters={"user_id": user_id}, top_k=limit, threshold=0.0)["results"]
    return [{"id": m["id"], "memory": m["memory"]} for m in found]


def list_memories(user_id: str) -> list[dict]:
    found = memory_store().get_all(filters={"user_id": user_id}, top_k=200)["results"]
    memories = [{key: m.get(key) for key in ("id", "memory", "created_at", "updated_at")} for m in found]
    return sorted(memories, key=lambda m: m["updated_at"] or m["created_at"] or "", reverse=True)


def delete_memory(user_id: str, memory_id: str) -> None:
    memory = memory_store().get(memory_id)

    # Another user's memory is treated as missing
    if not memory or memory.get("user_id") != user_id:
        raise PipelineError("That memory doesn't exist")

    memory_store().delete(memory_id)


def delete_all_memories(user_id: str) -> None:
    memory_store().delete_all(user_id=user_id)


def format_memories(memories: list[dict]) -> str:
    return "\n".join(f"- {m['memory']}" for m in memories)


def recall_memories(user_id: str, question: str, trace: Trace) -> list[dict]:
    """The user's memories closest to the question, for the question, answer and diagram steps."""
    memories = []

    with trace.step("memory search", input=question, fallback=True) as step:
        memories = search_memories(user_id, question, RECALL_LIMIT)
        step["raw_output"] = format_memories(memories)
        count = f"{len(memories)} {'memory' if len(memories) == 1 else 'memories'}"
        step["output"] = f"Used {count}: " + "; ".join(m["memory"] for m in memories) if memories else "No memories saved yet"

    if "error" in step:
        step["output"] = f"Couldn't read the memories, so the answer is written without them: {step['error']}"

    return memories


class MemoryChange(BaseModel):
    number: int
    memory: str


class MemoryReply(BaseModel):
    add: list[str] = []
    update: list[MemoryChange] = []
    delete: list[int] = []


def describe_changes(changes: list[dict]) -> str:
    words = {"saved": "Saved", "updated": "Updated", "deleted": "Deleted"}
    return "; ".join(f"{words[c['action']]}: {c['memory']}" for c in changes) or "Nothing new to remember"


def update_memories(ref: ModelRef, user_id: str, message: str, trace: Trace) -> list[dict]:
    """Saves what the message says about the user: a new fact is added, one that changes a saved memory
    replaces it, and "forget ..." deletes it. Returns the changes, like {"action": "saved", "memory": "..."}."""
    changes = []

    with trace.step("memory update", model=ref, fallback=True) as step:
        saved = search_memories(user_id, message, COMPARE_LIMIT)
        numbered = "\n".join(f"{number}. {m['memory']}" for number, m in enumerate(saved, start=1)) or "(none)"
        step["input"] = agent_input = f"Saved memories:\n{numbered}\n\nNew message from the user:\n{message}"

        reply = call_agent(ref, "memory.md", agent_input, step, reply_type=MemoryReply)
        by_number = {number: m for number, m in enumerate(saved, start=1)}

        for number in dict.fromkeys(reply.delete):
            if number in by_number:
                memory_store().delete(by_number.pop(number)["id"])
                changes.append({"action": "deleted", "memory": saved[number - 1]["memory"]})

        for change in reply.update:
            text = change.memory.strip()[:MAX_MEMORY_LENGTH]
            if change.number in by_number and text and text != by_number[change.number]["memory"]:
                # Replaced rather than updated: Mem0's update fails on Weaviate, as it sends the stored "id" back
                memory_store().delete(by_number.pop(change.number)["id"])
                memory_store().add(text, user_id=user_id, infer=False)
                changes.append({"action": "updated", "memory": text})

        known = {m["memory"] for m in saved}
        for text in dict.fromkeys(t.strip()[:MAX_MEMORY_LENGTH] for t in reply.add[:MAX_NEW_MEMORIES]):
            if text and text not in known:
                memory_store().add(text, user_id=user_id, infer=False)
                changes.append({"action": "saved", "memory": text})

        step["output"] = describe_changes(changes)

    if "error" in step:
        step["output"] = f"Couldn't update the memories: {step['error']}"

    return changes
