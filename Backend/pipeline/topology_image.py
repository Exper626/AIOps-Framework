import base64
import struct
from html import escape
from pathlib import Path

from graphviz import ExecutableNotFound, Graph

from pipeline.diagram import Device, Diagram
from pipeline.errors import PipelineError
from pipeline.trace import Trace

# One PNG per device type, made from the Cisco icons in Image Generation/icons
ICONS_DIR = Path(__file__).parent.parent / "icons"
# Icons are drawn this tall (in points); their width follows their shape
ICON_HEIGHT = 42
DPI = "150"
# Graphviz draws each cable's first device above its second, so cables run from
# the core of the network out to the end devices, and PCs end up at the bottom
LEVELS = {"cloud": 0, "router": 1, "firewall": 1, "multilayer_switch": 2, "switch": 3, "access_point": 4, "server": 4}
END_DEVICE_LEVEL = 5


def icon_path(device_type: str) -> Path:
    path = ICONS_DIR / f"{device_type}.png"
    return path if path.exists() else ICONS_DIR / "other.png"


def png_size(path: Path) -> tuple[int, int]:
    # A PNG's width and height are the two numbers after its 16-byte header
    return struct.unpack(">II", path.read_bytes()[16:24])


def device_label(device: Device) -> str:
    """The icon with the name underneath, and the model under that in grey"""
    icon = icon_path(device.type)
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

    levels = {device.id: LEVELS.get(device.type, END_DEVICE_LEVEL) for device in diagram.devices}

    for device in diagram.devices:
        graph.node(device.id, label=device_label(device))
    for link in diagram.links:
        top, bottom = sorted((link.source, link.target), key=lambda device_id: levels.get(device_id, END_DEVICE_LEVEL))
        graph.edge(top, bottom)

    return graph


def draw_topology_image(diagram: Diagram, trace: Trace) -> str | None:
    """The diagram drawn with Graphviz, as a PNG data URL, or None if it couldn't be drawn"""
    image = None

    with trace.step("graphviz", input=f"{len(diagram.devices)} devices, {len(diagram.links)} cables", fallback=True) as step:
        graph = build_graph(diagram)
        step["raw_output"] = graph.source

        try:
            png = graph.pipe()
        except ExecutableNotFound as error:
            raise PipelineError("Graphviz isn't installed where the backend runs: install it (graphviz.org/download) and restart") from error

        image = "data:image/png;base64," + base64.b64encode(png).decode()
        step["output"] = f"Drew the diagram: {len(png) // 1024} KB image"

    return image
