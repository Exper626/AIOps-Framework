from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import chromadb
import ollama

def vector_database_get_chunks(topic :str = "company", embedding_model = "all-MiniLM-L6-v2" , top_k = 3):
    
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        collection = chroma_client.get_collection(topic)
    
    except Exception as e:
        return e

    return collection


def retrieve_relavent_chunks(user_query, collection,  embedding_model = "all-MiniLM-L6-v2", top_k = 10):

    embedding_model = SentenceTransformer(embedding_model)
    user_query_embedding = embedding_model.encode([user_query])[0]
    results = collection.query(query_embeddings = [user_query_embedding.tolist()], n_results = top_k)
    
    return results["documents"], results["ids"]




llama_models = { "gemma": "C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-7462734796d67c40ecec2ca98eddf970e171dbb6b370e43fd633ee75b69abe1b",
               "llama3.2:1b": "C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff", 
               "llama3.2:latest": "C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-74701a8c35f6c8d9a4b91f3f3497643001d63e0c7a84e085bed452548fa88d45"
}




def ollamaModel(collection):


    which_model = int(input("Gemma = 1 \nllama 3.2.1b = 2\nllama3.2:latest = 3\n\n"))

    if which_model == 1:
        language_model = "gemma"

    elif which_model == 2:
        language_model = "llama3.2:1b"

    elif  which_model == 3:
        language_model = "llama3.2:latest"

    while True:
        user_query = input("Enter the question : ")
        relavent_chunks, relavent_ids = retrieve_relavent_chunks(user_query, collection=collection)
        response = ollama.chat(model= language_model , messages=[{"role":"user", "content":f"{relavent_chunks}\n\n{user_query}"}],stream=True)
        full_response = ""
        for chunk in response:
            full_response += chunk["message"]["content"]
            print(chunk["message"]["content"], end="", flush=True)  # Print content as it arrives




def llamacpp():

    which_model = int(input("Gemma = 1 \nllama 3.2.1b = 2\nllama3.2:latest = 3\n\n"))

    if which_model == 1:
        llm = Llama(model_path= llama_models["gemma"] )

    elif which_model == 2:
        llm = Llama(model_path= llama_models["llama3.2:1b"] )

    elif  which_model == 3:
        llm = Llama(model_path= llama_models["llama3.2:latest"] )


    collection = vector_database_get_chunks()

    while True:
        user_query = input("\nEnter question here : ") 
        rag_data , _  = retrieve_relavent_chunks(user_query = user_query, collection = collection)
        prompt = f"Context:\n{rag_data}\n\nUser Question:\n{user_query}"
        output = llm(prompt)
        print(output['choices'][0]['text'])
        print("\n\n")


which_way = int(input("Lamacpp : 1\nOllama : 2\n"))
if which_way == 1:
    llamacpp()

elif which_way == 2:

    collection = vector_database_get_chunks()
    ollamaModel(collection=collection)





