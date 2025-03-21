import chromadb

# Path to the stored ChromaDB database
CHROMA_DB_DIR = "embeddings"

# Load ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_collection(name="telecom_finance")

def query_chroma(user_query, top_k=3):
    """
    Queries ChromaDB to retrieve the most relevant documents for a given query.
    
    :param user_query: The question or search term
    :param top_k: Number of most relevant results to retrieve
    :return: List of matching document excerpts
    """
    results = collection.query(
        query_texts=[user_query],
        n_results=top_k
    )

    # Check if any results were found
    if results["documents"]:
        print(f"\n🔍 Query: {user_query}")
        for i, doc in enumerate(results["documents"][0]):
            print(f"\n📄 Match {i+1}:")
            print(f"Source: {results['metadatas'][0][i]['source']}")
            print(f"Excerpt: {doc[:500]}...")  # Show first 500 chars
    else:
        print("⚠️ No relevant documents found.")

if __name__ == "__main__":
    while True:
        user_query = input("\n📝 Enter your query (or type 'exit' to stop): ")
        if user_query.lower() == "exit":
            break
        query_chroma(user_query)
