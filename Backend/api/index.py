from fastapi import FastAPI
from pydantic import BaseModel

from rag.pipeline import run_rag


app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    model: str


@app.get("/")
def root():
    return {"status": "Nawaloka backend is working"}


@app.post("/chat")
def chat(request: ChatRequest):
    answer = run_rag(request.message, request.model)

    return {
        "message": answer,
    }
