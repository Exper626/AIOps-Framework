import json
from collections.abc import Iterator
from typing import Literal

from pydantic import BaseModel, Field

from config import settings
from pipeline.answer import build_answer_messages, write_answer
from pipeline.context import context_runs, run_context
from pipeline.errors import describe_error
from pipeline.models import DEFAULT_MODEL, ModelRef, ResolvedModel
from pipeline.query import run_query
from pipeline.trace import Trace
from pipeline.vision import ImageInput, describe_images


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []
    answer_model: ModelRef | None = None
    query_model: ModelRef | None = None
    context_model: ModelRef | None = None
    vision_model: ModelRef | None = None
    agents: dict[str, bool] = {}
    reranker: bool = True
    hybrid_search: bool = True
    chunk_count: int = Field(default=5, ge=1, le=20)
    images: list[ImageInput] = []


def to_event(data: dict, trace: Trace | None = None) -> str:
    if trace is not None and settings.debug_trace:
        data = {**data, "debug": trace.to_dict()}

    return json.dumps(data) + "\n"


def run_steps(request: ChatRequest, answer_model: ResolvedModel, trace: Trace) -> Iterator[dict]:
    message = request.message.strip()
    history = [m.model_dump() for m in request.history]
    query_enabled = request.agents.get("queryTransformation", True)
    context_enabled = request.agents.get("contextManagement", True)

    descriptions = []
    if request.images:
        yield {"phase": "vision", "message": "Reading the attached image..."}
        descriptions = describe_images(request.vision_model or DEFAULT_MODEL, request.images, trace)

    if query_enabled:
        yield {"phase": "query", "message": "Understanding your question..."}
    question = run_query(request.query_model or DEFAULT_MODEL, message, history, trace, enabled=query_enabled)

    if context_runs(context_enabled, history):
        yield {"phase": "context", "message": "Checking what context is needed..."}
    selected = run_context(request.context_model or DEFAULT_MODEL, question, history, trace, enabled=context_enabled)

    messages = build_answer_messages(message, question, selected, descriptions)
    yield {"phase": "answer", "message": "Writing the answer...", "modelId": answer_model.id}

    yield from write_answer(answer_model, messages, trace)


def run_chat(request: ChatRequest, answer_model: ResolvedModel) -> Iterator[str]:
    trace = Trace()

    try:
        for event in run_steps(request, answer_model, trace):
            yield to_event(event, trace if event["phase"] == "done" else None)
    except Exception as error:
        message = describe_error(error, "chat")
        print(f"[chat] {message}")
        yield to_event({"phase": "error", "error": message}, trace)

    print(f"[chat] {trace.summary()}")
