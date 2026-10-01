"""The models running in your Modal workspace, found with MODAL_TOKEN_ID and MODAL_TOKEN_SECRET, so a model
deployed there shows up in Settings without adding its address to SELF_HOSTED_SERVERS: Modal's Endpoints
(models Modal hosts for you, like GLM or DeepSeek) and the Servers of your deployed Apps (models you deploy
yourself, like Model Hosting/networking_model.py). An App tagged with its model's name (tags={"model": ...})
is listed by that name without waking it up; the others are asked for their models.

Modal's SDK has no documented function for listing them, so this asks the way `modal endpoint list` and
`modal app info` do (modal is pinned in requirements.txt for that reason), then gets each one's URL with
modal.Server.get_url()."""

import asyncio
import time

from modal._utils.async_utils import synchronizer
from modal._server import _Server
from modal.client import _Client
from modal_proto import api_pb2

from config import ModelKind, SelfHostedServer, settings

# Models are looked up again at most once a minute, and Modal gets 15 seconds to answer; a failed lookup
# is also remembered for a minute, so a slow Modal doesn't hold up every request
CACHE_SECONDS = 60
TIMEOUT_SECONDS = 15
# Modal doesn't say which models can read images, and most can now, so every model is offered for image
# description too; a text-only model picked for Vision fails with its server's reason
KINDS: list[ModelKind] = ["text", "vision"]
STOPPED = (api_pb2.APP_STATE_STOPPING, api_pb2.APP_STATE_STOPPED)
# The App tags that name its model and say it can't read images
MODEL_TAG = "model"
NO_IMAGES_TAG = "reads-images"

_client: _Client | None = None
# When Modal was last asked, and the servers it gave or the error
_found: tuple[float, list[SelfHostedServer] | Exception] | None = None


@synchronizer.create_blocking
async def list_model_servers() -> list[SelfHostedServer]:
    """Each Endpoint that isn't stopped and each Server of a deployed App"""
    try:
        return await asyncio.wait_for(ask_modal(), timeout=TIMEOUT_SECONDS)
    except TimeoutError as error:
        raise RuntimeError(f"Modal didn't answer within {TIMEOUT_SECONDS} seconds") from error


async def ask_modal() -> list[SelfHostedServer]:
    global _client
    if _client is None:
        _client = await _Client.from_credentials(settings.modal_token_id, settings.modal_token_secret)

    endpoints, app_servers = await asyncio.gather(endpoint_functions(_client), app_server_functions(_client))
    found = [(function_id, {}) for function_id in endpoints] + app_servers
    urls = await asyncio.gather(*(_Server.from_id(function_id, client=_client).get_url() for function_id, _ in found))

    # An Endpoint can also be listed as an App's Server; each address is listed once
    servers: dict[str, SelfHostedServer] = {}
    for url, (_, tags) in zip(urls, found, strict=True):
        if url and url not in servers:
            servers[url] = SelfHostedServer(
                base_url=f"{url.rstrip('/')}/v1",
                kinds=["text"] if tags.get(NO_IMAGES_TAG) == "no" else KINDS,
                models=[tags[MODEL_TAG]] if tags.get(MODEL_TAG) else [],
            )
    return list(servers.values())


async def endpoint_functions(client: _Client) -> list[str]:
    request = api_pb2.EndpointListRequest(
        environment_name=settings.modal_environment,
        pagination=api_pb2.ListPagination(max_objects=100, created_before=time.time()),
    )
    response = await client._stub.EndpointList(request)
    return [item.function_id for item in response.items if item.app_state not in STOPPED and item.function_id]


async def app_server_functions(client: _Client) -> list[tuple[str, dict[str, str]]]:
    """Each Server of a deployed App, with the App's tags"""
    response = await client._stub.AppList(api_pb2.AppListRequest(environment_name=settings.modal_environment))
    deployed = [app.app_id for app in response.apps if app.state == api_pb2.APP_STATE_DEPLOYED]

    async def servers_of(app_id: str) -> list[tuple[str, dict[str, str]]]:
        info, tags = await asyncio.gather(
            client._stub.AppGetInfo(api_pb2.AppGetInfoRequest(app_id=app_id)),
            client._stub.AppGetTags(api_pb2.AppGetTagsRequest(app_id=app_id)),
        )
        return [(function_id, dict(tags.tags)) for function_id in info.info.servers.values()]

    apps = await asyncio.gather(*(servers_of(app_id) for app_id in deployed))
    return [server for servers in apps for server in servers]


def modal_servers() -> list[SelfHostedServer]:
    """The Modal models as self-hosted servers (their OpenAI-compatible API is under /v1), or none
    when no Modal token is set. Raises when Modal can't be asked."""
    global _found

    if not (settings.modal_token_id and settings.modal_token_secret):
        return []

    if not (_found and time.monotonic() - _found[0] < CACHE_SECONDS):
        try:
            _found = (
                time.monotonic(),
                list_model_servers(),
            )
        except Exception as error:
            _found = (time.monotonic(), error)

    if isinstance(_found[1], Exception):
        raise _found[1]
    return _found[1]
