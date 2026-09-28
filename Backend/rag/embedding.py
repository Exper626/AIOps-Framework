import requests

from config import settings


# Must match embedding.model and embedding.dim in Knowledge Base/Scripts/config.yaml,
# which the knowledge base was loaded with: vectors from different models don't compare
EMBEDDING_MODEL = "text-embedding-v4"
EMBEDDING_DIM = 1024
EMBEDDING_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

# A question is embedded as a query, with a short description of the task; the
# knowledge base pages were embedded as documents
QUERY_INSTRUCTION = "Given a question about network devices, retrieve the product pages that answer it"


def create_embedding(query: str) -> list[float]:
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty")

    response = requests.post(
        EMBEDDING_URL,
        headers={"Authorization": f"Bearer {settings.dashscope_api_key}"},
        json={
            "model": EMBEDDING_MODEL,
            "input": {"texts": [query]},
            "parameters": {"dimension": EMBEDDING_DIM, "text_type": "query", "instruct": QUERY_INSTRUCTION},
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(f"Embedding failed: {response.status_code} {response.text}")

    embeddings = response.json().get("output", {}).get("embeddings") or []

    if not embeddings:
        raise RuntimeError("Embedding API returned no embedding")

    return embeddings[0]["embedding"]
