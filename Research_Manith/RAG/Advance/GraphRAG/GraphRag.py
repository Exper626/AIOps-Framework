from neo4j import GraphDatabase
from chromadb import PersistentClient
from transformers import pipeline
import ollama
from transformers import AutoTokenizer, AutoModel
import torch

# Load a pre-trained embedding model from Hugging Face
def load_embedding_model(model_name="all-MiniLM-L6-v2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model

# Function to encode the text into embeddings
def encode_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings
def connect_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def store_knowledge(driver, entity, relation, target):
    with driver.session() as session:
        query = (
            "MERGE (e:Entity {name: $entity}) "
            "MERGE (t:Entity {name: $target}) "
            "MERGE (e)-[:RELATION {type: $relation}]->(t)"
        )
        session.run(query, entity=entity, relation=relation, target=target)

def query_neo4j(driver, entity):
    with driver.session() as session:
        query = "MATCH (e:Entity {name: $entity})-[:RELATION]->(t) RETURN t.name"
        results = session.run(query, entity=entity)
        return [record["t.name"] for record in results]

def connect_chroma():
    client = PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("documents")
    return collection

def store_embeddings(collection, doc_id, text, embed_model):
    embedding = embed_model.encode(text).tolist()
    collection.add(ids=[doc_id], embeddings=[embedding], documents=[text])


def query_chroma(collection, query_text, embed_model):
    embedding = embed_model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=3)
    return [res["documents"] for res in results["matches"]]




def generate_response(llm_model, context, query):
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    return ollama.chat(model=llm_model, messages=[{"role": "user", "content": prompt}])["message"]["content"]



tokenizer, model = load_embedding_model()
embed_model = lambda text: encode_text(text, tokenizer, model)


# Example usage
driver = connect_neo4j("bolt://localhost:7687", "neo4j", "User123456")
store_knowledge(driver, "AI", "is a field of", "Computer Science")
related_entities = query_neo4j(driver, "AI")

chroma_collection = connect_chroma()
# Assume `embed_model` is a preloaded embedding model
store_embeddings(chroma_collection, "doc1", "Artificial Intelligence is a branch of CS.", embed_model)
retrieved_docs = query_chroma(chroma_collection, "What is AI?", embed_model)

final_response = generate_response("llama2", " ".join(retrieved_docs), "What is AI?")
print(final_response)
