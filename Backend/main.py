import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI
from pydantic import BaseModel

load_dotenv()

AI_GATEWAY_BASE_URL = os.getenv("AI_GATEWAY_BASE_URL", "https://ai-gateway.vercel.sh/v1")
TEXT_PROMPT_PATH = Path(__file__).parent / "prompts" / "text.md"

# Added to the gateway's own error message so it says what to fix
LLM_ERROR_HINTS = {
    401: " Check that AI_GATEWAY_API_KEY on the backend is a valid AI Gateway key.",
    404: " The model id probably doesn't exist on the AI Gateway; pick another model.",
    429: " Rate or credit limit reached; wait a moment or check your AI Gateway balance.",
}

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
    model: str
    history: list[HistoryMessage] = []


def to_event(data: dict) -> str:
    """One line of the NDJSON stream the frontend reads."""
    return json.dumps(data) + "\n"


def build_messages(request: ChatRequest) -> list[dict]:
    messages = []

    # prompts/text.md becomes the system prompt once it has content
    system_prompt = TEXT_PROMPT_PATH.read_text(encoding="utf-8").strip() if TEXT_PROMPT_PATH.exists() else ""
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.extend(message.model_dump() for message in request.history)
    messages.append({"role": "user", "content": request.message.strip()})

    return messages


def describe_llm_error(error: Exception, model: str) -> str:
    """Turn an AI Gateway failure into a message that says what to fix."""
    if isinstance(error, APITimeoutError):
        return f"The AI Gateway did not answer in time for model '{model}'. Try again or pick a faster model."

    if isinstance(error, APIConnectionError):
        return f"Could not reach the AI Gateway at {AI_GATEWAY_BASE_URL}: {error.__cause__ or error}"

    if isinstance(error, APIStatusError):
        body = error.body
        reason = (body.get("message") if isinstance(body, dict) else None) or str(body or error)
        hint = LLM_ERROR_HINTS.get(error.status_code, "")
        return f"The AI Gateway rejected the request for model '{model}' ({error.status_code}): {reason.rstrip('.')}.{hint}"

    return f"LLM call failed: {error}"


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


@app.post("/chat")
def chat(request: ChatRequest):
    """Send the user's message to the LLM and stream the answer back as NDJSON."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if not request.model.strip():
        raise HTTPException(status_code=400, detail="Model cannot be empty")

    api_key = os.getenv("AI_GATEWAY_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="AI_GATEWAY_API_KEY is not set on the backend. Add it to the backend's environment variables and redeploy.",
        )

    client = OpenAI(api_key=api_key, base_url=AI_GATEWAY_BASE_URL)
    model = request.model.strip()
    messages = build_messages(request)

    def stream():
        parts = []

        try:
            response = client.chat.completions.create(model=model, messages=messages, stream=True)

            for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta.content

                if delta:
                    parts.append(delta)
                    yield to_event({"phase": "delta", "delta": delta})
        except Exception as error:
            description = describe_llm_error(error, model)
            print(f"[chat] {description}")
            yield to_event({"phase": "error", "error": description})
            return

        answer = "".join(parts)

        if not answer.strip():
            yield to_event({"phase": "error", "error": "The model returned an empty answer"})
            return

        yield to_event({"phase": "done", "message": answer})

    return StreamingResponse(stream(), media_type="application/x-ndjson")
