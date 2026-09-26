from pydantic import BaseModel, Field

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace


class Device(BaseModel):
    id: str = Field(min_length=1)
    name: str
    type: str = "router"
    model: str = ""
    x: float | None = None
    y: float | None = None


class Link(BaseModel):
    source: str
    target: str


class Diagram(BaseModel):
    devices: list[Device] = []
    links: list[Link] = []


class DiagramDevice(BaseModel):
    name: str = Field(min_length=1)
    type: str = "router"
    model: str = ""


class DiagramLink(BaseModel):
    source: str = Field(alias="from")
    target: str = Field(alias="to")


class DiagramContent(BaseModel):
    devices: list[DiagramDevice] = []
    links: list[DiagramLink] = []


class DiagramReply(BaseModel):
    diagram: DiagramContent | None


def to_diagram(content: DiagramContent) -> Diagram | None:
    devices = {d.name: Device(id=d.name, name=d.name, type=d.type, model=d.model) for d in content.devices}
    links = {
        tuple(sorted((link.source, link.target)))
        for link in content.links
        if link.source in devices and link.target in devices and link.source != link.target
    }

    if not devices:
        return None

    return Diagram(devices=list(devices.values()), links=[Link(source=a, target=b) for a, b in sorted(links)])


def describe_diagram(diagram: Diagram) -> str:
    names = {d.id: d.name for d in diagram.devices}
    devices = ", ".join(f"{d.name} ({d.type}{', ' + d.model if d.model else ''})" for d in diagram.devices)
    links = ", ".join(f"{names.get(l.source, l.source)} – {names.get(l.target, l.target)}" for l in diagram.links)
    return f"Devices: {devices}\nLinks: {links or 'none'}"


def keep_positions(diagram: Diagram, before: Diagram) -> None:
    positions = {d.name: (d.x, d.y) for d in before.devices}

    for device in diagram.devices:
        device.x, device.y = positions.get(device.name, (None, None))


def run_diagram(
    ref: ModelRef, question: str, answer: str, images: list[str], drawn: Diagram | None, earlier: Diagram | None, trace: Trace
) -> Diagram | None:
    agent_input = f"Question: {question}\n\nAnswer: {answer}"
    attached = images + ([describe_diagram(drawn)] if drawn else [])

    if attached:
        agent_input += "\n\nTopology the user attached:\n" + "\n\n".join(attached)

    if earlier:
        agent_input += f"\n\nDiagram from earlier in the conversation:\n{describe_diagram(earlier)}"

    diagram = None

    with trace.step("diagram", model=ref, input=agent_input, fallback=True) as step:
        reply = call_agent(ref, "diagram.md", agent_input, step, reply_type=DiagramReply)
        diagram = to_diagram(reply.diagram) if reply.diagram else None

    if diagram:
        step["output"] = f"Drew a diagram: {len(diagram.devices)} devices, {len(diagram.links)} cables"
    elif "error" not in step:
        step["output"] = "No diagram needed"

    if diagram and (drawn or earlier):
        keep_positions(diagram, drawn or earlier)

    return diagram
