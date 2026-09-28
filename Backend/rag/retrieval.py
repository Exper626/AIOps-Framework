import atexit
from functools import cache

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter, MetadataQuery

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


def attribute_filter(attributes: dict) -> Filter | None:
    """{"vendor": "Juniper", "device_type": "access point", "tags": ["Outdoor"]} as a Weaviate filter"""
    parts = [Filter.by_property(name).equal(attributes[name]) for name in ("vendor", "device_type") if name in attributes]
    if attributes.get("tags"):
        parts.append(Filter.by_property("tags").contains_all(attributes["tags"]))
    return Filter.all_of(parts) if parts else None


def fetch_devices(devices: list[str], limit: int = RETRIEVAL_TOP_K) -> list[dict]:
    """The entries for these devices, by exact name"""
    collection = weaviate_client().collections.get(COLLECTION_NAME)
    response = collection.query.fetch_objects(filters=Filter.by_property("device").contains_any(devices), limit=limit)
    return [{**obj.properties, "score": None} for obj in response.objects]


def retrieve_chunks(
    query: str, query_vector: list[float], top_k: int = RETRIEVAL_TOP_K, hybrid: bool = True, filters: Filter | None = None
) -> list[dict]:
    collection = weaviate_client().collections.get(COLLECTION_NAME)

    if hybrid:
        response = collection.query.hybrid(
            query=query,
            vector=query_vector,
            alpha=HYBRID_ALPHA,
            limit=top_k,
            filters=filters,
            return_metadata=MetadataQuery(score=True),
        )
        return [{**obj.properties, "score": obj.metadata.score} for obj in response.objects]

    response = collection.query.near_vector(
        near_vector=query_vector,
        limit=top_k,
        filters=filters,
        return_metadata=MetadataQuery(distance=True),
    )
    return [{**obj.properties, "score": 1 - obj.metadata.distance} for obj in response.objects]
