import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb 
import numpy as np
import ollama



def tokenizer() -> str:

    file_path = "data/2021.pdf"
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    with open("Tokens.txt" , "w") as file:
        file.write(text)
    
    return text 



def sentence_transformers(text : str) -> np.ndarray:

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def chunk_text(text, chunk_size = 500):
        return [text[ i : i + chunk_size] for i in range(0,len(text), chunk_size)]

    chunks = chunk_text(text)
    embeddings = embedding_model.encode(chunks, convert_to_numpy = True)
    np.save("embedding.npy", embeddings)
    
    return embeddings, chunks


def vector_database(embeddings : np.array, chunks: list):

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("pdf_knowledge")

    for i, chunk in enumerate(chunks):
        collection.add(ids=[str(i)], documents = [chunk], embeddings = [embeddings[i].tolist()])

    return collection


def retrieve_relavent_chunks(query, top_k, collection, embedding_model):

    query_embedding = embedding_model.encode([query])[0]
    results = collection.query(query_embeddings = [query_embedding.tolist()])

    return results["documents"][0]



def ollama_response(query :str, embedding_model, collection ) -> str:

    relavent_chunks = retrieve_relavent_chunks(query, top_k=5, embedding_model=embedding_model, collection=collection)
    context = "\n".join(relavent_chunks)
    response = ollama.chat(model="llama3.2:1b", messages=[{"role":"user", "content":f"{context}\n\n{query}"}])

    return response


if __name__ == "__main__":

    text = tokenizer()
    embeddings, chunks = sentence_transformers(text)
    collection = vector_database(embeddings, chunks)

    embedding_model = (SentenceTransformer("all-MiniLM-L6-v2"))

    while True:
        user_input = input("Enter your question here >> ")
        response   = ollama_response(user_input, embedding_model=embedding_model, collection=collection)
        print(response["message"]["content"])
