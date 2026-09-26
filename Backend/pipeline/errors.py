from openai import APIError, APIStatusError

from pipeline.llm import AI_GATEWAY_BASE_URL


class PipelineError(Exception):
    """An error whose message can be shown to the user as it is."""


class ModelUnavailable(PipelineError):
    pass


class StepFailed(PipelineError):
    pass


GATEWAY_HINTS = {
    401: " Check that AI_GATEWAY_API_KEY on the backend is a valid AI Gateway key.",
    404: " The model id probably doesn't exist on the AI Gateway; pick another model.",
    429: " Rate or credit limit reached; wait a moment or check your AI Gateway balance.",
}

SELF_HOSTED_HINTS = {
    401: " Check SELF_HOSTED_API_KEY on the backend.",
    404: " That server doesn't serve this model any more; pick it again under Settings → Self-hosted.",
}


def describe_error(error: Exception, step: str, model=None) -> str:
    if isinstance(error, PipelineError):
        return str(error)

    if isinstance(error, APIError):
        return describe_api_error(error, model)

    if isinstance(error, ValueError):
        return f"The reply from the {step} step isn't valid: {str(error)[:500]}"

    return f"The {step} step failed: {error}"


def describe_api_error(error: APIError, model) -> str:
    model_id = model.id if model else "unknown"
    provider, base_url, hints = "The AI Gateway", AI_GATEWAY_BASE_URL, GATEWAY_HINTS

    if model is not None and model.source == "self-hosted":
        url = error.request.url
        provider, base_url, hints = "The self-hosted server", f"{url.scheme}://{url.netloc.decode()}", SELF_HOSTED_HINTS

    if isinstance(error, APIStatusError):
        body = error.body
        reason = (body.get("message") if isinstance(body, dict) else None) or str(body or error)
        hint = hints.get(error.status_code, "")
        return f"{provider} rejected the request for model '{model_id}' ({error.status_code}): {reason.rstrip('.')}.{hint}"

    return f"Could not reach {provider[0].lower() + provider[1:]} at {base_url}: {error.__cause__ or error}"
