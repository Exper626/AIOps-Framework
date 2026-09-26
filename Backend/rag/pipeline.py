from rag.embedding import create_embedding
from rag.generation import generate_answer
from rag.prompt import build_context, build_messages
from rag.reranker import rerank_chunks
from rag.retrieval import retrieve_chunks


def run_rag(query: str, model: str, hybrid_search: bool = True, reranker: bool = True, chunk_count: int = 5) -> str:
    query = query.strip()
    model = model.strip()

    if not query:
        raise ValueError("Query cannot be empty")

    if not model:
        raise ValueError("Model cannot be empty")

    print(f"[RAG] Query: {query}")
    print(f"[RAG] Generation model: {model}")

    query_vector = create_embedding(query)
    print(f"[RAG] Embedding dimension: {len(query_vector)}")

    retrieved = retrieve_chunks(query, query_vector, hybrid=hybrid_search)
    print(f"[RAG] Retrieved chunks: {len(retrieved)} ({'hybrid' if hybrid_search else 'vector'} search)")

    reranked = rerank_chunks(query, retrieved, top_n=chunk_count) if reranker else retrieved[:chunk_count]
    print(f"[RAG] Chunks for the answer: {len(reranked)}")

    if not reranked:
        return "I could not find enough relevant information in the knowledge base to answer that question."

    context = build_context(reranked)
    messages = build_messages(query, context)

    answer = generate_answer(messages, model)
    print("[RAG] Answer generated")

    return answer
