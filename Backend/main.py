from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from config import settings
from mcp_server import PICTURE_PATH, McpEndpoint, mcp, read_picture_link
from pipeline.chat import ChatRequest, run_chat
from pipeline.diagram import Diagram
from pipeline.memory import delete_all_memories, delete_memory, list_memories
from pipeline.errors import PipelineError
from pipeline.models import DEFAULT_MODEL, list_self_hosted_models, resolve_model
from pipeline.title import write_title
from pipeline.topology_image import build_graph, render_png, to_data_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    # The MCP tools' sessions (mcp_server.py)
    async with mcp.session_manager.run():
        yield


app = FastAPI(title="AIOps Backend", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# MCP clients (DeepSeek Harness, Claude Desktop...) use the assistant's tools at /mcp (with MCP_API_KEY once set)
app.add_middleware(McpEndpoint, key=settings.mcp_api_key)


@app.exception_handler(PipelineError)
def pipeline_error(request: Request, error: PipelineError):
    return JSONResponse(status_code=400, content={"detail": str(error)})


@app.get("/")
def root():
    return {"status": "ok", "service": "AIOps Backend"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/models")
def models():
    # Also says which model a step uses when none is picked in Settings
    return {**list_self_hosted_models(), "default_model": DEFAULT_MODEL.id}


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise PipelineError("Message cannot be empty")

    answer_model = resolve_model(request.answer_model or DEFAULT_MODEL, "text")
    return StreamingResponse(run_chat(request, answer_model), media_type="application/x-ndjson")


class TitleRequest(BaseModel):
    message: str = Field(min_length=1)


@app.post("/title")
def title(request: TitleRequest):
    # The name of a new chat in the sidebar, from its first message
    return {"title": write_title(request.message)}


def check_size(diagram: Diagram) -> None:
    if not diagram.devices:
        raise PipelineError("The diagram has no devices to draw")
    if len(diagram.devices) > 200 or len(diagram.links) > 500:
        raise PipelineError("The diagram is too big to draw (at most 200 devices and 500 cables)")


@app.post("/diagram/image")
def diagram_image(diagram: Diagram):
    # Redraws an answer's picture after someone edits the diagram in the chat
    check_size(diagram)
    return {"image": to_data_url(render_png(build_graph(diagram)))}


@app.get(PICTURE_PATH)
def diagram_picture(d: str = Query(max_length=20_000)):
    # The pictures draw_network links to (mcp_server.py), drawn again from the diagram inside the link
    diagram = read_picture_link(d)
    if diagram is None:
        raise PipelineError("This picture link is broken")

    check_size(diagram)
    png = render_png(build_graph(diagram))
    return Response(png, media_type="image/png", headers={"Cache-Control": "public, max-age=31536000, immutable"})


@app.get("/memories")
def memories(user_id: str):
    # Each user's memories, for Settings → Memory in the frontend
    return {"memories": list_memories(user_id)}


@app.delete("/memories/{memory_id}")
def forget_memory(memory_id: str, user_id: str):
    delete_memory(user_id, memory_id)
    return {"deleted": True}


@app.delete("/memories")
def forget_all_memories(user_id: str):
    delete_all_memories(user_id)
    return {"deleted": True}
