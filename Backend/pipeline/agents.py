"""The small agents that prepare a message before the answer model sees it.

1. Query agent: rewrites the message as a standalone question and splits it into sub-questions.
2. Context management agent: decides which context each sub-question needs.

Each one uses the model picked for it in Settings and asks for JSON mode, so the reply is
valid JSON. If an agent fails, is slow or still returns bad JSON, it falls back to what the
chat did without it, so the answer still comes.
"""

import json
import os
from pathlib import Path

from openai import APIError, BadRequestError, OpenAI, UnprocessableEntityError
from pydantic import BaseModel, Field

from pipeline.llm import describe_llm_error
from pipeline.models import ModelRef, ModelUnavailable, ResolvedModel, resolve_model
from pipeline.trace import Trace

# Used when the frontend doesn't say which model to use. These steps only rewrite
# and route the question, so a small, fast model is enough.
QUERY_MODEL = os.getenv("QUERY_MODEL", "xai/grok-4.1-fast-non-reasoning")
CONTEXT_MODEL = os.getenv("CONTEXT_MODEL", "xai/grok-4.1-fast-non-reasoning")
AGENT_TIMEOUT_SECONDS = float(os.getenv("AGENT_TIMEOUT_SECONDS", "8"))

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
MAX_SUB_QUESTIONS = 5
HISTORY_FOR_AGENTS = 6  # most recent messages the agents see
HISTORY_CHARS = 500  # per message, to keep the agent calls small and fast

# Context the pipeline knows how to add; anything else an agent asks for is ignored
KNOWN_NEEDS = {"history"}


class SubQuestion(BaseModel):
    question: str
    needs: list[str] = []


class Plan(BaseModel):
    """What the answer model gets asked: the rewritten question, its parts and their context."""

    standalone_question: str
    sub_questions: list[SubQuestion]

    @property
    def needs_history(self) -> bool:
        return any("history" in sub.needs for sub in self.sub_questions)


class QueryReply(BaseModel):
    standalone_question: str = Field(min_length=1)
    sub_questions: list[str] = Field(min_length=1)


class ContextNeed(BaseModel):
    number: int
    needs: list[str] = []


class ContextReply(BaseModel):
    sub_questions: list[ContextNeed]


def format_conversation(history: list[dict]) -> str:
    recent = history[-HISTORY_FOR_AGENTS:]
    return "\n".join(f"{m['role']}: {m['content'][:HISTORY_CHARS]}" for m in recent) or "(no earlier messages)"


def parse_json_object(raw: str) -> dict:
    """Small models sometimes wrap the JSON in code fences or add a sentence around it."""
    start, end = raw.find("{"), raw.rfind("}")

    if start == -1 or end <= start:
        raise ValueError("no JSON object in the reply")

    return json.loads(raw[start : end + 1])


def ask_agent(model: ResolvedModel, prompt_file: str, agent_input: str, step: dict) -> dict:
    """One small-model call that must reply with a JSON object."""
    client = model.client.with_options(timeout=AGENT_TIMEOUT_SECONDS, max_retries=0)
    messages = [
        {"role": "system", "content": (PROMPTS_DIR / prompt_file).read_text(encoding="utf-8")},
        {"role": "user", "content": agent_input},
    ]

    try:
        # JSON mode: the server only lets the model write valid JSON
        response = client.chat.completions.create(
            model=model.id, messages=messages, temperature=0, response_format={"type": "json_object"}
        )
        step["json_mode"] = True
    except (BadRequestError, UnprocessableEntityError) as error:
        # Not every model or server supports JSON mode, so it asks again without it
        print(f"[agents] {model.id} rejected JSON mode, asking without it: {str(error)[:200]}")
        response = client.chat.completions.create(model=model.id, messages=messages, temperature=0)
        step["json_mode"] = False

    raw = (response.choices[0].message.content or "") if response.choices else ""
    step["raw_output"] = raw

    return parse_json_object(raw)


def describe_agent_error(agent: str, error: Exception, ref: ModelRef, model: ResolvedModel | None) -> str:
    if isinstance(error, ModelUnavailable):
        return str(error)

    if isinstance(error, APIError):
        return describe_llm_error(error, ref.id, **(model.error_context if model else {}))

    if isinstance(error, ValueError):
        # Covers broken JSON and JSON in the wrong shape
        return f"The {agent} agent's reply isn't valid: {str(error)[:500]}"

    return f"The {agent} agent failed: {error}"


def run_query_agent(
    ref: ModelRef,
    gateway_client: OpenAI | None,
    message: str,
    history: list[dict],
    trace: Trace,
    enabled: bool = True,
) -> QueryReply:
    """Rewrite the message and split it into sub-questions."""
    unchanged = QueryReply(standalone_question=message, sub_questions=[message])

    if not enabled:
        with trace.step("query") as step:
            step["skipped"] = "Turned off in Settings → Agents"
            step["output"] = unchanged.model_dump()
        return unchanged

    agent_input = f"Conversation:\n{format_conversation(history)}\nNew message: {message}"

    with trace.step("query", model=ref.id, input=agent_input) as step:
        step["source"] = ref.source
        model = None

        try:
            model = resolve_model(ref, "text", gateway_client)
            reply = QueryReply.model_validate(ask_agent(model, "query.md", agent_input, step))
            sub_questions = [q.strip() for q in reply.sub_questions if q.strip()][:MAX_SUB_QUESTIONS]

            if not sub_questions:
                raise ValueError("the reply has no sub-questions")

            result = QueryReply(standalone_question=reply.standalone_question.strip(), sub_questions=sub_questions)
        except Exception as error:
            step["error"] = describe_agent_error("query", error, ref, model)
            step["fallback"] = True
            print(f"[query] {step['error']} (using the message as-is)")
            result = unchanged

        step["output"] = result.model_dump()

    return result


def context_agent_runs(enabled: bool, history: list[dict]) -> bool:
    # Without earlier messages there is nothing the questions could depend on
    return enabled and bool(history)


def run_context_agent(
    ref: ModelRef,
    gateway_client: OpenAI | None,
    sub_questions: list[str],
    history: list[dict],
    trace: Trace,
    enabled: bool = True,
) -> list[list[str]]:
    """For each sub-question, the context it needs (currently only "history")."""
    with_history = [["history"] for _ in sub_questions]  # what the chat did before this agent
    without_context = [[] for _ in sub_questions]

    if not context_agent_runs(enabled, history):
        with trace.step("context management") as step:
            step["skipped"] = "Turned off in Settings → Agents" if not enabled else "No earlier messages yet"
            needs = with_history if not enabled else without_context
            step["output"] = [{"question": q, "needs": n} for q, n in zip(sub_questions, needs)]
        return needs

    numbered = "\n".join(f"{i}. {q}" for i, q in enumerate(sub_questions, start=1))
    agent_input = f"Conversation:\n{format_conversation(history)}\nQuestions:\n{numbered}"

    with trace.step("context management", model=ref.id, input=agent_input) as step:
        step["source"] = ref.source
        model = None

        try:
            model = resolve_model(ref, "text", gateway_client)
            reply = ContextReply.model_validate(ask_agent(model, "context_management.md", agent_input, step))
            needs = [[] for _ in sub_questions]

            for item in reply.sub_questions:
                if 1 <= item.number <= len(sub_questions):
                    needs[item.number - 1] = [need for need in item.needs if need in KNOWN_NEEDS]
        except Exception as error:
            step["error"] = describe_agent_error("context management", error, ref, model)
            step["fallback"] = True
            print(f"[context] {step['error']} (sending the whole conversation)")
            needs = with_history

        step["output"] = [{"question": q, "needs": n} for q, n in zip(sub_questions, needs)]

    return needs


def build_plan(query: QueryReply, needs: list[list[str]]) -> Plan:
    return Plan(
        standalone_question=query.standalone_question,
        sub_questions=[SubQuestion(question=q, needs=n) for q, n in zip(query.sub_questions, needs)],
    )
