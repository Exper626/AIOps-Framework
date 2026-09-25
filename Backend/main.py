import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

# Imported after load_dotenv() so these modules see the values from .env
from pipeline.agents import (  # noqa: E402
    CONTEXT_MODEL,
    QUERY_MODEL,
    Plan,
    build_plan,
    context_agent_runs,
    run_context_agent,
    run_query_agent,
)
from pipeline.llm import create_client, describe_llm_error  # noqa: E402
from pipeline.models import ModelRef, ModelUnavailable, list_self_hosted_models, resolve_model  # noqa: E402
from pipeline.trace import Trace  # noqa: E402

TEXT_PROMPT_PATH = Path(__file__).parent / "prompts" / "text.md"

# Sends a step-by-step trace with every answer, shown as "Pipeline trace" in the chat.
# It includes prompts and model output, so keep it off for real users.
DEBUG_TRACE = os.getenv("DEBUG_TRACE", "false").strip().lower() in ("1", "true", "yes")

TRACE_CHARS = 1000  # per message in the trace, so saved chats don't grow too large

app = FastAPI(title="AIOps Backend", version="0.1.0")


allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    # The answer model; "api" = the AI Gateway, "self-hosted" = one of SELF_HOSTED_MODELS
    model: str
    text_source: Literal["api", "self-hosted"] = "api"
    history: list[HistoryMessage] = []
    # Models for the agents before the answer; the backend defaults are used when missing
    query_model: ModelRef | None = None
    context_model: ModelRef | None = None
    # Settings → Agents switches, e.g. {"queryTransformation": false}
    agents: dict[str, bool] = {}
    # Settings → Knowledge Base; for when knowledge base search is added (see rag/reranker.py)
    reranker: bool = True


def to_event(data: dict, trace: Trace | None = None) -> str:
    """One line of the NDJSON stream the frontend reads."""
    if trace is not None and DEBUG_TRACE:
        data = {**data, "debug": trace.to_dict()}

    return json.dumps(data) + "\n"


def build_answer_messages(message: str, history: list[dict], plan: Plan) -> list[dict]:
    messages = []

    # prompts/text.md becomes the system prompt once it has content
    system_prompt = TEXT_PROMPT_PATH.read_text(encoding="utf-8").strip() if TEXT_PROMPT_PATH.exists() else ""
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if plan.needs_history:
        messages.extend(history)
        question = message
    elif plan.standalone_question == message:
        question = message
    else:
        # Without the history the question must stand on its own, so the rewrite leads.
        # The user's own words stay alongside it in case the rewrite changed the meaning.
        question = f'{plan.standalone_question}\n\n(The user\'s exact words: "{message}")'

    if len(plan.sub_questions) > 1:
        numbered = "\n".join(f"{i}. {sub.question}" for i, sub in enumerate(plan.sub_questions, start=1))
        question = (
            f"{question}\n\nThis message contains {len(plan.sub_questions)} separate questions. "
            f"Answer each one in order, under its own short heading:\n{numbered}"
        )

    messages.append({"role": "user", "content": question})

    return messages


def preview(messages: list[dict]) -> list[dict]:
    """Messages as they appear in the trace, with long contents shortened."""
    return [
        {**m, "content": m["content"] if len(m["content"]) <= TRACE_CHARS else m["content"][:TRACE_CHARS] + "…"}
        for m in messages
    ]


@app.get("/")
def root():
    return {"status": "ok", "service": "AIOps Backend"}


@app.get("/health")
def health():
    """Railway hits this to confirm the service is alive."""
    return {"status": "healthy"}


@app.get("/api/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}


@app.get("/models")
def models():
    """Self-hosted models the frontend lets users pick, by kind: {"text": [...], "vision": [...]}."""
    return list_self_hosted_models()


@app.post("/chat")
def chat(request: ChatRequest):
    """Run the query and context management agents, then stream the answer back as NDJSON."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if not request.model.strip():
        raise HTTPException(status_code=400, detail="Model cannot be empty")

    api_key = os.getenv("AI_GATEWAY_API_KEY")
    gateway_client = create_client(api_key) if api_key else None

    # The answer model must be usable before streaming starts; the agents fall back instead
    try:
        answer_model = resolve_model(
            ModelRef(id=request.model.strip(), source=request.text_source), "text", gateway_client
        )
    except ModelUnavailable as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error

    query_ref = request.query_model or ModelRef(id=QUERY_MODEL)
    context_ref = request.context_model or ModelRef(id=CONTEXT_MODEL)
    query_enabled = request.agents.get("queryTransformation", True)
    context_enabled = request.agents.get("contextManagement", True)

    message = request.message.strip()
    history = [m.model_dump() for m in request.history]
    trace = Trace()

    def stream():
        # 1. Query agent: rewrite the message and split it into sub-questions
        if query_enabled:
            yield to_event({"phase": "query", "message": "Understanding your question..."})
        query = run_query_agent(query_ref, gateway_client, message, history, trace, enabled=query_enabled)

        # 2. Context management agent: which context each sub-question needs
        if context_agent_runs(context_enabled, history):
            yield to_event({"phase": "context", "message": "Checking what context is needed..."})
        needs = run_context_agent(
            context_ref, gateway_client, query.sub_questions, history, trace, enabled=context_enabled
        )
        plan = build_plan(query, needs)
        messages = build_answer_messages(message, history, plan)

        # 3. Answer: the model picked for answers, streamed
        yield to_event({"phase": "answer", "message": "Writing the answer...", "modelId": answer_model.id})
        parts = []

        with trace.step("answer", model=answer_model.id, input=preview(messages)) as step:
            step["source"] = answer_model.source

            try:
                response = answer_model.client.chat.completions.create(
                    model=answer_model.id, messages=messages, stream=True
                )

                for chunk in response:
                    if not chunk.choices:
                        continue

                    delta = chunk.choices[0].delta.content

                    if delta:
                        parts.append(delta)
                        yield to_event({"phase": "delta", "delta": delta})
            except Exception as error:
                step["error"] = describe_llm_error(error, answer_model.id, **answer_model.error_context)

            answer = "".join(parts)
            step["output"] = {"chars": len(answer)}

            if "error" not in step and not answer.strip():
                step["error"] = "The model returned an empty answer"

        print(f"[chat] {trace.summary()}")

        if "error" in step:
            print(f"[chat] {step['error']}")
            yield to_event({"phase": "error", "error": step["error"]}, trace)
            return

        yield to_event({"phase": "done", "message": answer}, trace)

    return StreamingResponse(stream(), media_type="application/x-ndjson")
