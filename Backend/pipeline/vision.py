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
    try:
        topology = parse_json_object(description)
    except ValueError:
        return description

    lines = [
        f"{device.get('name', 'unknown')} ({device.get('model', 'unknown')}): "
        f"connected to {', '.join(map(str, device.get('connected_to') or [])) or 'nothing'}"
        for devices in topology.values()
        if isinstance(devices, list)
        for device in devices
        if isinstance(device, dict)
    ]

    return f"Found {len(lines)} devices:\n" + "\n".join(lines) if lines else description


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
