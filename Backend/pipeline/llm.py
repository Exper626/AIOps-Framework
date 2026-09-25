import os

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

AI_GATEWAY_BASE_URL = os.getenv("AI_GATEWAY_BASE_URL", "https://ai-gateway.vercel.sh/v1")

# Added to the provider's own error message so it says what to fix
LLM_ERROR_HINTS = {
    401: " Check that AI_GATEWAY_API_KEY on the backend is a valid AI Gateway key.",
    404: " The model id probably doesn't exist on the AI Gateway; pick another model.",
    429: " Rate or credit limit reached; wait a moment or check your AI Gateway balance.",
}

SELF_HOSTED_ERROR_HINTS = {
    401: " Check SELF_HOSTED_API_KEY on the backend.",
    404: " The model id probably doesn't exist on that server; check SELF_HOSTED_MODELS on the backend.",
}


def create_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=AI_GATEWAY_BASE_URL)


def describe_llm_error(
    error: Exception,
    model: str,
    *,
    provider: str = "The AI Gateway",
    base_url: str = AI_GATEWAY_BASE_URL,
    hints: dict[int, str] = LLM_ERROR_HINTS,
) -> str:
    """Turn a model provider failure into a message that says what to fix."""
    if isinstance(error, APITimeoutError):
        return f"{provider} did not answer in time for model '{model}'. Try again or pick a faster model."

    if isinstance(error, APIConnectionError):
        return f"Could not reach {provider[0].lower() + provider[1:]} at {base_url}: {error.__cause__ or error}"

    if isinstance(error, APIStatusError):
        body = error.body
        reason = (body.get("message") if isinstance(body, dict) else None) or str(body or error)
        hint = hints.get(error.status_code, "")
        return f"{provider} rejected the request for model '{model}' ({error.status_code}): {reason.rstrip('.')}.{hint}"

    return f"LLM call failed: {error}"
