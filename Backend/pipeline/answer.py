from collections.abc import Generator
from pathlib import Path

from pipeline.diagram import Diagram, describe_diagram
from pipeline.errors import PipelineError
from pipeline.models import ResolvedModel
from pipeline.trace import Trace
from pipeline.vision import ImageDescription
from rag.prompt import build_context

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
# The answer's instructions: text.md normally, answer.md (with the passages
# in place of {context}) when the knowledge base found something
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "text.md"
KNOWLEDGE_PROMPT_PATH = PROMPTS_DIR / "answer.md"


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


def system_prompt(passages: list[dict]) -> str:
    if passages:
        return KNOWLEDGE_PROMPT_PATH.read_text(encoding="utf-8").replace("{context}", build_context(passages)).strip()

    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip() if SYSTEM_PROMPT_PATH.exists() else ""


def build_answer_messages(
    message: str, question: str, history: list[dict], descriptions: list[ImageDescription], diagram: Diagram | None, passages: list[dict]
) -> list[dict]:
    messages = []

    prompt = system_prompt(passages)
    if prompt:
        messages.append({"role": "system", "content": prompt})

    messages.extend(history)

    if question != message:
        question = f'{question}\n\n(The user\'s exact words: "{message}")'

    if descriptions:
        question = f"{question}\n\n{describe_attachments(descriptions)}"

    if diagram:
        question = f"{question}\n\nThe user drew this network diagram:\n{describe_diagram(diagram)}"

    messages.append({"role": "user", "content": question})

    return messages


def describe_messages(messages: list[dict]) -> str:
    return "\n\n".join(
        f"System prompt ({len(m['content']):,} characters)" if m["role"] == "system" else f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
    )


def write_answer(model: ResolvedModel, messages: list[dict], trace: Trace) -> Generator[dict, None, str]:
    parts = []
    written = 0

    with trace.step("answer", model=model, input=describe_messages(messages)) as step:
        for chunk in model.client.chat.completions.create(model=model.id, messages=messages, stream=True):
            delta = chunk.choices[0].delta.content if chunk.choices else None

            if delta:
                parts.append(delta)
                written += len(delta)
                step["output"] = f"Wrote {written:,} characters"
                yield {"phase": "delta", "delta": delta}

        if not "".join(parts).strip():
            raise PipelineError("The model returned an empty answer")

    return "".join(parts)
