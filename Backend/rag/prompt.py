from pathlib import Path


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_context(chunks: list[dict]) -> str:
    sources = []

    for index, chunk in enumerate(chunks, start=1):
        # Entries loaded before the device metadata have "subcategory" and "filename" instead
        labels = [chunk.get("vendor"), chunk.get("device_type"), *(chunk.get("tags") or [chunk.get("subcategory")])]

        sources.append(
            "\n".join(
                [
                    f"SOURCE {index}",
                    f"Device: {chunk.get('device') or chunk.get('filename') or ''}",
                    f"Type: {' / '.join(label for label in labels if label)}",
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
