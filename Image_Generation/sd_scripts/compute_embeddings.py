#!/usr/bin/env python
# coding=utf-8
# Copyright 2025 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import glob
import hashlib

import pandas as pd
import torch
from transformers import T5EncoderModel

from diffusers import StableDiffusion3Pipeline


PROMPT = "a photo of sks dog"
MAX_SEQ_LENGTH = 77
LOCAL_DATA_DIR = "dog"
OUTPUT_PATH = "sample_embeddings.parquet"


def bytes_to_giga_bytes(bytes):
    return bytes / 1024 / 1024 / 1024


def generate_image_hash(image_path):
    with open(image_path, "rb") as f:
        img_data = f.read()
    return hashlib.sha256(img_data).hexdigest()


def load_sd3_pipeline():
    id = "stabilityai/stable-diffusion-3-medium-diffusers"
    text_encoder = T5EncoderModel.from_pretrained(id, subfolder="text_encoder_3", load_in_8bit=True, device_map="auto")
    pipeline = StableDiffusion3Pipeline.from_pretrained(
        id, text_encoder_3=text_encoder, transformer=None, vae=None, device_map="balanced"
    )
    return pipeline


@torch.no_grad()
def compute_embeddings(pipeline, prompt, max_sequence_length):
    (
        prompt_embeds,
        negative_prompt_embeds,
        pooled_prompt_embeds,
        negative_pooled_prompt_embeds,
    ) = pipeline.encode_prompt(prompt=prompt, prompt_2=None, prompt_3=None, max_sequence_length=max_sequence_length)

    print(
        f"{prompt_embeds.shape=}, {negative_prompt_embeds.shape=}, {pooled_prompt_embeds.shape=}, {negative_pooled_prompt_embeds.shape}"
    )

    max_memory = bytes_to_giga_bytes(torch.cuda.max_memory_allocated())
    print(f"Max memory allocated: {max_memory:.3f} GB")
    return prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds












import os

def run(args):
    pipeline = load_sd3_pipeline()

    # Support multiple image formats
    image_paths = glob.glob(os.path.join(args.local_data_dir, "*.*"))
    data = []

    for image_path in image_paths:
        # Compute hash
        img_hash = generate_image_hash(image_path)

        # Load corresponding caption
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        caption_path = os.path.join(args.captions_dir, base_name + ".txt")
        if os.path.exists(caption_path):
            with open(caption_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        else:
            prompt = ""  # fallback

        # Compute embeddings for this prompt
        (
            prompt_embeds,
            negative_prompt_embeds,
            pooled_prompt_embeds,
            negative_pooled_prompt_embeds,
        ) = compute_embeddings(pipeline, prompt, args.max_sequence_length)

        data.append(
            (img_hash, prompt_embeds, negative_prompt_embeds, pooled_prompt_embeds, negative_pooled_prompt_embeds)
        )

    # Create DataFrame
    embedding_cols = [
        "prompt_embeds",
        "negative_prompt_embeds",
        "pooled_prompt_embeds",
        "negative_pooled_prompt_embeds",
    ]
    df = pd.DataFrame(data, columns=["image_hash"] + embedding_cols)

    # Convert embeddings to lists for parquet
    for col in embedding_cols:
        df[col] = df[col].apply(lambda x: x.cpu().numpy().flatten().tolist())

    df.to_parquet(args.output_path)
    print(f"Data successfully serialized to {args.output_path}")

















if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Compute embeddings for SD3 with per-image prompts.")

    parser.add_argument(
        "--local_data_dir",
        type=str,
        required=True,
        help="Path to the directory containing instance images."
    )
    parser.add_argument(
        "--captions_dir",
        type=str,
        required=True,
        help="Path to the directory containing captions corresponding to images."
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="sample_embeddings.parquet",
        help="Path to serialize the parquet file."
    )
    parser.add_argument(
        "--max_sequence_length",
        type=int,
        default=77,
        help="Maximum sequence length to use for computing the embeddings."
    )

    args = parser.parse_args()

    # Pass both image folder and captions folder to the run() function
    run(args)
