"""Vision description: reads attached topology images with prompts/vision.md.

The vision model turns each image into a JSON description of the devices and cables,
which the answer model then gets together with the question.
"""

import json
import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from pipeline.agents import PROMPTS_DIR, describe_agent_error
from pipeline.models import ModelRef, resolve_model
from pipeline.trace import Trace

# Used when the frontend doesn't say which vision model to use
VISION_MODEL = os.getenv("VISION_MODEL", "google/gemini-2.5-flash")
# Reading a diagram takes longer than the small agents, but the whole answer must
# still fit in the frontend's 60 seconds
VISION_TIMEOUT_SECONDS = float(os.getenv("VISION_TIMEOUT_SECONDS", "40"))


class ImageInput(BaseModel):
    name: str = "image"
    media_type: Literal["image/png", "image/jpeg"]
    # The image itself, as a base64 data URL ("data:image/png;base64,...")
    data_url: str = Field(pattern=r"^data:image/(png|jpeg);base64,")


class ImageDescription(BaseModel):
    name: str
    description: str | None = None
    error: str | None = None


def describe_images(
    ref: ModelRef, gateway_client: OpenAI | None, images: list[ImageInput], trace: Trace
) -> list[ImageDescription]:
    """One vision call per image, since the prompt is written for a single diagram."""
    prompt = (PROMPTS_DIR / "vision.md").read_text(encoding="utf-8")
    results = []

    for number, image in enumerate(images, start=1):
        name = "vision description" if len(images) == 1 else f"vision description {number}"
        # The trace shows which image was read, not the image data itself
        size_kb = round(len(image.data_url) * 3 / 4 / 1024)
        step_input = {"prompt": "prompts/vision.md", "image": f"{image.name} ({image.media_type}, {size_kb} KB)"}

        with trace.step(name, model=ref.id, input=step_input) as step:
            step["source"] = ref.source
            model = None

            try:
                model = resolve_model(ref, "vision", gateway_client)
                response = model.client.with_options(
                    timeout=VISION_TIMEOUT_SECONDS, max_retries=0
                ).chat.completions.create(
                    model=model.id,
                    messages=[
                        {"role": "system", "content": prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Extract the network topology from this image."},
                                {"type": "image_url", "image_url": {"url": image.data_url}},
                            ],
                        },
                    ],
                    temperature=0,
                )
                raw = (response.choices[0].message.content or "") if response.choices else ""
                step["raw_output"] = raw

                if not raw.strip():
                    raise ValueError("the model returned an empty description")

                description, is_json = compact_json(raw)
                step["output"] = {"valid_json": is_json, "chars": len(description)}
                results.append(ImageDescription(name=image.name, description=description))
            except Exception as error:
                step["error"] = describe_agent_error("vision", error, ref, model)
                print(f"[vision] {step['error']}")
                results.append(ImageDescription(name=image.name, error=step["error"]))

    return results


def compact_json(raw: str) -> tuple[str, bool]:
    """The topology as compact JSON when the reply is JSON (possibly in code fences), else as sent."""
    text = raw.strip()
    start, end = text.find("{"), text.rfind("}")

    if start != -1 and end > start:
        try:
            return json.dumps(json.loads(text[start : end + 1]), separators=(",", ":")), True
        except ValueError:
            pass

    return text, False
