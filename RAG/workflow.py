# Evaluation, proof reading, answer generation, summarization, sentiment analysis, contenet classification
import langgraph
from langgraph.graph import StateGraph
import ollama



def generate_answer()   











def retrieve_relavent_chunks(user_query, collection, embedding_model = "all-MiniLM-L6-v2" , top_k = 3):

    embedding_model = SentenceTransformer(embedding_model).to(device())
    user_query_embedding = embedding_model.encode([user_query])[0]
    results = collection.query(query_embeddings = [user_query_embedding.tolist()], n_results = top_k)
    
    return results["documents"], results["ids"]




def ollama_response(user_query :str, collection, embedding_model = "all-MiniLM-L6-v2", top_k = 3, langauge_model = "llama3.2:1b" ) -> str:

    relavent_chunks, relavent_ids = retrieve_relavent_chunks(user_query,collection=collection,top_k=top_k, embedding_model=embedding_model)
    response = ollama(model= langauge_model , messages=[{"role":"user", "content":f"{relavent_chunks}\n\n{user_query}"}],stream=True)

    full_response = ""

    for chunk in response:
        full_response += chunk["message"]["content"]
        print(chunk["message"]["content"], end="", flush=True)  

    return full_response 




