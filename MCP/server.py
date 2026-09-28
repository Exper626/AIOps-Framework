"""The assistant's tools for MCP clients (Claude Desktop, Claude Code, Cursor, VS Code...):
search the device knowledge base, draw a network with Graphviz, and read a topology image.

It runs the Backend's own code (../Backend) with the Backend's keys (../Backend/.env).

    python server.py                    for a client on this computer, over stdin/stdout
    python server.py --http --port 8001 as a web server at /mcp; each request needs
                                        "Authorization: Bearer <MCP_API_KEY>"
"""

import argparse
import base64
import hmac
import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent / "Backend"

# MCP/.env first (MCP_API_KEY), then the Backend's keys; neither replaces a variable already set
load_dotenv(HERE / ".env")
load_dotenv(BACKEND / ".env")
sys.path.insert(0, str(BACKEND))

from graphviz import ExecutableNotFound  # noqa: E402
from mcp.server.mcpserver import Image, MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402
from mcp.server.transport_security import TransportSecuritySettings  # noqa: E402
from pydantic import BaseModel, ConfigDict, Field  # noqa: E402
from starlette.responses import JSONResponse  # noqa: E402
from starlette.types import ASGIApp, Receive, Scope, Send  # noqa: E402

from config import settings  # noqa: E402
from pipeline.agent import call_agent  # noqa: E402
from pipeline.diagram import DiagramContent, DiagramDevice, DiagramLink, to_diagram  # noqa: E402
from pipeline.errors import describe_error  # noqa: E402
from pipeline.knowledge import search_knowledge_base  # noqa: E402
from pipeline.models import DEFAULT_MODEL  # noqa: E402
from pipeline.topology_image import build_graph  # noqa: E402
from pipeline.trace import Trace  # noqa: E402
from rag.prompt import build_context  # noqa: E402

DeviceType = Literal["router", "multilayer_switch", "switch", "firewall", "access_point", "server", "pc", "laptop", "cloud", "other"]

mcp = MCPServer(
    name="SLT Network Assistant",
    instructions=(
        "Tools from Sri Lanka Telecom's network assistant. search_devices looks up Cisco and Juniper devices in "
        "SLT's knowledge base; draw_network draws a network as a picture; read_topology reads a topology image "
        "into the devices and cables draw_network takes."
    ),
)


class NetworkDevice(BaseModel):
    name: str = Field(description="A unique name, like Switch1 or PC3")
    type: DeviceType = Field(default="other", description="The kind of device, which picks its icon")
    model: str = Field(default="", description="The model, like 2960-24TT (optional)")


class NetworkCable(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    start: str = Field(alias="from", description="The name of the device at one end")
    end: str = Field(alias="to", description="The name of the device at the other end")


@mcp.tool()
def search_devices(question: str, passages: int = 5) -> str:
    """Search Sri Lanka Telecom's knowledge base of Cisco and Juniper switches, routers and access points
    (their product pages: models, specifications, ports, PoE, throughput, supported features). Use it for
    questions about specific devices, vendors or product lines. Returns the matching pages with their URLs."""
    trace = Trace()
    chunks = search_knowledge_base(DEFAULT_MODEL, question, True, True, max(1, min(passages, 20)), trace)

    failed = next((step["error"] for step in trace.steps if step["name"] == "knowledge base" and step.get("error")), None)
    if failed:
        raise ToolError(f"The knowledge base search failed: {failed}")

    return build_context(chunks) if chunks else "Nothing in the knowledge base matches this question."


@mcp.tool()
def draw_network(devices: list[NetworkDevice], links: list[NetworkCable]) -> Image:
    """Draw a network diagram as a PNG with Cisco icons, core devices above end devices.
    List each device once and each cable once (read_topology returns exactly this shape)."""
    diagram = to_diagram(
        DiagramContent(
            devices=[DiagramDevice(name=d.name, type=d.type, model=d.model) for d in devices],
            links=[DiagramLink.model_validate({"from": link.start, "to": link.end}) for link in links],
        )
    )
    if diagram is None:
        raise ToolError("Give at least one device to draw.")

    try:
        return Image(data=build_graph(diagram).pipe(), format="png")
    except ExecutableNotFound as error:
        raise ToolError("Graphviz isn't installed on this computer, so it can't draw (graphviz.org/download).") from error


@mcp.tool()
def read_topology(image: str) -> str:
    """Read a network topology image (a Cisco Packet Tracer screenshot works best) and return its devices
    and cables as JSON: {"devices": [...], "links": [...]}, the shape draw_network takes. `image` is an
    https URL of a PNG or JPEG, a data URL (data:image/png;base64,...) or plain base64."""
    image = image.strip()

    if not image.startswith(("https://", "data:image/")):
        try:
            jpeg = base64.b64decode(image[:24])[:2] == b"\xff\xd8"
        except ValueError:
            jpeg = False
        image = f"data:image/{'jpeg' if jpeg else 'png'};base64,{image}"

    content = [
        {"type": "text", "text": "Output the JSON for this image."},
        {"type": "image_url", "image_url": {"url": image}},
    ]
    try:
        return call_agent(DEFAULT_MODEL, "vision.md", content, {}, kind="vision", timeout=settings.vision_timeout_seconds)
    except Exception as error:
        raise ToolError(describe_error(error, "read_topology", DEFAULT_MODEL)) from error


class RequireKey:
    """Lets a web request through only with the MCP key, sent as "Authorization: Bearer <key>"."""

    def __init__(self, app: ASGIApp, key: str):
        self.app = app
        self.expected = f"Bearer {key}".encode()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            given = dict(scope["headers"]).get(b"authorization", b"")
            if not hmac.compare_digest(given, self.expected):
                response = JSONResponse({"detail": "Send the MCP key as 'Authorization: Bearer <key>'"}, status_code=401)
                return await response(scope, receive, send)

        await self.app(scope, receive, send)


def serve_http(host: str, port: int) -> None:
    import uvicorn

    key = os.environ.get("MCP_API_KEY", "")
    if not key:
        sys.exit("Set MCP_API_KEY (in MCP/.env or the environment) before serving over HTTP.")

    # Clients reach it by its real address, not localhost, so the SDK's localhost-only
    # host check is off; the key protects it instead
    app = mcp.streamable_http_app(
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    uvicorn.run(RequireKey(app, key), host=host, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SLT Network Assistant tools over MCP")
    parser.add_argument("--http", action="store_true", help="serve over HTTP at /mcp instead of stdin/stdout")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8001)))
    args = parser.parse_args()

    if args.http:
        serve_http(args.host, args.port)
    else:
        mcp.run()
