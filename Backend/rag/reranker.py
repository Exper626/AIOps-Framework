import requests

from config import settings


RERANK_MODEL = "qwen3-rerank"
RERANK_TOP_N = 5
RERANK_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/reranks"


def rerank_chunks(query: str, chunks: list[dict], top_n: int = RERANK_TOP_N) -> list[dict]:
    candidates = [chunk for chunk in chunks if (chunk.get("text") or "").strip()]

    if not candidates:
        return []

    documents = [chunk["text"].strip() for chunk in candidates]
    top_n = min(top_n, len(documents))

    response = requests.post(
        RERANK_URL,
        headers={
            "Authorization": f"Bearer {settings.dashscope_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": RERANK_MODEL,
            "query": query.strip(),
            "documents": documents,
            "top_n": top_n,
            "instruct": "Given a web search query, retrieve relevant passages that answer the query.",
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(f"Reranker failed: {response.status_code} {response.text}")

    data = response.json()
    reranked = []

    for item in data.get("results", []):
        index = item.get("index")

        if not isinstance(index, int) or not 0 <= index < len(candidates):
            continue

        reranked.append({**candidates[index], "rerank_score": item.get("relevance_score")})

    return reranked
