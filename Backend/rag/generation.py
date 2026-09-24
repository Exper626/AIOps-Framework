import os

from openai import OpenAI


AI_GATEWAY_BASE_URL = os.getenv(
    "AI_GATEWAY_BASE_URL",
    "https://ai-gateway.vercel.sh/v1",
)


def generate_answer(messages: list[dict], model: str) -> str:
    api_key = os.getenv("AI_GATEWAY_API_KEY")

    if not api_key:
        raise RuntimeError("AI_GATEWAY_API_KEY is not set")

    if not model.strip():
        raise ValueError("Model cannot be empty")

    client = OpenAI(
        api_key=api_key,
        base_url=AI_GATEWAY_BASE_URL,
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    if not response.choices:
        raise RuntimeError("AI Gateway returned no choices")

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("Generation model returned an empty answer")

    return answer.strip()
