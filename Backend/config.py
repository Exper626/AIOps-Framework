from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ModelKind = Literal["text", "vision"]


class SelfHostedServer(BaseModel):
    base_url: str = Field(min_length=1)
    kinds: list[ModelKind] = ["text"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    ai_gateway_api_key: str
    dashscope_api_key: str
    weaviate_url: str
    weaviate_api_key: str

    self_hosted_servers: list[SelfHostedServer] = []
    self_hosted_api_key: str = "not-needed"
    debug_trace: bool = False
    allowed_origins: str = "*"
    vision_timeout_seconds: float = 40
    # The Weaviate cluster and collection Mem0 keeps each user's memories in. A free Weaviate Cloud cluster
    # holds one collection, which the knowledge base uses, so the memories need a cluster of their own.
    # Without one set, the knowledge base's cluster is used.
    memory_weaviate_url: str = ""
    memory_weaviate_api_key: str = ""
    memory_collection: str = "Memories"


settings = Settings()
