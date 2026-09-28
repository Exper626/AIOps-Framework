from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.diagram import Diagram
from pipeline.models import ModelRef
from pipeline.trace import Trace

# How each device type is counted: "1 switch", "6 PCs"
TYPE_NAMES = {
    "router": ("router", "routers"),
    "multilayer_switch": ("multilayer switch", "multilayer switches"),
    "switch": ("switch", "switches"),
    "firewall": ("firewall", "firewalls"),
    "access_point": ("access point", "access points"),
    "server": ("server", "servers"),
    "pc": ("PC", "PCs"),
    "laptop": ("laptop", "laptops"),
    "cloud": ("cloud", "clouds"),
}
OTHER = ("other device", "other devices")


class CaptionReply(BaseModel):
    caption: str


def count(number: int, names: tuple[str, str]) -> str:
    return f"{number} {names[0] if number == 1 else names[1]}"


def count_diagram(diagram: Diagram) -> str:
    """Counted in code so the caption doesn't have to, like "2 switches, 6 PCs and 7 cables"."""
    counts: dict[tuple[str, str], int] = {}
    for device in diagram.devices:
        names = TYPE_NAMES.get(device.type, OTHER)
        counts[names] = counts.get(names, 0) + 1

    parts = [count(number, names) for names, number in counts.items()]
    parts.append(count(len(diagram.links), ("cable", "cables")))
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def describe_connections(diagram: Diagram) -> str:
    """Each device and what it is cabled to, like "Switch17 (switch, 2950-24): Switch20, PC21"."""
    names = {device.id: device.name for device in diagram.devices}
    neighbours: dict[str, list[str]] = {device.id: [] for device in diagram.devices}
    for link in diagram.links:
        neighbours.setdefault(link.source, []).append(names.get(link.target, link.target))
        neighbours.setdefault(link.target, []).append(names.get(link.source, link.source))

    return "\n".join(
        f"{device.name} ({', '.join(part for part in (device.type, device.model) if part)}): {', '.join(neighbours[device.id]) or 'no cables'}"
        for device in diagram.devices
    )


def write_caption(ref: ModelRef, question: str, diagram: Diagram, trace: Trace) -> str:
    """One or two sentences describing the drawn diagram, for a message that only asked for a picture"""
    counts = count_diagram(diagram)
    agent_input = f"Request: {question}\nDiagram: {counts}\n{describe_connections(diagram)}"
    caption = f"A network of {counts}."

    with trace.step("caption", model=ref, input=agent_input, fallback=True) as step:
        caption = call_agent(ref, "caption.md", agent_input, step, reply_type=CaptionReply).caption.strip() or caption
        step["output"] = caption

    if "error" in step:
        step["output"] = f"Couldn't write a caption, so it gives the counts: {caption}"

    return caption
