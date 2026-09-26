import json
from pathlib import Path

from openai import BadRequestError, UnprocessableEntityError
from pydantic import BaseModel

from config import ModelKind
from pipeline.models import ModelRef, ResolvedModel, resolve_model

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def parse_json_object(raw: str) -> dict:
    start, end = raw.find("{"), raw.rfind("}")

    if start == -1 or end <= start:
        raise ValueError("no JSON object in the reply")

    return json.loads(raw[start : end + 1])


def ask_model(model: ResolvedModel, prompt_file: str, content: str | list, step: dict, timeout: float | None) -> str:
    client = model.client.with_options(timeout=timeout, max_retries=0) if timeout else model.client
    messages = [
        {"role": "system", "content": (PROMPTS_DIR / prompt_file).read_text(encoding="utf-8")},
        {"role": "user", "content": content},
    ]

    try:
        response = client.chat.completions.create(
            model=model.id, messages=messages, temperature=0, response_format={"type": "json_object"}
        )
        step["json_mode"] = True
    except (BadRequestError, UnprocessableEntityError) as error:
        print(f"[agents] {model.id} rejected JSON mode, asking without it: {str(error)[:200]}")
        response = client.chat.completions.create(model=model.id, messages=messages, temperature=0)
        step["json_mode"] = False

    raw = (response.choices[0].message.content or "") if response.choices else ""
    step["raw_output"] = raw

    return raw


def call_agent(ref: ModelRef, prompt_file: str, content: str | list, step: dict, reply_type: type[BaseModel] | None = None, kind: ModelKind = "text", timeout: float | None = None):
    model = resolve_model(ref, kind)
    raw = ask_model(model, prompt_file, content, step, timeout)

    if reply_type is not None:
        return reply_type.model_validate(parse_json_object(raw))

    if not raw.strip():
        raise ValueError("the model returned an empty reply")

    return raw.strip()
