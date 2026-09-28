from pipeline.trace import Trace
from rag.embedding import EMBEDDING_MODEL, create_embedding
from rag.lookup import find_attributes, find_devices
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
    return f"{how}. Using {len(chunks)} passage{'s' if len(chunks) > 1 else ''}, from: {', '.join(devices)}"


def best(question: str, chunks: list[dict], rerank: bool, chunk_count: int) -> list[dict]:
    if rerank and len(chunks) > chunk_count:
        return rerank_chunks(question, chunks, top_n=chunk_count)
    return chunks[:chunk_count]


def search_knowledge_base(question: str, hybrid: bool, rerank: bool, chunk_count: int, trace: Trace) -> list[dict]:
    """Metadata first: a device the question names is looked up by name; a vendor,
    type or tag narrows the search; anything else is searched by keywords and meaning."""
    chunks = []

    with trace.step("knowledge base", input=question, fallback=True) as step:
        devices = find_devices(question)

        if devices:
            how = f"Matched {describe_devices(devices)}"
            chunks = best(question, fetch_devices(devices), rerank, chunk_count)
        else:
            step["model"] = EMBEDDING_MODEL
            vector = create_embedding(question)
            attributes = find_attributes(question)
            found = retrieve_chunks(question, vector, hybrid=hybrid, filters=attribute_filter(attributes)) if attributes else []

            if found:
                how = "Filtered by " + ", ".join(str(v) if not isinstance(v, list) else ", ".join(v) for v in attributes.values())
            else:
                how = "Searched by keywords and meaning" if hybrid else "Searched by meaning"
                found = retrieve_chunks(question, vector, hybrid=hybrid)

            chunks = best(question, found, rerank, chunk_count)

    step["output"] = describe_passages(chunks, how) if "error" not in step else "Answering without the knowledge base"

    return chunks
