
'''
from llama_cpp import Llama 


llm = Llama(model_path = "C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff")
output = llm("Hi how are you")
print(output)


''' 


import time
from llama_cpp import Llama
import ollama



# Measure the time taken to load llama-cpp model
start_load_time = time.time()
llm = Llama(model_path="C:\\Users\\ashwinir\\.ollama\\models\\blobs\\sha256-7462734796d67c40ecec2ca98eddf970e171dbb6b370e43fd633ee75b69abe1b")
end_load_time = time.time()

# Function to test llama-cpp-python inference speed
def test_llama_cpp():
    start_time = time.time()
    output = llm("Hi, how are you?")
    end_time = time.time()
    
    print("\nllama-cpp-python Output:")
    print(output['choices'][0]['text'])
    print(f"llama-cpp-python Inference Time: {end_time - start_time:.4f} seconds")

# Function to test Ollama inference speed
def test_ollama():
    start_time = time.time()
    response = ollama.chat(model="gemma2:2b", messages=[{"role": "user", "content": "Hello, how are you?"}])
    end_time = time.time()
    
    print("\nOllama Output:")
    print(response["message"]["content"])
    print(f"Ollama Inference Time: {end_time - start_time:.4f} seconds")

# Print the model load time
print(f"llama-cpp-python Model Load Time: {end_load_time - start_load_time:.4f} seconds")

# Run Tests
test_llama_cpp()
test_ollama()
