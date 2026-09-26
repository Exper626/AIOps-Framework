from collections.abc import Iterator
from pathlib import Path

from pipeline.errors import PipelineError
from pipeline.models import ResolvedModel
from pipeline.trace import Trace
from pipeline.vision import ImageDescription

SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "text.md"


def describe_attachments(descriptions: list[ImageDescription]) -> str:
    read = [d for d in descriptions if d.description]
    lines = []

    if read:
        lines.append(
            "The user attached network topology images. A vision model extracted this from them "
            "(JSON with each device's name, model and connections):"
        )
        lines.extend(f"Image \"{d.name}\":\n{d.description}" for d in read)

    if len(read) < len(descriptions):
        lines.append(
            "Some attached images could not be read. Tell the user you couldn't see those images "
            "and answer from the rest."
        )

    return "\n\n".join(lines)


def build_answer_messages(message: str, question: str, history: list[dict], descriptions: list[ImageDescription]) -> list[dict]:
    messages = []

    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip() if SYSTEM_PROMPT_PATH.exists() else ""
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.extend(history)

    if question != message:
        question = f'{question}\n\n(The user\'s exact words: "{message}")'

    if descriptions:
        question = f"{question}\n\n{describe_attachments(descriptions)}"

    messages.append({"role": "user", "content": question})

    return messages


def write_answer(model: ResolvedModel, messages: list[dict], trace: Trace) -> Iterator[dict]:
    parts = []

    with trace.step("answer", model=model, input=messages) as step:
        step["output"] = {"chars": 0}

        for chunk in model.client.chat.completions.create(model=model.id, messages=messages, stream=True):
            delta = chunk.choices[0].delta.content if chunk.choices else None

            if delta:
                parts.append(delta)
                step["output"]["chars"] += len(delta)
                yield {"phase": "delta", "delta": delta}

        if not "".join(parts).strip():
            raise PipelineError("The model returned an empty answer")

    yield {"phase": "done", "message": "".join(parts)}
