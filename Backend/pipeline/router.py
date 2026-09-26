from typing import Literal

from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace

RECENT_MESSAGES = 4
# Earlier answers can be long; the start is enough to follow the conversation
MESSAGE_PREVIEW = 600

ROUTE_NAMES = {
    "devices": "Device question",
    "troubleshooting": "Troubleshooting",
    "configuration": "Configuration",
    "design": "Network design",
    "concept": "Concept",
    "chat": "Chat",
}


class Route(BaseModel):
    route: Literal["devices", "troubleshooting", "configuration", "design", "concept", "chat"]
    search_knowledge_base: bool
    draw_diagram: bool


# If the router can't decide, the answer is written as it was before there was
# a router: without the knowledge base (answer.md only allows its passages), and
# the diagram step decides for itself whether to draw
FALLBACK = Route(route="concept", search_knowledge_base=False, draw_diagram=True)


def describe_route(route: Route) -> str:
    search = "search the knowledge base" if route.search_knowledge_base else "no knowledge base search"
    diagram = "draw a diagram if it helps" if route.draw_diagram else "no diagram"
    return f"{ROUTE_NAMES[route.route]}: {search}, {diagram}"


def run_router(ref: ModelRef, message: str, history: list[dict], images: int, drew_diagram: bool, trace: Trace) -> Route:
    recent = "\n".join(f"{m['role']}: {m['content'][:MESSAGE_PREVIEW]}" for m in history[-RECENT_MESSAGES:]) or "(no earlier messages)"
    attached = [f"The user attached {images} image(s)." if images else "", "The user drew a network diagram." if drew_diagram else ""]
    agent_input = f"Conversation:\n{recent}\n\nNew message: {message}\n" + "\n".join(note for note in attached if note)

    route = FALLBACK

    with trace.step("router", model=ref, input=agent_input.strip(), fallback=True) as step:
        route = call_agent(ref, "router.md", agent_input, step, reply_type=Route)

    step["output"] = describe_route(route) if "error" not in step else "Couldn't decide, so it answers without the knowledge base"

    return route
