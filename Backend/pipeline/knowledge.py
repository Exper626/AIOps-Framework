from pipeline.trace import Trace
from rag.embedding import EMBEDDING_MODEL, create_embedding
from rag.reranker import rerank_chunks
from rag.retrieval import retrieve_chunks


def describe_passages(chunks: list[dict]) -> str:
    if not chunks:
        return "Nothing relevant found, so the answer doesn't use the knowledge base"

    sources = list(dict.fromkeys(chunk.get("filename") or "unnamed document" for chunk in chunks))
    return f"Found {len(chunks)} passages, from: {', '.join(sources)}"


def search_knowledge_base(question: str, hybrid: bool, rerank: bool, chunk_count: int, trace: Trace) -> list[dict]:
    chunks = []

    with trace.step("knowledge base", input=question, fallback=True) as step:
        step["model"] = EMBEDDING_MODEL
        found = retrieve_chunks(question, create_embedding(question), hybrid=hybrid)
        chunks = rerank_chunks(question, found, top_n=chunk_count) if rerank else found[:chunk_count]

    step["output"] = describe_passages(chunks) if "error" not in step else "Answering without the knowledge base"

    return chunks
