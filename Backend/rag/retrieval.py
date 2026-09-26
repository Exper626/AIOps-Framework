import atexit
from functools import cache

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery

from config import settings


COLLECTION_NAME = "NetworkDevice"
RETRIEVAL_TOP_K = 20
HYBRID_ALPHA = 0.5


@cache
def weaviate_client() -> weaviate.WeaviateClient:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=settings.weaviate_url,
        auth_credentials=Auth.api_key(settings.weaviate_api_key),
    )
    atexit.register(client.close)
    return client


def retrieve_chunks(query: str, query_vector: list[float], top_k: int = RETRIEVAL_TOP_K, hybrid: bool = True) -> list[dict]:
    collection = weaviate_client().collections.get(COLLECTION_NAME)

    if hybrid:
        response = collection.query.hybrid(
            query=query,
            vector=query_vector,
            alpha=HYBRID_ALPHA,
            limit=top_k,
            return_metadata=MetadataQuery(score=True),
        )
        return [{**obj.properties, "score": obj.metadata.score} for obj in response.objects]

    response = collection.query.near_vector(
        near_vector=query_vector,
        limit=top_k,
        return_metadata=MetadataQuery(distance=True),
    )
    return [{**obj.properties, "score": 1 - obj.metadata.distance} for obj in response.objects]
