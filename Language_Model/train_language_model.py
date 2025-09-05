import os
if "COLAB_" not in "".join(os.environ.keys()):
    os.system("pip install unsloth")
else:
    os.system("pip install --no-deps bitsandbytes accelerate xformers==0.0.29.post3 peft trl triton cut_cross_entropy unsloth_zoo")
    os.system('pip install sentencepiece protobuf "datasets>=3.4.1,<4.0.0" "huggingface_hub>=0.34.0" hf_transfer')
    os.system("pip install --no-deps unsloth")

os.environ["UNSLOTH_NO_TRL_PATCH"] = "1"
from unsloth import FastLanguageModel
import torch






max_seq_length = 2048
dtype = None
load_in_4bit = True

local_rank = int(os.environ.get("LOCAL_RANK", 0))  # DDP sets this automatically
device_map = {"": local_rank} 

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    device_map=device_map
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)









model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)









from datasets import Dataset

file_path = "/kaggle/input/ccnanetwork/NowNetworkTrain.txt"
file_path = "NowNetworkTrain.txt"


def extract_prompt_response_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f if line.strip()]  # remove completely blank lines

    data = []
    prompt, response = None, None
    reading_prompt, reading_response = False, False

    instruction = (
        "I am a highly knowledgeable IT networking expert specializing in protocols, architectures, "
        "and communication models. I provide accurate and concise answers to technical networking "
        "questions in a clear and helpful manner."
    )

    for line in lines:
        line = line.strip()  # strip each line of spaces
        if line.startswith("Prompt:"):
            # Save previous pair before starting new one
            if prompt and response:
                data.append({
                    "instruction": instruction,
                    "input": prompt.strip(),
                    "output": response.strip()
                })
            prompt = line.replace("Prompt:", "").strip()
            response = ""  # reset
            reading_prompt = True
            reading_response = False

        elif line.startswith("Response:"):
            response = line.replace("Response:", "").strip()
            reading_response = True
            reading_prompt = False

        elif reading_prompt:  # still collecting prompt
            prompt += "\n" + line.strip()
        elif reading_response:  # still collecting response
            response += "\n" + line.strip()

    # Add the last block if valid
    if prompt and response:
        data.append({
            "instruction": instruction,
            "input": prompt.strip(),
            "output": response.strip()
        })

    print(f"Total Pairs: {len(data)}")
    return data

pairs = extract_prompt_response_pairs(file_path)
finetuning_dataset = Dataset.from_list(pairs)
print(finetuning_dataset[2400])
print(len(finetuning_dataset))
finetuning_dataset = finetuning_dataset.shuffle(seed=42)







networking_prompt = """
### Instruction:
{}

### Input:
{}

### Response:
{}"""

EOS_TOKEN = tokenizer.eos_token

def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        text = networking_prompt.format(instruction, input, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts }

formatted_dataset = finetuning_dataset.map(formatting_prompts_func, batched=True)
print(formatted_dataset[0]["text"])



print("Started training......\n\n")

from trl import SFTConfig, SFTTrainer
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = formatted_dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    packing = False, # Can make training 5x faster for short sequences.
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 50,
        num_train_epochs = 3,
        #max_steps = 60,
        learning_rate = 2e-4,
        logging_steps = 4,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
        ddp_find_unused_parameters = False
    ),
)


model_name = 'a2'

trainer_stats = trainer.train()
model.save_pretrained(model_name)
tokenizer.save_pretrained(model_name)