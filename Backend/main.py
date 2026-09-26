from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from config import settings
from pipeline.chat import ChatRequest, run_chat
from pipeline.errors import PipelineError
from pipeline.models import DEFAULT_MODEL, list_self_hosted_models, resolve_model

app = FastAPI(title="AIOps Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(PipelineError)
def pipeline_error(request: Request, error: PipelineError):
    return JSONResponse(status_code=400, content={"detail": str(error)})


@app.get("/")
def root():
    return {"status": "ok", "service": "AIOps Backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}


@app.get("/models")
def models():
    return list_self_hosted_models()


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise PipelineError("Message cannot be empty")

    answer_model = resolve_model(request.answer_model or DEFAULT_MODEL, "text")
    return StreamingResponse(run_chat(request, answer_model), media_type="application/x-ndjson")
