from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import cache
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from config import ModelKind, SelfHostedServer, settings
from pipeline.errors import ModelUnavailable
from pipeline.llm import gateway_client

DISCOVERY_TIMEOUT_SECONDS = 15


class ModelRef(BaseModel):
    id: str = Field(min_length=1)
    source: Literal["api", "self-hosted"] = "api"


DEFAULT_MODEL = ModelRef(id="google/gemini-2.5-flash")


@dataclass
class ResolvedModel:
    client: OpenAI
    id: str
    source: str


@dataclass
class SelfHostedModel:
    id: str
    server: SelfHostedServer


known_models: dict[str, SelfHostedModel] = {}


@cache
def self_hosted_client(base_url: str) -> OpenAI:
    return OpenAI(api_key=settings.self_hosted_api_key, base_url=base_url)


def ask_server_for_models(server: SelfHostedServer) -> list[str]:
    client = self_hosted_client(server.base_url).with_options(timeout=DISCOVERY_TIMEOUT_SECONDS, max_retries=0)
    return [model.id for model in client.models.list()]


def discover_self_hosted_models() -> list[str]:
    servers = settings.self_hosted_servers

    with ThreadPoolExecutor(max_workers=max(len(servers), 1)) as pool:
        replies = [(server, pool.submit(ask_server_for_models, server)) for server in servers]

    unreachable = []

    for server, reply in replies:
        if reply.exception():
            unreachable.append(f"{server.base_url} ({reply.exception()})")
            continue

        for model_id in [m.id for m in known_models.values() if m.server == server]:
            del known_models[model_id]

        for model_id in reply.result():
            known_models[model_id] = SelfHostedModel(id=model_id, server=server)

    return unreachable


def list_self_hosted_models() -> dict:
    unreachable = discover_self_hosted_models()
    listing: dict = {
        kind: [{"id": m.id, "name": m.id.rsplit("/", 1)[-1]} for m in known_models.values() if kind in m.server.kinds]
        for kind in ("text", "vision")
    }

    if unreachable:
        listing["error"] = "Couldn't get the models from " + "; ".join(unreachable)

    return listing


def resolve_model(ref: ModelRef, kind: ModelKind) -> ResolvedModel:
    if ref.source == "api":
        return ResolvedModel(client=gateway_client, id=ref.id, source="api")

    if ref.id not in known_models:
        discover_self_hosted_models()

    model = known_models.get(ref.id)

    if model is None:
        raise ModelUnavailable(
            f"The self-hosted model '{ref.id}' isn't served by any server in SELF_HOSTED_SERVERS right now. "
            "Pick another model, or check that its server is running."
        )

    if kind not in model.server.kinds:
        raise ModelUnavailable(
            f"The self-hosted model '{ref.id}' isn't set up as a {kind} model: add \"{kind}\" to the kinds "
            "of its server in SELF_HOSTED_SERVERS, or pick another model."
        )

    return ResolvedModel(client=self_hosted_client(model.server.base_url), id=ref.id, source="self-hosted")
