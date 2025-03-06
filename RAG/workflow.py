from llama_cpp import Llama
import ollama

llama_model_locations = { "gemma": "C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-7462734796d67c40ecec2ca98eddf970e171dbb6b370e43fd633ee75b69abe1b")
}




llm = Llama(model_path="")
output = llm(user_query)
print(output['choices'][0]['text'])

