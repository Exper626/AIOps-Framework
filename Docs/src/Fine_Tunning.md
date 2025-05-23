# Model Finetuning Techniques

## PEFT (Parameter Efficient Fine Tuning )
Below are some technqiues belong to this 


#### 1. LoRA (Low Rank Adaptation) 
- Freezing the model then train only the new dataset 


#### 2. DoRA (Weighted-Decomposed Low-Rank Adaptation)
- Developed by NVIDIA Research 
- Stated outperform LoRA and replacement to the LoRA


#### 3. Unsloth 
- An Organization : which found different ways to optimize model 
- Using some tricks to make LLM training 2x and 70% memory less training
- Can be only trained on a single gpu 
- Can be only trained on only Llama and other limited models available only 


#### 4. QLORA (Qunatized LoRA)
- Freeze the model then qunatized it ex: 32 bit --> 16 bit then train the new dataset on 32 bit


#### 5. QDoRA  
- Just like LoRA with qunatized this is DoRA with qunatized
- Outperform QLoRA


#### 5. LoRA+
- Just change the optimizer 


#### 6. NEFT (Noisy Embeddings Improve Finetuning)
- Adding gaussian noise : appreciate high level rather than low level granularity 


****** 


#### Preference Optimization
- Hard to define single "correct answer"
- allows the model to learn from comparision rather than labels 


### SFT (Self Finetuning)
- Label inputs  [ex: prompt, response]


### RLHF (Reinforcement Learning from Human Feedback)
- Broad paradigm


### PPO (Proximal Policy Optimization)
- Popular RL algorithm widely used to fine tune a LLM 
- 1 base model , policy model and reward model 


### DPO (Direct Preference Optimization)
- Newer technqiue designed to simplify Preference Optimization, not use full capability of RL 
- 1 base model and a policy model : not separate ; same 


### model quantized
AWQ - inference only 
GPTQ - inference only
GGUF - inference only
BitsAndBytes - Can be trained and inference
