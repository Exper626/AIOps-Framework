from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any, Literal
from unsloth import FastLanguageModel
import torch
from pydantic import Field

app = FastAPI()

max_seq_length = 2048
dtype = None
load_in_4bit = True

print("Loading Unsloth model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

model.eval()
print("Model loaded.")



class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ToolInputSchema(BaseModel):
    type: str
    properties: Dict[str, Any]
    required: Optional[List[str]] = None


class Tool(BaseModel):
    name: str
    description: Optional[str] = None
    input_schema: Optional[ToolInputSchema] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: Optional[List[Tool]] = None
    max_tokens: int = Field(..., alias="max_tokens")




with open("MCPPrompt.txt", "r") as f:
    system_prompt = f.read()



import uuid


@app.post("/v1/chat/completions")
def generate_text(request: ChatCompletionRequest) -> dict:
    print("Request:\n", request)

    user_messages = next((m.content for m in reversed(request.messages) if m.role == "user"), '')
    prompt = system_prompt + user_messages
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=0.7,
            top_p=0.95,
            top_k=50,
            do_sample=True,
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    raw_output = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    print("Raw Output:", raw_output)

    lines = raw_output.splitlines()

    # Simple check for tool use style output
    if len(lines) >= 3 and lines[0].strip().lower() == "tool_use":
        tool_name = lines[1].strip()
        tool_param = lines[2].strip()
        return {
            "id": "ex",
            "object": "chat.completion",
            "created": "ex",
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": tool_name,
                                "input": {
                                  "series" : tool_param,
                                }
                            }
                        ]
                    },
                    "finish_reason": "stop"
                }
            ]
        }

    # Default to regular text
    return {
        "id": "ex",
        "object": "chat.completion",
        "created": "ex",
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": raw_output
                        }
                    ]
                },
                "finish_reason": "stop"
            }
        ]
    }

print("End of the file is reached")
