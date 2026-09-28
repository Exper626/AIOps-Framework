from pipeline.models import ModelRef
from pipeline.retrieval_agent import run_retrieval_agent
from pipeline.trace import Trace
from rag.embedding import EMBEDDING_MODEL, create_embedding
from rag.lookup import find_attributes, find_devices
from rag.prompt import build_context
from rag.reranker import rerank_chunks
from rag.retrieval import attribute_filter, fetch_devices, retrieve_chunks

# Devices listed by name in the trace before "and N more"
LISTED_DEVICES = 5


def describe_devices(devices: list[str]) -> str:
    shown = ", ".join(devices[:LISTED_DEVICES])
    return shown + (f" and {len(devices) - LISTED_DEVICES} more" if len(devices) > LISTED_DEVICES else "")


def describe_passages(chunks: list[dict], how: str) -> str:
    if not chunks:
        return f"{how}: nothing relevant found, so the answer doesn't use the knowledge base"

    devices = list(dict.fromkeys(chunk.get("device") or chunk.get("filename") or "unnamed" for chunk in chunks))
    passages = f"{len(chunks)} passage{'s' if len(chunks) > 1 else ''}"

    # A match already names its devices
    if how.startswith("Matched"):
        return f"{how} · {passages}"

    return f"{how} · {passages} from {', '.join(devices)}"


def best(question: str, chunks: list[dict], rerank: bool, chunk_count: int, step: dict) -> list[dict]:
    if rerank and len(chunks) > chunk_count:
        try:
            return rerank_chunks(question, chunks, top_n=chunk_count)
        except Exception as error:
            # The passages found are still good: keep the search's own order
            print(f"[knowledge base] {error} (keeping the search order)")
            step["rerank_error"] = str(error)[:200]
    return chunks[:chunk_count]


def search_knowledge_base(ref: ModelRef, question: str, hybrid: bool, rerank: bool, chunk_count: int, trace: Trace) -> list[dict]:
    """The retrieval agent plans the search first: a device the question is about is fetched
    by name; a vendor, type or tag narrows the search; anything else is searched by keywords
    and meaning. Without a plan, the words of the question are matched instead."""
    plan = run_retrieval_agent(ref, question, trace)
    search = plan.search_text if plan and plan.search_text else question
    chunks = []

    with trace.step("knowledge base", input=search, fallback=True) as step:
        # Exact model numbers ("C9300X-48HX") are matched in the question as well
        devices = sorted({*plan.devices, *find_devices(question)}) if plan else find_devices(question)

        if devices:
            how = f"Matched {describe_devices(devices)}"
            chunks = best(question, fetch_devices(devices), rerank, chunk_count, step)
        else:
            step["model"] = EMBEDDING_MODEL
            vector = create_embedding(search)
            attributes = plan.filters() if plan else find_attributes(question)
            found = retrieve_chunks(search, vector, hybrid=hybrid, filters=attribute_filter(attributes)) if attributes else []

            if found:
                how = "Filtered by " + ", ".join(str(v) if not isinstance(v, list) else ", ".join(v) for v in attributes.values())
            else:
                how = "Searched by keywords and meaning" if hybrid else "Searched by meaning"
                found = retrieve_chunks(search, vector, hybrid=hybrid)

            chunks = best(question, found, rerank, chunk_count, step)

    step["output"] = describe_passages(chunks, how) if "error" not in step else "Answering without the knowledge base"
    if "rerank_error" in step:
        step["output"] += f" · reranking failed, so the search order was kept: {step['rerank_error']}"
    if chunks:
        # The passages exactly as the answer's prompt gets them
        step["raw_output"] = build_context(chunks)

    return chunks
