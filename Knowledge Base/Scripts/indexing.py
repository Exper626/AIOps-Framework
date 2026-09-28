import os
import re
from collections import Counter
from pathlib import Path

import requests
import weaviate
import yaml
from dotenv import load_dotenv
from weaviate.classes.config import Configure, DataType, Property, Tokenization
from weaviate.classes.data import DataObject
from weaviate.classes.init import Auth


from dotenv import load_dotenv
load_dotenv()

SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")
CONFIG = yaml.safe_load((SCRIPT_DIR / "config.yaml").read_text(encoding="utf-8"))

KB_ROOT = (SCRIPT_DIR / CONFIG["knowledge_base"]["root"]).resolve()
COLLECTION_NAME = CONFIG["weaviate"]["collection_name"]

EMBED_URL = CONFIG["embedding"]["url"]
EMBED_MODEL_NAME = CONFIG["embedding"]["model"]
EMBED_DIM = CONFIG["embedding"]["dim"]
EMBED_BATCH_SIZE = CONFIG["embedding"]["batch_size"]

URL_PATTERN = re.compile(r"^https?://")
MODEL_PATTERN = re.compile(r"\b[A-Z]{1,5}\d{2,5}[A-Z]{0,4}(?:-[A-Z0-9/]+)+\b")
NOT_MODELS = re.compile(r"^(?:Q?SFP|OSFP|CFP)\d")
DEVICE_TYPES = {"switches": "switch", "routers": "router", "access points": "access point"}


def expand_model(model: str) -> list[str]:
    pieces = re.split(r"/(?=[A-Z]{2,}\d)", model)
    if len(pieces) > 1:
        return [m for piece in pieces for m in expand_model(piece)]

    parts = model.split("-")
    for i, part in enumerate(parts):
        if "/" in part:
            options = [o for o in part.split("/") if o]
            suffix = re.sub(r"^\d+", "", options[-1])
            options = [o if re.search(r"[A-Z]", o) else o + suffix for o in options]
            return ["-".join([*parts[:i], o, *parts[i + 1 :]]) for o in options]

    return [model]


def load_devices(root: Path) -> list[dict]:
    devices = []

    for path in sorted(root.rglob("*.txt")):
        parts = path.relative_to(root).parts
        if len(parts) < 3 or parts[0] == SCRIPT_DIR.name:
            continue

        lines = [line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
        source_url = lines[0] if lines and URL_PATTERN.match(lines[0]) else ""
        text = "\n".join(lines[1:] if source_url else lines)

        if not text:
            print(f"  Skipped (empty): {path.relative_to(root)}")
            continue

        device_type = parts[1].strip().lower()
        devices.append(
            {
                "vendor": parts[0],
                "device_type": DEVICE_TYPES.get(device_type, device_type),
                "tags": list(parts[2:-1]),
                "device": path.stem,
                "models": sorted({m for found in MODEL_PATTERN.findall(text) for m in expand_model(found) if not NOT_MODELS.match(m)}),
                "source_url": source_url,
                "text": text,
            }
        )

    return devices


def embedding_text(device: dict) -> str:
    label = " · ".join([device["vendor"], device["device_type"], *device["tags"], device["device"]])
    return f"{label}\n{device['text']}"


def get_embeddings(texts: list[str]) -> list[list[float]]:
    vectors = []

    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        response = requests.post(
            EMBED_URL,
            headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
            json={
                "model": EMBED_MODEL_NAME,
                "input": {"texts": texts[i : i + EMBED_BATCH_SIZE]},
                "parameters": {"dimension": EMBED_DIM, "text_type": "document"},
            },
            timeout=120,
        )
        if not response.ok:
            raise RuntimeError(f"Embedding failed: {response.status_code} {response.text}")

        embeddings = sorted(response.json()["output"]["embeddings"], key=lambda item: item["text_index"])
        vectors.extend(item["embedding"] for item in embeddings)

    if vectors and len(vectors[0]) != EMBED_DIM:
        raise ValueError(
            f"config.yaml says embedding.dim={EMBED_DIM}, but the API returned {len(vectors[0])}-dim vectors: update config.yaml to match."
        )

    return vectors


def create_collection(client: weaviate.WeaviateClient):
    if client.collections.exists(COLLECTION_NAME):
        client.collections.delete(COLLECTION_NAME)

    return client.collections.create(
        name=COLLECTION_NAME,
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="vendor", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
            Property(name="device_type", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
            Property(name="tags", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.FIELD),
            Property(name="device", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
            Property(name="models", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.FIELD),
            Property(name="source_url", data_type=DataType.TEXT, index_searchable=False),
        ],
        vector_config=Configure.Vectors.self_provided(),
    )


def main():
    devices = load_devices(KB_ROOT)
    if not devices:
        print(f"No device files found in '{KB_ROOT}': check knowledge_base.root in config.yaml.")
        return

    print(f"Found {len(devices)} devices in '{KB_ROOT}':")
    for (vendor, device_type), count in sorted(Counter((d["vendor"], d["device_type"]) for d in devices).items()):
        print(f"  {vendor} {device_type}: {count}")
    print(f"  Model numbers found inside the files: {sum(len(d['models']) for d in devices)}")

    answer = input(f"\nThis replaces the '{COLLECTION_NAME}' collection in Weaviate. Continue? [y/N] ")
    if answer.strip().lower() != "y":
        print("Nothing changed.")
        return

    print("Embedding...")
    vectors = get_embeddings([embedding_text(d) for d in devices])

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ["WEAVIATE_URL"],
        auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
    )
    try:
        collection = create_collection(client)
        result = collection.data.insert_many([DataObject(properties=d, vector=v) for d, v in zip(devices, vectors, strict=True)])

        print(f"Inserted {len(devices) - len(result.errors)} / {len(devices)} devices into '{COLLECTION_NAME}'")
        for index, error in result.errors.items():
            print(f"  [{devices[index]['device']}] {error.message}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
