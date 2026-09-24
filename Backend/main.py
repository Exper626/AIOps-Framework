import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

AI_GATEWAY_BASE_URL = os.getenv("AI_GATEWAY_BASE_URL", "https://ai-gateway.vercel.sh/v1")
TEXT_PROMPT_PATH = Path(__file__).parent / "prompts" / "text.md"

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
        raise HTTPException(status_code=500, detail="AI_GATEWAY_API_KEY is not set")

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
            print(f"[chat] LLM call failed: {error}")
            yield to_event({"phase": "error", "error": f"LLM call failed: {error}"})
            return

        answer = "".join(parts)

        if not answer.strip():
            yield to_event({"phase": "error", "error": "The model returned an empty answer"})
            return

        yield to_event({"phase": "done", "message": answer})

    return StreamingResponse(stream(), media_type="application/x-ndjson")
