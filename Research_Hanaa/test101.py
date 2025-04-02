import ollama

models = ["mistral:latest", "deepseek-r1:latest", "llama3.2:latest", "gemma2:latest"]

for model in models:
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": "Hello, can you respond?"}])
        print(f"{model} is working: {response['message']['content'][:50]}...")
    except Exception as e:
        print(f"Error loading {model}: {e}")
