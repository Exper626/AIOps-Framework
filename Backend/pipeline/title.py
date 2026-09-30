from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.errors import PipelineError, describe_error
from pipeline.models import DEFAULT_MODEL

# The model gets the start of a long message, and 15 seconds to answer
MESSAGE_PREVIEW = 1000
TIMEOUT_SECONDS = 15
MAX_TITLE_LENGTH = 60


class TitleReply(BaseModel):
    title: str


def write_title(message: str) -> str:
    """A short title for a new chat, from its first message, written with the default model"""
    try:
        reply = call_agent(DEFAULT_MODEL, "title.md", message[:MESSAGE_PREVIEW], {}, reply_type=TitleReply, timeout=TIMEOUT_SECONDS)
    except Exception as error:
        raise PipelineError(describe_error(error, "title")) from error

    title = " ".join(reply.title.split()).strip(" .\"'")[:MAX_TITLE_LENGTH]
    if not title:
        raise PipelineError("The model returned an empty title")

    return title
