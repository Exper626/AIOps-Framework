import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.cache_utils import DynamicCache
import os

from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv("hf_token")

def generate(model, input_ids: torch.Tensor, past_key_values, max_new_tokens: int = 50) -> torch.Tensor:
    device = model.model.embed_tokens.weight.device
    origin_len = input_ids.shape[-1]
    input_ids = input_ids.to(device)
    output_ids = input_ids.clone()
    next_token = input_ids

    with torch.no_grad():
        for _ in range(max_new_tokens):
            out = model(
                input_ids=next_token,
                past_key_values=past_key_values,
                use_cache=True
            )
            logits = out.logits[:, -1, :]
            token = torch.argmax(logits, dim=-1, keepdim=True)
            output_ids = torch.cat([output_ids, token], dim=-1)
            past_key_values = out.past_key_values
            next_token = token.to(device)

            if model.config.eos_token_id is not None and token.item() == model.config.eos_token_id:
                break

    return output_ids[:, origin_len:]



def get_kv_cache(model, tokenizer, prompt: str) -> DynamicCache:
    device = model.model.embed_tokens.weight.device
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    cache = DynamicCache()

    with torch.no_grad():
        _ = model(
            input_ids=input_ids,
            past_key_values=cache,
            use_cache=True
        )
    return cache

def clean_up(cache: DynamicCache, origin_len: int):
    for i in range(len(cache.key_cache)):
        cache.key_cache[i] = cache.key_cache[i][:, :, :origin_len, :]
        cache.value_cache[i] = cache.value_cache[i][:, :, :origin_len, :]



model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name, token="", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True,
    token= hf_token
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"Loaded {model_name}.")



with open("document.txt", "r", encoding="utf-8") as f:
    doc_text = f.read()

system_prompt = f"""
<|system|>
You are an assistant who provides concise factual answers.
<|user|>
Context:
{doc_text}
Question:
""".strip()

ronan_cache = get_kv_cache(model, tokenizer, system_prompt)
origin_len = ronan_cache.key_cache[0].shape[-2]
print("KV cache built.")



question1 = "Who is Ronan Takizawa?"
clean_up(ronan_cache, origin_len)
input_ids_q1 = tokenizer(question1 + "\n", return_tensors="pt").input_ids.to(device)
gen_ids_q1 = generate(model, input_ids_q1, ronan_cache)
answer1 = tokenizer.decode(gen_ids_q1[0], skip_special_tokens=True)
print("Q1:", question1)
print("A1:", answer1)
