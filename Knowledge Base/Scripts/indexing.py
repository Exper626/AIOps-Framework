import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.data import DataObject

load_dotenv()


with open("config.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

KB_ROOT = CONFIG["knowledge_base"]["root"]
COLLECTION_NAME = CONFIG["weaviate"]["collection_name"]

EMBED_BASE_URL = CONFIG["embedding"]["base_url"]
EMBED_MODEL_NAME = CONFIG["embedding"]["model"]
EMBED_DIM = CONFIG["embedding"]["dim"]
EMBED_BATCH_SIZE = CONFIG["embedding"]["batch_size"]

URL_PATTERN = re.compile(r"^https?://")

_embed_client = OpenAI(base_url=EMBED_BASE_URL, api_key=os.environ["EMBED_API_KEY"])



def load_knowledge_base(root_dir: str):
    root = Path(root_dir)
    chunks = []

    for path in sorted(root.rglob("*.txt")):
        raw = path.read_text(encoding="utf-8", errors="ignore").strip()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        if not lines:
            continue

        source_url = None
        body_lines = lines
        if URL_PATTERN.match(lines[0]):
            source_url = lines[0]
            body_lines = lines[1:]

        body = "\n".join(body_lines).strip()
        if not body:
            continue

        rel_parts = path.relative_to(root).parts   # e.g. ('Cisco', 'switches', 'Access', 'Cisco Catalyst 9200.txt')
        vendor = rel_parts[0] if rel_parts else None
        device_type = rel_parts[1] if len(rel_parts) > 1 else None
        sub_parts = rel_parts[2:-1]
        subcategory = " / ".join(sub_parts) if sub_parts else None
        filename = rel_parts[-1]

        chunks.append({
            "text": body,
            "vendor": vendor,
            "device_type": device_type,
            "subcategory": subcategory or "",
            "filename": filename,
            "source_url": source_url or "",
        })

    return chunks



def get_embeddings(texts: list[str]) -> list[list[float]]:
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i : i + EMBED_BATCH_SIZE]
        resp = _embed_client.embeddings.create(model=EMBED_MODEL_NAME, input=batch)
        vectors.extend(item.embedding for item in resp.data)

    if vectors and len(vectors[0]) != EMBED_DIM:
        raise ValueError(
            f"config.yaml says embedding.dim={EMBED_DIM}, but the API returned "
            f"{len(vectors[0])}-dim vectors — update config.yaml to match."
        )
    return vectors



def get_or_create_collection(client: weaviate.WeaviateClient):
    if client.collections.exists(COLLECTION_NAME):
        return client.collections.get(COLLECTION_NAME)

    return client.collections.create(
        name=COLLECTION_NAME,
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="vendor", data_type=DataType.TEXT),
            Property(name="device_type", data_type=DataType.TEXT),
            Property(name="subcategory", data_type=DataType.TEXT),
            Property(name="filename", data_type=DataType.TEXT),
            Property(name="source_url", data_type=DataType.TEXT),
        ],
        vector_config=Configure.Vectors.self_provided(),  # we supply our own embeddings
    )


def main():
    chunks = load_knowledge_base(KB_ROOT)
    print(f"Loaded {len(chunks)} chunks from '{KB_ROOT}'")
    if not chunks:
        print("No chunks found — check KB_ROOT path.")
        return

    print("Embedding...")
    vectors = get_embeddings([c["text"] for c in chunks])

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ["WEAVIATE_URL"],
        auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
    )
    try:
        collection = get_or_create_collection(client)

        objects = [
            DataObject(
                properties={
                    "text": c["text"],
                    "vendor": c["vendor"],
                    "device_type": c["device_type"],
                    "subcategory": c["subcategory"],
                    "filename": c["filename"],
                    "source_url": c["source_url"],
                },
                vector=vec,
            )
            for c, vec in zip(chunks, vectors)
        ]

        result = collection.data.insert_many(objects)
        n_errors = len(result.errors)
        print(f"Inserted {len(objects) - n_errors} / {len(objects)} objects into '{COLLECTION_NAME}'")
        if n_errors:
            for idx, err in result.errors.items():
                print(f"  [{idx}] {err.message}")
    finally:
        client.close()


if __name__ == "__main__":
    main()