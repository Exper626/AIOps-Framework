from pydantic import BaseModel

from pipeline.agent import call_agent
from pipeline.models import ModelRef
from pipeline.trace import Trace
from rag.lookup import catalog, catalog_text, key


class SearchPlan(BaseModel):
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


def known(value: str | None, options) -> str | None:
    """The option the value means, written as the knowledge base writes it ("cisco" is "Cisco")"""
    return next((option for option in options if key(option) == key(value)), None) if value else None


def keep_known(plan: SearchPlan) -> SearchPlan:
    """Only devices and filter values that are in the knowledge base"""
    devices = catalog().devices
    tags = [part.strip() for tag in plan.tags for part in tag.split("/")]

    return SearchPlan(
        devices=[name for device in plan.devices if (name := known(device, {d["device"] for d in devices}))],
        vendor=known(plan.vendor, catalog().vendors),
        device_type=known(plan.device_type, {d["device_type"] for d in devices}),
        tags=[name for tag in tags if (name := known(tag, catalog().tags))],
        search_text=plan.search_text.strip(),
    )


def describe_search_plan(plan: SearchPlan) -> str:
    parts = [", ".join(plan.devices)] if plan.devices else []
    filters = [value for value in (plan.vendor, plan.device_type, *plan.tags) if value]
    if filters:
        parts.append("Filter: " + ", ".join(filters))
    if plan.search_text:
        parts.append(f"Search: “{plan.search_text}”")
    return " · ".join(parts) or "Nothing to narrow down: searching the question as it is"


def run_retrieval_agent(ref: ModelRef, question: str, trace: Trace) -> SearchPlan | None:
    """Plans the search with the knowledge base's structure and device list in its prompt:
    which devices to fetch, which filters to use and what text to search for"""
    devices = catalog_text()

    if not devices:
        with trace.step("retrieval agent") as step:
            step["skipped"] = "Couldn't read the knowledge base's device list"
        return None

    plan = None

    with trace.step("retrieval agent", model=ref, input=question, fallback=True) as step:
        plan = keep_known(call_agent(ref, "retrieval.md", question, step, reply_type=SearchPlan, variables={"catalog": devices}))

    if plan:
        step["output"] = describe_search_plan(plan)
    else:
        step["output"] = "Couldn't plan the search, so it matches the words in the question instead"

    return plan
