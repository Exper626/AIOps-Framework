from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace


class ContextReply(BaseModel):
    history: list[int]


def group_exchanges(history: list[dict]) -> list[list[dict]]:
    exchanges = []

    for m in history:
        if m["role"] == "user" or not exchanges:
            exchanges.append([m])
        else:
            exchanges[-1].append(m)

    return exchanges


def format_exchanges(exchanges: list[list[dict]]) -> str:
    return "\n\n".join(
        f"Exchange {number}\n" + "\n".join(f"{m['role']}: {m['content']}" for m in exchange)
        for number, exchange in enumerate(exchanges, start=1)
    )


def context_runs(enabled: bool, history: list[dict]) -> bool:
    return enabled and bool(history)


def run_context(ref: ModelRef, question: str, history: list[dict], trace: Trace, enabled: bool = True) -> list[dict]:
    exchanges = group_exchanges(history)
    everything = list(range(1, len(exchanges) + 1))

    if not context_runs(enabled, history):
        with trace.step("context management") as step:
            step["skipped"] = "Turned off in Settings → Agents" if not enabled else "No earlier messages yet"
            step["output"] = {"history": everything}
        return history

    agent_input = f"Conversation:\n{format_exchanges(exchanges)}\n\nQuestion: {question}"

    selected = everything

    with trace.step("context management", model=ref, input=agent_input, fallback=True) as step:
        reply = call_agent(ref, "context_management.md", agent_input, step, reply_type=ContextReply)
        selected = sorted({n for n in reply.history if 1 <= n <= len(exchanges)})

    step["output"] = {"history": selected}

    return [m for number in selected for m in exchanges[number - 1]]
