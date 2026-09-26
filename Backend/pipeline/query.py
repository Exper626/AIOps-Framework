from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace


class QueryReply(BaseModel):
    standalone_question: str | None


def format_conversation(history: list[dict]) -> str:
    return "\n".join(f"{m['role']}: {m['content']}" for m in history) or "(no earlier messages)"


def run_query(ref: ModelRef, message: str, history: list[dict], trace: Trace, enabled: bool = True) -> str:
    if not enabled:
        with trace.step("query") as step:
            step["skipped"] = "Turned off in Settings → Agents"
            step["output"] = {"standalone_question": message, "rewritten": False}
        return message

    agent_input = f"Conversation:\n{format_conversation(history)}\nNew message: {message}"
    question = message

    with trace.step("query", model=ref, input=agent_input, fallback=True) as step:
        reply = call_agent(ref, "query.md", agent_input, step, reply_type=QueryReply)
        question = (reply.standalone_question or "").strip() or message

    step["output"] = {"standalone_question": question, "rewritten": question != message}

    return question
