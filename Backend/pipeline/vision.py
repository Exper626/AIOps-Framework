from typing import Literal

from pydantic import BaseModel, Field

from config import settings
from pipeline.agent import call_agent, parse_json_object
from pipeline.models import ModelRef
from pipeline.trace import Trace, plural


class ImageInput(BaseModel):
    name: str = "image"
    media_type: Literal["image/png", "image/jpeg"]
    data_url: str = Field(pattern=r"^data:image/(png|jpeg);base64,")


class ImageDescription(BaseModel):
    name: str
    description: str | None = None


def read_topology(description: str) -> dict:
    """The vision model's JSON: {"devices": [...], "links": [...]}, and a "description" for other images"""
    try:
        topology = parse_json_object(description)
    except ValueError:
        return {}
    return topology if isinstance(topology, dict) else {}


def describe_topology(description: str) -> str:
    """One line for the trace, like "3 devices, 2 cables: Router0 (2621XM), Switch0 (2950-24), PC0 (PC-PT)"."""
    topology = read_topology(description)
    devices = [d for d in topology.get("devices") or [] if isinstance(d, dict)]

    if devices:
        names = ", ".join(f"{d.get('name', 'unknown')} ({d.get('model', 'unknown')})" for d in devices)
        return f"{plural(len(devices), 'device')}, {plural(len(topology.get('links') or []), 'cable')}: {names}"

    text = str(topology.get("description") or description).strip()
    return text.splitlines()[0][:200] if text else text


def topology_models(description: str) -> list[str]:
    """The device models read from a topology image, to search the knowledge base with"""
    return [
        str(d["model"])
        for d in read_topology(description).get("devices") or []
        if isinstance(d, dict) and d.get("model") not in (None, "", "unknown")
    ]


def describe_images(ref: ModelRef, images: list[ImageInput], trace: Trace) -> list[ImageDescription]:
    results = []

    for number, image in enumerate(images, start=1):
        name = "vision description" if len(images) == 1 else f"vision description {number}"
        size_kb = round(len(image.data_url) * 3 / 4 / 1024)
        step_input = f"{image.name} ({image.media_type}, {size_kb} KB)"
        content = [
            {"type": "text", "text": "Output the JSON for this image."},
            {"type": "image_url", "image_url": {"url": image.data_url}},
        ]

        description = None

        with trace.step(name, model=ref, input=step_input, fallback=True) as step:
            description = call_agent(ref, "vision.md", content, step, kind="vision", timeout=settings.vision_timeout_seconds)
            step["output"] = describe_topology(description)

        results.append(ImageDescription(name=image.name, description=description))

    return results
