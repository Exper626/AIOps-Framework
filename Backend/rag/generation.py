from pipeline.llm import gateway_client


def generate_answer(messages: list[dict], model: str) -> str:
    if not model.strip():
        raise ValueError("Model cannot be empty")

    response = gateway_client.chat.completions.create(model=model, messages=messages)

    if not response.choices:
        raise RuntimeError("AI Gateway returned no choices")

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("Generation model returned an empty answer")

    return answer.strip()
