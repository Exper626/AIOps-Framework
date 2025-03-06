# import ollama

'''
response = ollama.chat(model= "llama3.2:1b" , messages=[{"role":"user", "content":f"Hello how are you"}],stream=True)

full_response = ""

for chunk in response:
    full_response += chunk["message"]["content"]
    print(chunk["message"]["content"], end="", flush=True)  

print("\n\n") 


print(full_response)
'''



import ollama

response = ollama.chat(model="llama3.2:1b", messages=[{"role": "user", "content": "Hello, how are you?"}])
print(response)
