import base64
import os
import shutil
import struct
from html import escape
from pathlib import Path

from graphviz import ExecutableNotFound, Graph

from pipeline.devices import device_kind
from pipeline.diagram import Device, Diagram
from pipeline.errors import PipelineError
from pipeline.trace import Trace, plural

# One PNG per icon in Frontend/lib/network-icons.json, made from the Cisco icons in Image Generation/icons
# by Frontend/scripts/build-network-icons.mjs
ICONS_DIR = Path(__file__).parent.parent / "icons"
# Icons are drawn this tall (in points); their width follows their shape
ICON_HEIGHT = 42
DPI = "150"

# Graphviz's Windows installer leaves it off PATH unless you tick that option
WINDOWS_GRAPHVIZ = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Graphviz" / "bin"
if os.name == "nt" and not shutil.which("dot") and WINDOWS_GRAPHVIZ.is_dir():
    os.environ["PATH"] += os.pathsep + str(WINDOWS_GRAPHVIZ)

ICONS = {path.stem for path in ICONS_DIR.glob("*.png")}


def icon_path(device: Device) -> Path:
    """The icon picked for the device, or else its kind's"""
    return ICONS_DIR / f"{device.icon if device.icon in ICONS else device_kind(device.type).icon}.png"


def png_size(path: Path) -> tuple[int, int]:
    # A PNG's width and height are the two numbers after its 16-byte header
    return struct.unpack(">II", path.read_bytes()[16:24])


def device_label(device: Device) -> str:
    """The icon with the name underneath, and the model under that in grey"""
    icon = icon_path(device)
    width, height = png_size(icon)
    model = f'<TR><TD><FONT POINT-SIZE="9" COLOR="#666666">{escape(device.model)}</FONT></TD></TR>' if device.model else ""

    return (
        '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
        f'<TR><TD FIXEDSIZE="TRUE" WIDTH="{round(ICON_HEIGHT * width / height)}" HEIGHT="{ICON_HEIGHT}">'
        f'<IMG SRC="{icon.as_posix()}" SCALE="TRUE"/></TD></TR>'
        f'<TR><TD><FONT POINT-SIZE="11">{escape(device.name)}</FONT></TD></TR>'
        f"{model}</TABLE>>"
    )


def build_graph(diagram: Diagram) -> Graph:
    graph = Graph("topology", format="png")
    graph.attr(rankdir="TB", dpi=DPI, bgcolor="white", pad="0.3", nodesep="0.35", ranksep="0.7")
    graph.attr("node", shape="none", margin="0", fontname="Helvetica")
    graph.attr("edge", color="#333333", penwidth="1.4")

    # Graphviz draws each cable's first device above its second, so cables run from the core of the
    # network out to the end devices, and PCs end up at the bottom
    levels = {device.id: device_kind(device.type).level for device in diagram.devices}

    for device in diagram.devices:
        graph.node(device.id, label=device_label(device))
    for link in diagram.links:
        top, bottom = sorted((link.source, link.target), key=lambda device_id: levels.get(device_id, 99))
        graph.edge(top, bottom)

    return graph


def render_png(graph: Graph) -> bytes:
    try:
        return graph.pipe()
    except ExecutableNotFound as error:
        raise PipelineError("Graphviz isn't installed where the backend runs: install it (graphviz.org/download) and restart") from error


def to_data_url(png: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png).decode()


def draw_topology_image(diagram: Diagram, trace: Trace) -> str | None:
    """The diagram drawn with Graphviz, as a PNG data URL, or None if it couldn't be drawn"""
    image = None

    with trace.step("graphviz", input=f"{plural(len(diagram.devices), 'device')}, {plural(len(diagram.links), 'cable')}", fallback=True) as step:
        graph = build_graph(diagram)
        step["raw_output"] = graph.source

        png = render_png(graph)
        image = to_data_url(png)
        step["output"] = f"Drew the diagram: {len(png) // 1024} KB image"

    if "error" in step:
        step["output"] = f"Couldn't draw the picture, so the chat shows an editable diagram instead: {step['error']}"

    return image
