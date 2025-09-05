from diffusers import FluxPipeline, AutoPipelineForText2Image, FluxTransformer2DModel, BitsAndBytesConfig
from transformers import T5EncoderModel
from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig
import torch
import gc

import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--last_epoch",
    type=int,
    default=1,
    help="Path to a specific checkpoint or 'latest' to auto-resume"
)

args = parser.parse_args()

ckpt_id = "black-forest-labs/FLUX.1-dev"
lora_path = f"/kaggle/working/output_model/checkpoint-{args.last_epoch}"
fused_transformer_path = "fused_transformer"

bnb_4bit_compute_dtype = torch.float16

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
)

# Load pipeline and fuse LoRA
transformer = FluxTransformer2DModel.from_pretrained(
    ckpt_id, subfolder="transformer",
    quantization_config=nf4_config, torch_dtype=torch.float16
)

quant_config = TransformersBitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.float16)
text_encoder = T5EncoderModel.from_pretrained(ckpt_id, subfolder="text_encoder_2", quantization_config=quant_config, torch_dtype=torch.float16,)


pipeline = FluxPipeline.from_pretrained(
    ckpt_id,
    transformer=transformer,
    text_encoder_2=text_encoder,
    torch_dtype=bnb_4bit_compute_dtype,
)
pipeline.load_lora_weights(lora_path)

del text_encoder
del transformer
gc.collect()
torch.cuda.empty_cache()

pipeline.to("cuda")

prompt = "[!SPEZ_TKS(sltmbntx)] router named Cisco ISR 1120"
image = pipeline(
    prompt,
    num_inference_steps=40,
    guidance_scale=12,
    height=768,
    width=768,
    generator=torch.manual_seed(42)
).images[0]

print(f"Pipeline memory usage: {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

image.save(f"networkManith3{args.last_epoch}.png")