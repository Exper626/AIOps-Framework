from typing import Literal

from pydantic import BaseModel, Field

from config import settings
from pipeline.agent import call_agent, parse_json_object
from pipeline.models import ModelRef
from pipeline.trace import Trace


class ImageInput(BaseModel):
    name: str = "image"
    media_type: Literal["image/png", "image/jpeg"]
    data_url: str = Field(pattern=r"^data:image/(png|jpeg);base64,")


class ImageDescription(BaseModel):
    name: str
    description: str | None = None
    error: str | None = None


def describe_topology(description: str) -> str:
    """One line for the trace, like "3 devices: Router0 (2621XM), Switch0 (2950-24), PC0 (PC-PT)"."""
    try:
        topology = parse_json_object(description)
    except ValueError:
        return description.strip().splitlines()[0][:200] if description.strip() else description

    devices = [
        f"{device.get('name', 'unknown')} ({device.get('model', 'unknown')})"
        for devices in topology.values()
        if isinstance(devices, list)
        for device in devices
        if isinstance(device, dict)
    ]

    return f"{len(devices)} devices: {', '.join(devices)}" if devices else description


def topology_models(description: str) -> list[str]:
    """The device models read from a topology image, to search the knowledge base with"""
    try:
        topology = parse_json_object(description)
    except ValueError:
        return []

    return [
        str(device["model"])
        for devices in topology.values()
        if isinstance(devices, list)
        for device in devices
        if isinstance(device, dict) and device.get("model") not in (None, "", "unknown")
    ]


def describe_images(ref: ModelRef, images: list[ImageInput], trace: Trace) -> list[ImageDescription]:
    results = []

    for number, image in enumerate(images, start=1):
        name = "vision description" if len(images) == 1 else f"vision description {number}"
        size_kb = round(len(image.data_url) * 3 / 4 / 1024)
        step_input = f"{image.name} ({image.media_type}, {size_kb} KB)"
        content = [
            {"type": "text", "text": "Extract the network topology from this image."},
            {"type": "image_url", "image_url": {"url": image.data_url}},
        ]

        description = None

        with trace.step(name, model=ref, input=step_input, fallback=True) as step:
            description = call_agent(ref, "vision.md", content, step, kind="vision", timeout=settings.vision_timeout_seconds)
            step["output"] = describe_topology(description)

        results.append(ImageDescription(name=image.name, description=description, error=step.get("error")))

    return results
