import json
import os
from dataclasses import dataclass, field
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from pipeline.llm import SELF_HOSTED_ERROR_HINTS

ModelKind = Literal["text", "vision"]


class ModelRef(BaseModel):
    """A model as the frontend picks it: an id plus where it runs."""

    id: str = Field(min_length=1)
    source: Literal["api", "self-hosted"] = "api"


@dataclass
class ResolvedModel:
    client: OpenAI
    id: str
    source: str
    # Passed to describe_llm_error so failures name the right service
    error_context: dict = field(default_factory=dict)


class ModelUnavailable(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class SelfHostedModel(BaseModel):
    id: str = Field(min_length=1)
    name: str = ""
    base_url: str = Field(min_length=1)
    kinds: list[ModelKind] = ["text"]


def load_self_hosted_models() -> tuple[list[SelfHostedModel], str | None]:
    """Self-hosted models from SELF_HOSTED_MODELS (a JSON list), plus an error if it can't be read.

    Example:
    SELF_HOSTED_MODELS=[{"id": "llama3.1:8b", "name": "Llama 3.1 8B",
                         "base_url": "http://10.0.0.5:11434/v1", "kinds": ["text"]}]
    """
    raw = os.getenv("SELF_HOSTED_MODELS", "").strip()

    if not raw:
        return [], None

    try:
        entries = json.loads(raw)

        if not isinstance(entries, list):
            raise ValueError("it must be a JSON list")

        return [SelfHostedModel.model_validate(entry) for entry in entries], None
    except (ValueError, ValidationError) as error:
        message = f"SELF_HOSTED_MODELS on the backend is invalid: {str(error)[:300]}"
        print(f"[models] {message}")
        return [], message


def list_self_hosted_models() -> dict:
    """What the frontend shows under "Self-hosted". Server addresses stay on the backend."""
    models, error = load_self_hosted_models()
    listing: dict = {
        kind: [{"id": m.id, "name": m.name or m.id} for m in models if kind in m.kinds]
        for kind in ("text", "vision")
    }

    if error:
        listing["error"] = error

    return listing


def find_self_hosted_model(model_id: str, kind: ModelKind) -> SelfHostedModel | None:
    models, _ = load_self_hosted_models()
    return next((m for m in models if m.id == model_id and kind in m.kinds), None)


def create_self_hosted_client(model: SelfHostedModel) -> OpenAI:
    # Servers like Ollama don't check the key, but the client needs a value
    return OpenAI(api_key=os.getenv("SELF_HOSTED_API_KEY") or "not-needed", base_url=model.base_url)


def resolve_model(ref: ModelRef, kind: ModelKind, gateway_client: OpenAI | None) -> ResolvedModel:
    """The client to call a picked model with: the AI Gateway, or its self-hosted server."""
    if ref.source == "self-hosted":
        model = find_self_hosted_model(ref.id, kind)

        if model is None:
            raise ModelUnavailable(
                f"The self-hosted {kind} model '{ref.id}' isn't set up on the backend. "
                "Pick another model, or add it to SELF_HOSTED_MODELS.",
                status_code=400,
            )

        return ResolvedModel(
            client=create_self_hosted_client(model),
            id=ref.id,
            source="self-hosted",
            error_context={
                "base_url": model.base_url,
                "hints": SELF_HOSTED_ERROR_HINTS,
                "provider": "The self-hosted server",
            },
        )

    if gateway_client is None:
        raise ModelUnavailable(
            "AI_GATEWAY_API_KEY is not set on the backend. Add it to the backend's environment variables and redeploy.",
            status_code=500,
        )

    return ResolvedModel(client=gateway_client, id=ref.id, source="api")
