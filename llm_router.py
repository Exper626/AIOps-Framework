import ollama
import chromadb
import random

# Path to stored ChromaDB embeddings
CHROMA_DB_DIR = "embeddings"

# Available LLMs with their latest versions
LLMS = {
    "mistral": "mistral:latest",
    "deepseek": "deepseek-r1:latest",
    "llama3": "llama3.2:latest",
    "gemma": "gemma2:latest"
}

# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_collection(name="telecom_finance")

def query_chroma(user_query, top_k=3):
    """
    Queries ChromaDB to retrieve the most relevant document excerpts.
    
    :param user_query: The question or search term
    :param top_k: Number of most relevant results to retrieve
    :return: List of relevant document texts
    """
    results = collection.query(query_texts=[user_query], n_results=top_k)

    if results["documents"]:
        return [doc for doc_list in results["documents"] for doc in doc_list]
    return []

def select_best_llm(user_query):
    """
    Dynamically selects the best LLM based on query type.
    
    - Mistral for short queries (< 10 words)
    - DeepSeek for longer, detailed queries
    - LLaMA 3.2 for general-purpose questions
    - Gemma for finance & stock-related queries
    """
    query_length = len(user_query.split())

    if "finance" in user_query.lower() or "stock" in user_query.lower():
        return LLMS["gemma"]  # Gemma is optimized for finance
    elif query_length < 10:
        return LLMS["mistral"]  # Mistral handles short prompts well
    elif query_length > 20:
        return LLMS["deepseek"]  # DeepSeek is great for detailed responses
    else:
        return LLMS["llama3"]  # Default model for general cases

def generate_answer(user_query):
    """
    Retrieves relevant data from ChromaDB and queries the best LLM.

    :param user_query: The user's input query
    :return: The LLM-generated response
    """
    retrieved_docs = query_chroma(user_query)
    context = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."

    # Ask user if they want to manually select an LLM
    use_manual = input("\n🎯 Do you want to manually select an LLM? (yes/no): ").strip().lower()

    if use_manual == "yes":
        print("\n🛠 Available LLMs: [mistral, deepseek, llama3, gemma]")
        selected_llm = input("🔹 Enter the model name: ").strip().lower()

        if selected_llm in LLMS:
            selected_llm = LLMS[selected_llm]  # Get the full model name
        else:
            print("\n⚠️ Invalid choice! Falling back to auto-selection.")
            selected_llm = select_best_llm(user_query)
    else:
        # Automatic selection
        selected_llm = select_best_llm(user_query)

    print(f"\n🤖 Using LLM: {selected_llm}")

    prompt = f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
    
    response = ollama.chat(model=selected_llm, messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]

if __name__ == "__main__":
    while True:
        user_query = input("\n📝 Enter your question (or type 'exit' to stop): ")
        if user_query.lower() == "exit":
            break
        answer = generate_answer(user_query)
        print(f"\n💡 Answer: {answer}")
