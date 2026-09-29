"""The endpoints running in your Modal workspace, found with MODAL_TOKEN_ID and MODAL_TOKEN_SECRET, so a model
deployed there shows up in Settings without adding its address to SELF_HOSTED_SERVERS.

Modal's SDK has no documented function for listing endpoints, so this asks the way `modal endpoint list` does
(modal is pinned in requirements.txt for that reason), then gets each one's URL with modal.Server.get_url()."""

import asyncio
import re
import time

from modal._utils.async_utils import synchronizer
from modal._server import _Server
from modal.client import _Client
from modal_proto import api_pb2

from config import SelfHostedServer, settings

# Endpoints are looked up again at most once a minute, and Modal gets 15 seconds to answer; a failed lookup
# is also remembered for a minute, so a slow Modal doesn't hold up every request
CACHE_SECONDS = 60
TIMEOUT_SECONDS = 15
# An endpoint named like a vision model (qwen2-5-vl-7b, llama-vision) is offered for image description too
VISION_NAME = re.compile(r"(^|[-_.])(vl|vision)([-_.]|$)", re.IGNORECASE)
STOPPED = (api_pb2.APP_STATE_STOPPING, api_pb2.APP_STATE_STOPPED)

_client: _Client | None = None
# When Modal was last asked, and the servers it gave or the error
_found: tuple[float, list[SelfHostedServer] | Exception] | None = None


@synchronizer.create_blocking
async def list_endpoints() -> list[tuple[str, str]]:
    """The name and URL of each endpoint that isn't stopped"""
    try:
        return await asyncio.wait_for(ask_modal(), timeout=TIMEOUT_SECONDS)
    except TimeoutError as error:
        raise RuntimeError(f"Modal didn't answer within {TIMEOUT_SECONDS} seconds") from error


async def ask_modal() -> list[tuple[str, str]]:
    global _client
    if _client is None:
        _client = await _Client.from_credentials(settings.modal_token_id, settings.modal_token_secret)

    request = api_pb2.EndpointListRequest(
        environment_name=settings.modal_environment,
        pagination=api_pb2.ListPagination(max_objects=100, created_before=time.time()),
    )
    response = await _client._stub.EndpointList(request)

    endpoints = []
    for item in response.items:
        if item.app_state in STOPPED or not item.function_id:
            continue
        url = await _Server.from_id(item.function_id, client=_client).get_url()
        if url:
            endpoints.append((item.name, url))

    return endpoints


def modal_servers() -> list[SelfHostedServer]:
    """The Modal endpoints as self-hosted servers (their OpenAI-compatible API is under /v1), or none
    when no Modal token is set. Raises when Modal can't be asked."""
    global _found

    if not (settings.modal_token_id and settings.modal_token_secret):
        return []

    if not (_found and time.monotonic() - _found[0] < CACHE_SECONDS):
        try:
            _found = (
                time.monotonic(),
                [
                    SelfHostedServer(
                        base_url=f"{url.rstrip('/')}/v1", kinds=["text", "vision"] if VISION_NAME.search(name) else ["text"]
                    )
                    for name, url in list_endpoints()
                ],
            )
        except Exception as error:
            _found = (time.monotonic(), error)

    if isinstance(_found[1], Exception):
        raise _found[1]
    return _found[1]
