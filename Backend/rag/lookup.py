"""Finds what a question names in the knowledge base: devices and model numbers
("C9300X-48HX", "Catalyst 9300", "MX105"), or a vendor, device type and tags
("Juniper outdoor access points"). Names are compared ignoring case, spaces and
dashes, so "c9300x 48hx" finds "C9300X-48HX". No model is called.
"""

import re
import time
from dataclasses import dataclass, field

from rag.retrieval import COLLECTION_NAME, weaviate_client

# The list of names is read from Weaviate, and again after this long, so a
# re-run of indexing.py shows up without restarting the backend
REFRESH_SECONDS = 600
# A partly typed model number needs at least this many characters ("C930" finds the C9300s)
MIN_PARTIAL_LENGTH = 4
# Longest name, in words, looked for in a question ("Cisco Business 150AX Wi-Fi 6")
MAX_NAME_WORDS = 8
# Words people use for a device type, as stored by indexing.py
DEVICE_TYPE_WORDS = {
    "switch": "switch",
    "switches": "switch",
    "router": "router",
    "routers": "router",
    "access point": "access point",
    "access points": "access point",
    "ap": "access point",
    "aps": "access point",
}
VENDOR_WORDS = {"meraki": "Cisco", "mist": "Juniper"}
# Folder names too vague to filter by
IGNORED_TAGS = {"Other"}


def key(text: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", text.upper())


def device_names(device: str, vendor: str) -> list[str]:
    """Ways a device is written: "Cisco Catalyst 9300 Series" is also
    "Catalyst 9300"; "QFX10008 and QFX10016" is two names"""
    names = [device]
    for part in re.split(r"\s+and\s+", device):
        short = re.sub(rf"^{re.escape(vendor)}\s+", "", part, flags=re.IGNORECASE)
        short = re.sub(r"\s+(Series|Switch|Router|Route|Access Point)$", "", short, flags=re.IGNORECASE)
        names += [part, short]
    return names


def model_tokens(device: str, models: list[str]) -> list[str]:
    """Model numbers: those found in the device's page, and the words in its name
    with both letters and digits ("MX67W" in "Meraki MX67W"). Plain numbers like
    "100" in "Cisco Business 100" aren't, or "100 users" would find it."""
    words = re.findall(r"[A-Za-z0-9]+", device)
    return [*models, *(w for w in words if re.search(r"\d", w) and re.search(r"[A-Za-z]", w) and len(w) >= 3)]


@dataclass
class Catalog:
    names: dict[str, set[str]] = field(default_factory=dict)  # name key -> devices
    tokens: dict[str, set[str]] = field(default_factory=dict)  # model number key -> devices
    vendors: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    # Every device with its vendor, device_type and tags (folders)
    devices: list[dict] = field(default_factory=list)


_catalog = Catalog()
_loaded_at: float | None = None


def catalog() -> Catalog:
    global _catalog, _loaded_at

    if _loaded_at is not None and time.monotonic() - _loaded_at < REFRESH_SECONDS:
        return _catalog

    fresh = Catalog()
    try:
        collection = weaviate_client().collections.get(COLLECTION_NAME)
        for item in collection.iterator(return_properties=["device", "models", "vendor", "device_type", "tags"]):
            p = item.properties
            fresh.devices.append({name: p.get(name) for name in ("device", "vendor", "device_type", "tags")})
            models = p.get("models") or []
            for name in [*device_names(p["device"], p["vendor"]), *models]:
                fresh.names.setdefault(key(name), set()).add(p["device"])
            for token in model_tokens(p["device"], models):
                fresh.tokens.setdefault(key(token), set()).add(p["device"])
            fresh.vendors.add(p["vendor"])
            fresh.tags.update(t for t in p.get("tags") or [] if t not in IGNORED_TAGS)
    except Exception as error:
        # e.g. a collection loaded before devices were metadata: search it the usual way
        # (and try again after REFRESH_SECONDS)
        print(f"[knowledge base] Couldn't read the device names, so questions are only searched by keywords and meaning: {error}")

    _catalog, _loaded_at = fresh, time.monotonic()
    return _catalog


def word_runs(text: str) -> set[str]:
    """Every run of whole words, as keys: "c9300x-48hx poe" gives C9300X, C9300X48HX,
    C9300X48HXPOE, 48HX... so names match whole words only ("cheap 12" isn't "AP12")"""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {
        key("".join(words[start:end]))
        for start in range(len(words))
        for end in range(start + 1, min(start + MAX_NAME_WORDS, len(words)) + 1)
    }


def find_devices(question: str) -> list[str]:
    """Devices the question names: exactly ("C9300X-48HX", "Catalyst 9300", "MX67"),
    or else by the start of a model number ("C9300" finds every C9300X-...)"""
    known = catalog()
    runs = word_runs(question)
    found = {d for name_key, devices in [*known.names.items(), *known.tokens.items()] if name_key in runs for d in devices}

    if not found:
        for word in re.findall(r"[a-z0-9]+", question.lower()):
            if len(word) >= MIN_PARTIAL_LENGTH and re.search(r"\d", word) and re.search(r"[a-z]", word):
                found |= {d for token_key, devices in known.tokens.items() if token_key.startswith(key(word)) for d in devices}

    return sorted(found)


def find_attributes(question: str) -> dict:
    """Vendor, device type and tags the question names: "Juniper outdoor APs" gives
    {"vendor": "Juniper", "device_type": "access point", "tags": ["Outdoor"]}"""
    known = catalog()
    text = question.lower()
    question_words = re.findall(r"[a-z0-9]+", text)
    attributes = {}

    vendors = {v for v in known.vendors if v.lower() in question_words}
    vendors |= {vendor for word, vendor in VENDOR_WORDS.items() if word in question_words}
    if len(vendors) == 1:
        attributes["vendor"] = vendors.pop()

    type_phrase = next((w for w in sorted(DEVICE_TYPE_WORDS, key=len, reverse=True) if re.search(rf"\b{w}\b", text)), None)
    if type_phrase:
        attributes["device_type"] = DEVICE_TYPE_WORDS[type_phrase]
        text = re.sub(rf"\b{type_phrase}\b", " ", text)  # so "access point" doesn't also mean the "Access" tag

    runs = word_runs(text)
    tags = [t for t in known.tags if key(t) in runs]
    # "Wi-Fi 6E" also contains "Wi-Fi 6": keep the longer one
    tags = [t for t in tags if not any(t != other and key(t) in key(other) for other in tags)]
    if tags:
        attributes["tags"] = sorted(tags)

    return attributes


def catalog_text() -> str:
    """The devices grouped by vendor, type and folders, one group a line, like
    "Cisco · router · branch / meraki / small branch: Meraki MX67, Meraki MX68"."""
    groups: dict[str, list[str]] = {}
    for d in catalog().devices:
        path = " · ".join(part for part in (d["vendor"], d["device_type"], " / ".join(d.get("tags") or [])) if part)
        groups.setdefault(path, []).append(d["device"])
    return "\n".join(f"{path}: {', '.join(sorted(devices))}" for path, devices in sorted(groups.items()))
