import re
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from _customPrompts_ import prompt1, prompt2


load_dotenv()


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key= os.getenv("NVIDIA_API_KEY")
)



# h.md , cisco.txt , juniper.txt

with open("juniper.txt", "r", encoding="utf-8") as f:
    full_text = f.read()



segments = re.split(r'#!--\s*', full_text)
segments = [s.strip() for s in segments if s.strip()]  




# The data is SLT Mobitel company annual report 2023 pdf
# The data consisting is realted to cisco networking
# The data consisting is realted to juniper networking
# annual.jsonl , cisco.jsonl , juniper.jsonl :  

with open("juniper.jsonl", "w", encoding="utf-8") as dpo_out:
    for i, segment in enumerate(segments):
        print(f"\n--- Processing segment {i+1}/{len(segments)} ---")


        completion = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            top_k = 0.1,
            top_p=0.1,
            stream=False
        )

        if completion and completion.choices and completion.choices[0].message and completion.choices[0].message.content:
            reply = completion.choices[0].message.content.strip()
            dpo_out.write(reply)
            print(reply)

        else:
            print("Warning: No reply generated.")
            reply = ""

