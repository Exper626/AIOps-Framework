from typing import Literal

from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace

RECENT_MESSAGES = 4
# Earlier answers can be long; the start is enough to follow the conversation
MESSAGE_PREVIEW = 600

Task = Literal["image_description", "retrieval", "text_generation", "image_generation"]

# The tasks always run in this order, each one using what the ones before it produced
TASK_NAMES: dict[Task, str] = {
    "image_description": "Image description",
    "retrieval": "Retrieval",
    "text_generation": "Text generation",
    "image_generation": "Image generation",
}


class Plan(BaseModel):
    tasks: list[Task]

    def has(self, task: Task) -> bool:
        return task in self.tasks


def complete_plan(tasks: list[Task], images: int) -> Plan:
    """Every message gets an answer or a picture, and attached images are always
    read (and never looked for when there are none), whatever the router said"""
    wanted = set(tasks)
    if not wanted & {"text_generation", "image_generation"}:
        wanted.add("text_generation")
    if images:
        wanted.add("image_description")
    else:
        wanted.discard("image_description")

    return Plan(tasks=[task for task in TASK_NAMES if task in wanted])


# If the router can't decide, the answer is written as it was before there was
# a router: without the knowledge base (answer.md only allows its passages), and
# the diagram step decides for itself whether to draw
FALLBACK_TASKS: list[Task] = ["text_generation", "image_generation"]


def describe_plan(plan: Plan) -> str:
    return " → ".join(TASK_NAMES[task] for task in plan.tasks)


def run_router(ref: ModelRef, message: str, history: list[dict], images: int, drew_diagram: bool, trace: Trace) -> Plan:
    recent = "\n".join(f"{m['role']}: {m['content'][:MESSAGE_PREVIEW]}" for m in history[-RECENT_MESSAGES:]) or "(no earlier messages)"
    attached = [f"The user attached {images} image(s)." if images else "", "The user drew a network diagram." if drew_diagram else ""]
    agent_input = f"Conversation:\n{recent}\n\nNew message: {message}\n" + "\n".join(note for note in attached if note)

    plan = complete_plan(FALLBACK_TASKS, images)

    with trace.step("router", model=ref, input=agent_input.strip(), fallback=True) as step:
        plan = complete_plan(call_agent(ref, "router.md", agent_input, step, reply_type=Plan).tasks, images)

    if "error" in step:
        step["output"] = f"Couldn't plan the steps, so it answers without the knowledge base: {describe_plan(plan)}"
    else:
        step["output"] = describe_plan(plan)

    return plan
