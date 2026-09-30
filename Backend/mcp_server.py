"""The assistant's tools for MCP clients (DeepSeek Harness, Claude Desktop, Cursor, VS Code...): search the
device knowledge base, draw a network with Graphviz, and read a topology image.

main.py serves them at /mcp: to anyone with the address while MCP_API_KEY is empty, else only to clients
that send "Authorization: Bearer <MCP_API_KEY>". For a client on this computer instead, run
`python mcp_server.py` in this folder (over stdin/stdout)."""

import base64
import hmac
from typing import Literal

from graphviz import ExecutableNotFound
from mcp.server.mcpserver import Image, MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import BaseModel, ConfigDict, Field
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from config import settings
from pipeline.agent import call_agent
from pipeline.devices import DEVICE_KINDS
from pipeline.diagram import DiagramContent, DiagramDevice, DiagramLink, to_diagram
from pipeline.errors import describe_error
from pipeline.knowledge import search_knowledge_base
from pipeline.models import DEFAULT_MODEL
from pipeline.topology_image import build_graph
from pipeline.trace import Trace
from rag.prompt import build_context

MCP_PATH = "/mcp"

# The kinds of device (pipeline/devices.py), each with its icon and place in the picture
DeviceType = Literal[tuple(DEVICE_KINDS)]  # type: ignore[valid-type]

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
    # No conversation, memories or image here: just the question
    chunks = search_knowledge_base(DEFAULT_MODEL, question, [], "", [], True, True, max(1, min(passages, 20)), trace)

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


NOT_AN_IMAGE = (
    "`image` must be the picture itself: an https link, a data URL or base64. This looks like a file path, and "
    "this server can't open files on your computer. If you can see the image yourself, read its devices and "
    "cables and call draw_network with them."
)


@mcp.tool()
def read_topology(image: str) -> str:
    """Read a network topology image (a Cisco Packet Tracer screenshot works best) and return its devices
    and cables as JSON: {"devices": [...], "links": [...]}, the shape draw_network takes. `image` is the
    picture itself: an https URL of a PNG or JPEG, a data URL (data:image/png;base64,...) or plain base64.
    Not a file path: this server runs online and can't open files on the user's computer. If you can see
    the image yourself, you can read it and call draw_network directly."""
    image = image.strip()

    if not image.startswith(("https://", "data:image/")):
        image = "".join(image.split())
        try:
            jpeg = base64.b64decode(image, validate=True)[:2] == b"\xff\xd8"
        except ValueError as error:
            raise ToolError(NOT_AN_IMAGE) from error
        image = f"data:image/{'jpeg' if jpeg else 'png'};base64,{image}"

    content = [
        {"type": "text", "text": "Output the JSON for this image."},
        {"type": "image_url", "image_url": {"url": image}},
    ]
    try:
        return call_agent(DEFAULT_MODEL, "vision.md", content, {}, kind="vision", timeout=settings.vision_timeout_seconds)
    except Exception as error:
        raise ToolError(describe_error(error, "read_topology", DEFAULT_MODEL)) from error


# The tools over HTTP. Clients reach the backend by its real address, not localhost, so the SDK's
# localhost-only host check is off. Its sessions run in main.py's lifespan.
http_app = mcp.streamable_http_app(
    streamable_http_path=MCP_PATH,
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


class McpEndpoint:
    """Sends requests for /mcp to the tools (with the MCP key, once one is set); everything else goes on
    to the backend's own routes."""

    def __init__(self, app: ASGIApp, key: str):
        self.app = app
        self.key = key

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["path"].rstrip("/") != MCP_PATH:
            return await self.app(scope, receive, send)

        given = dict(scope["headers"]).get(b"authorization", b"")
        if self.key and not hmac.compare_digest(given, f"Bearer {self.key}".encode()):
            response = JSONResponse({"detail": "Send the MCP key as 'Authorization: Bearer <key>'"}, status_code=401)
            return await response(scope, receive, send)

        await http_app({**scope, "path": MCP_PATH}, receive, send)


if __name__ == "__main__":
    mcp.run()
