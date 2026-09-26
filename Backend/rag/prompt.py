from pathlib import Path


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_context(chunks: list[dict]) -> str:
    sources = []

    for index, chunk in enumerate(chunks, start=1):
        device = " / ".join(part for part in (chunk.get("vendor"), chunk.get("device_type"), chunk.get("subcategory")) if part)

        sources.append(
            "\n".join(
                [
                    f"SOURCE {index}",
                    f"Device: {device}",
                    f"File: {chunk.get('filename') or ''}",
                    f"URL: {chunk.get('source_url') or ''}",
                    "Content:",
                    (chunk.get("text") or "").strip(),
                ]
            ).strip()
        )

    return "\n\n".join(sources)


def build_messages(question: str, context: str) -> list[dict]:
    system_prompt = (PROMPTS_DIR / "answer.md").read_text(encoding="utf-8").replace("{context}", context)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]
