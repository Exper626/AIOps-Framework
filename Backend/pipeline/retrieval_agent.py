from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.router import recent_conversation
from pipeline.trace import Trace
from rag.lookup import catalog, catalog_text, key

# A safety net against a broken reply: a message never has this many separate parts
MAX_SEARCHES = 10


class Search(BaseModel):
    devices: list[str] = []
    vendor: str | None = None
    device_type: str | None = None
    tags: list[str] = []
    search_text: str = ""

    def filters(self) -> dict:
        """As rag.retrieval.attribute_filter takes them"""
        attributes = {name: value for name, value in (("vendor", self.vendor), ("device_type", self.device_type)) if value}
        if self.tags:
            attributes["tags"] = self.tags
        return attributes


class SearchPlan(BaseModel):
    searches: list[Search] = []


def known(value: str | None, options) -> str | None:
    """The option the value means, written as the knowledge base writes it ("cisco" is "Cisco")"""
    return next((option for option in options if key(option) == key(value)), None) if value else None


def keep_known(search: Search) -> Search:
    """Only devices and filter values that are in the knowledge base"""
    devices = catalog().devices
    tags = [part.strip() for tag in search.tags for part in tag.split("/")]

    return Search(
        devices=[name for device in search.devices if (name := known(device, {d["device"] for d in devices}))],
        vendor=known(search.vendor, catalog().vendors),
        device_type=known(search.device_type, {d["device_type"] for d in devices}),
        tags=[name for tag in tags if (name := known(tag, catalog().tags))],
        search_text=search.search_text.strip(),
    )


def describe_search(search: Search) -> str:
    parts = [", ".join(search.devices)] if search.devices else []
    filters = [value for value in (search.vendor, search.device_type, *search.tags) if value]
    if filters:
        parts.append("Filter: " + ", ".join(filters))
    if search.search_text:
        parts.append(f"Search: “{search.search_text}”")
    return " · ".join(parts) or "Nothing to narrow down: searching the message as it is"


def describe_search_plan(plan: SearchPlan) -> str:
    if len(plan.searches) == 1:
        return describe_search(plan.searches[0])
    return "\n".join(f"{number}. {describe_search(search)}" for number, search in enumerate(plan.searches, start=1))


def run_retrieval_agent(
    ref: ModelRef, message: str, history: list[dict], memories: str, image_models: list[str], trace: Trace
) -> SearchPlan | None:
    """Plans the searches with the knowledge base's structure and device list in its prompt: for each
    part of the message, which devices to fetch, which filters to use and what text to search for. The
    conversation and memories let it rewrite follow-ups ("and its PoE?") into searches that stand alone."""
    devices = catalog_text()

    if not devices:
        with trace.step("retrieval agent") as step:
            step["skipped"] = "Couldn't read the knowledge base's device list"
        return None

    agent_input = f"Conversation:\n{recent_conversation(history)}\n\nNew message: {message}"
    if image_models:
        agent_input += f"\nDevices in the attached image: {', '.join(image_models)}"
    if memories:
        agent_input = f"What you remember about the user:\n{memories}\n\n{agent_input}"

    plan = None

    with trace.step("retrieval agent", model=ref, input=agent_input, fallback=True) as step:
        reply = call_agent(ref, "retrieval.md", agent_input, step, reply_type=SearchPlan, variables={"catalog": devices})
        searches = [keep_known(search) for search in reply.searches[:MAX_SEARCHES]]
        # A search needs something to look for
        plan = SearchPlan(searches=[s for s in searches if s.devices or s.search_text or s.filters()])

    if plan and plan.searches:
        step["output"] = describe_search_plan(plan)
    elif plan:
        step["output"] = "Planned no search, so it matches the words in the message instead"
    else:
        step["output"] = "Couldn't plan the search, so it matches the words in the message instead"

    return plan if plan and plan.searches else None
