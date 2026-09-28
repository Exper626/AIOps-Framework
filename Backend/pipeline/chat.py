import json
from collections.abc import Iterator
from typing import Literal

from pydantic import BaseModel, Field

from config import settings
from pipeline.answer import build_answer_messages, describe_sources, write_answer
from pipeline.caption import write_caption
from pipeline.context import run_context
from pipeline.diagram import Diagram, describe_diagram, run_diagram
from pipeline.errors import describe_error
from pipeline.knowledge import search_knowledge_base
from pipeline.models import DEFAULT_MODEL, ModelRef, ResolvedModel
from pipeline.query import run_query
from pipeline.router import run_router
from pipeline.topology_image import draw_topology_image
from pipeline.trace import Trace
from pipeline.vision import ImageInput, describe_images, topology_models


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    diagram: Diagram | None = None

    def to_dict(self) -> dict:
        if self.diagram is None:
            return {"role": self.role, "content": self.content}

        return {"role": self.role, "content": f"{self.content}\n\nNetwork diagram:\n{describe_diagram(self.diagram)}"}


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []
    router_model: ModelRef | None = None
    answer_model: ModelRef | None = None
    query_model: ModelRef | None = None
    context_model: ModelRef | None = None
    vision_model: ModelRef | None = None
    reranker: bool = True
    hybrid_search: bool = True
    chunk_count: int = Field(default=5, ge=1, le=20)
    images: list[ImageInput] = []
    diagram: Diagram | None = None


def to_event(data: dict, trace: Trace | None = None) -> str:
    if trace is not None and settings.debug_trace:
        data = {**data, "debug": trace.to_dict()}

    return json.dumps(data) + "\n"


def run_steps(request: ChatRequest, answer_model: ResolvedModel, trace: Trace) -> Iterator[dict]:
    message = request.message.strip()
    history = [m.to_dict() for m in request.history]

    yield {"phase": "router", "message": "Planning the steps..."}
    plan = run_router(request.router_model or DEFAULT_MODEL, message, history, len(request.images), request.diagram is not None, trace)

    descriptions = []
    if plan.has("image_description"):
        yield {"phase": "vision", "message": "Reading the attached image..."}
        descriptions = describe_images(request.vision_model or DEFAULT_MODEL, request.images, trace)

    yield {"phase": "query", "message": "Understanding your question..."}
    question = run_query(request.query_model or DEFAULT_MODEL, message, history, trace)

    if history:
        yield {"phase": "context", "message": "Checking what context is needed..."}
    selected = run_context(request.context_model or DEFAULT_MODEL, question, history, trace)

    passages = []
    if plan.has("retrieval"):
        yield {"phase": "vector", "message": "Searching the knowledge base..."}
        # Models read from an attached topology are searched for too
        models = list(dict.fromkeys(m for d in descriptions if d.description for m in topology_models(d.description)))
        search = f"{question}\nDevices in the attached image: {', '.join(models)}" if models else question
        passages = search_knowledge_base(
            request.query_model or DEFAULT_MODEL, search, request.hybrid_search, request.reranker, request.chunk_count, trace
        )

    answer = ""
    if plan.has("text_generation"):
        messages = build_answer_messages(message, question, selected, descriptions, request.diagram, passages)
        yield {"phase": "answer", "message": "Writing the answer...", "modelId": answer_model.id}
        sources = describe_sources(message, question, selected, descriptions, request.diagram, passages)
        answer = yield from write_answer(answer_model, messages, sources, trace)

    if plan.has("image_generation"):
        if not answer:
            yield {"phase": "answer", "message": "Drawing the diagram..."}
        images = [d.description for d in descriptions if d.description]
        earlier = [m.diagram for m in request.history if m.diagram and m.to_dict() in selected]
        diagram = run_diagram(
            request.answer_model or DEFAULT_MODEL, question, answer, images, request.diagram, earlier[-1] if earlier else None, passages, trace
        )

        # Only a picture was asked for: a short caption of it, instead of an answer
        if not answer:
            answer = (
                write_caption(request.answer_model or DEFAULT_MODEL, question, diagram, trace)
                if diagram
                else "I couldn't find a network to draw in your message. List its devices and how they are connected, and I'll draw it."
            )
            yield {"phase": "delta", "delta": answer}

        if diagram:
            yield {"phase": "diagram", "diagram": diagram.model_dump(), "image": draw_topology_image(diagram, trace)}

    yield {"phase": "done", "message": answer}


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
