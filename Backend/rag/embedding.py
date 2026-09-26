from pipeline.llm import gateway_client


EMBEDDING_MODEL = "openai/text-embedding-3-small"


def create_embedding(query: str) -> list[float]:
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty")

    response = gateway_client.embeddings.create(model=EMBEDDING_MODEL, input=query)

    if not response.data:
        raise RuntimeError("Embedding API returned no embedding")

    return response.data[0].embedding
