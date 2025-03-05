






if __name__ == "__main__":

    filepath = filePaths("company")
    text = tokenizer(filepath)
    embeddings, chunks = embedding_text("company", text)
    collection = vector_database_create_chunks("company", embeddings, chunks)


    while True:
        user_input = input("Enter your question here >> ")
        response   = ollama_response(user_query = "What is mobitel company is known for", collection=collection)
