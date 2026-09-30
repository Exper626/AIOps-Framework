from concurrent.futures import ThreadPoolExecutor

from pipeline.errors import describe_error
from pipeline.models import ModelRef
from pipeline.retrieval_agent import Search, run_retrieval_agent
from pipeline.trace import Trace
from rag.embedding import EMBEDDING_MODEL, create_embedding
from rag.lookup import find_attributes, find_devices
from rag.prompt import build_context
from rag.reranker import rerank_chunks
from rag.retrieval import attribute_filter, fetch_devices, retrieve_chunks

# Devices listed by name in the trace before "and N more"
LISTED_DEVICES = 5


def describe_devices(devices: list[str]) -> str:
    shown = ", ".join(devices[:LISTED_DEVICES])
    return shown + (f" and {len(devices) - LISTED_DEVICES} more" if len(devices) > LISTED_DEVICES else "")


def describe_passages(chunks: list[dict], how: str) -> str:
    if not chunks:
        return f"{how}: nothing relevant found"

    devices = list(dict.fromkeys(chunk.get("device") or chunk.get("filename") or "unnamed" for chunk in chunks))
    passages = f"{len(chunks)} passage{'s' if len(chunks) > 1 else ''}"

    # A match already names its devices
    if how.startswith("Matched"):
        return f"{how} · {passages}"

    return f"{how} · {passages} from {', '.join(devices)}"


def shares(total: int, searches: int) -> list[int]:
    """How many passages each search gets: the total split evenly, and at least one each"""
    if searches >= total:
        return [1] * searches
    each, extra = divmod(total, searches)
    return [each + (1 if number < extra else 0) for number in range(searches)]


def best(text: str, chunks: list[dict], rerank: bool, count: int) -> tuple[list[dict], str | None]:
    """The count passages that answer the text best, and why reranking failed if it did"""
    if rerank and len(chunks) > count:
        try:
            return rerank_chunks(text, chunks, top_n=count), None
        except Exception as error:
            # The passages found are still good: keep the search's own order
            print(f"[knowledge base] {error} (keeping the search order)")
            return chunks[:count], str(error)[:200]
    return chunks[:count], None


def run_search(search: Search, hybrid: bool, rerank: bool, count: int) -> tuple[list[dict], str, str | None]:
    """One search: a device it names is fetched by name; a vendor, type or tag narrows the search;
    anything else is searched by keywords and meaning. Returns the passages, how they were found,
    and why reranking failed if it did."""
    attributes = search.filters()
    text = search.search_text or " ".join([*search.devices, *(str(v) for v in attributes.values())])

    if search.devices:
        chunks, rerank_error = best(text, fetch_devices(search.devices), rerank, count)
        return chunks, f"Matched {describe_devices(search.devices)}", rerank_error

    vector = create_embedding(text)
    found = retrieve_chunks(text, vector, hybrid=hybrid, filters=attribute_filter(attributes)) if attributes else []

    if found:
        how = "Filtered by " + ", ".join(str(v) if not isinstance(v, list) else ", ".join(v) for v in attributes.values())
    else:
        how = "Searched by keywords and meaning" if hybrid else "Searched by meaning"
        found = retrieve_chunks(text, vector, hybrid=hybrid)

    chunks, rerank_error = best(text, found, rerank, count)
    return chunks, how, rerank_error


def plan_from_words(message: str) -> list[Search]:
    """Without the retrieval agent's plan: the devices, vendor, type and tags named in the message"""
    attributes = find_attributes(message)
    return [
        Search(
            devices=find_devices(message),
            vendor=attributes.get("vendor"),
            device_type=attributes.get("device_type"),
            tags=attributes.get("tags", []),
            search_text=message,
        )
    ]


def search_knowledge_base(
    ref: ModelRef,
    message: str,
    history: list[dict],
    memories: str,
    image_models: list[str],
    hybrid: bool,
    rerank: bool,
    chunk_count: int,
    trace: Trace,
) -> list[dict]:
    """The retrieval agent plans a search for each part of the message; they run at the same time, and
    each gets its share of the passages, so one part can't crowd out another. Without a plan, the words
    of the message are matched instead."""
    plan = run_retrieval_agent(ref, message, history, memories, image_models, trace)
    text = f"{message}\nDevices in the attached image: {', '.join(image_models)}" if image_models else message
    searches = plan.searches if plan else plan_from_words(text)

    # Exact model numbers in the message ("C9300X-48HX") are fetched even when the plan missed them
    planned = {device for search in searches for device in search.devices}
    missed = [device for device in find_devices(text) if device not in planned]
    if plan and missed:
        searches = [*searches, Search(devices=missed, search_text=message)]

    chunks = []

    with trace.step("knowledge base", input="\n".join(s.search_text for s in searches), fallback=True) as step:
        step["model"] = EMBEDDING_MODEL
        with ThreadPoolExecutor(max_workers=len(searches)) as pool:
            replies = [
                pool.submit(run_search, search, hybrid, rerank, count)
                for search, count in zip(searches, shares(chunk_count, len(searches)))
            ]

        lines, failed = [], []
        seen = set()
        for reply in replies:
            if reply.exception():
                failed.append(reply.exception())
                lines.append(f"Failed: {describe_error(reply.exception(), 'knowledge base')}")
                continue

            found, how, rerank_error = reply.result()
            # A page two searches both found is used once
            new = [c for c in found if (c.get("device"), c.get("text")) not in seen]
            seen.update((c.get("device"), c.get("text")) for c in new)
            chunks += new
            line = describe_passages(new, how)
            if rerank_error:
                line += f" · reranking failed, so the search order was kept: {rerank_error}"
            lines.append(line)

        if len(failed) == len(searches):
            raise failed[0]

    if "error" in step:
        step["output"] = "Answering without the knowledge base"
    elif len(lines) == 1:
        step["output"] = lines[0]
    else:
        step["output"] = "\n".join(f"{number}. {line}" for number, line in enumerate(lines, start=1))
    if not chunks and "error" not in step:
        step["output"] += "\nSo the answer doesn't use the knowledge base"
    if chunks:
        # The passages exactly as the answer's prompt gets them
        step["raw_output"] = build_context(chunks)

    return chunks
