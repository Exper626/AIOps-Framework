from llm_router import generate_answer

def main():
    print("\n🚀 Welcome to the LLM RAG System!")
    print("🔎 Ask any question related to the telecom finance dataset.")
    
    while True:
        user_query = input("\n📝 Enter your question (or type 'exit' to stop): ")
        if user_query.lower() == "exit":
            print("\n👋 Exiting... Have a great day!")
            break
        
        # Generate response using LLM
        answer = generate_answer(user_query)
        print(f"\n💡 Answer:\n{answer}")

if __name__ == "__main__":
    main()
