"""The networking model fine-tuned with ORPO (Llama-3-8B + a LoRA adapter, trained on Kaggle), served on Modal
with vLLM's OpenAI-compatible API. Once deployed, the Backend finds it by itself (with MODAL_TOKEN_ID and
MODAL_TOKEN_SECRET set) and it shows up in Settings → Self-hosted as "slt-networking-llama3-8b".

1. Upload the adapter (adapter_config.json and adapter_model.safetensors) to the Hugging Face repo below
2. On Modal, add a Secret named "huggingface" with HF_TOKEN set to a Hugging Face read token, since the
   repo is private
3. Start the server:  modal deploy networking_model.py

It was trained on single networking questions in one fixed format, not on chat, so the server always puts the
latest question into that format and leaves out the system prompt, earlier messages and knowledge base
passages. Pick it for the Answer step only: the other steps need JSON, and it can't read images."""

import subprocess
import time
import urllib.request

import modal

# The Hugging Face repo the adapter was uploaded to from Kaggle
ADAPTER_REPO = "Manith/slt-networking-llama3-8b"
# The model it was trained on, in 16-bit (training used a 4-bit copy of the same weights); public on Hugging Face
BASE_MODEL = "unsloth/llama-3-8b"
# The fine-tuned model's name in the Backend's Settings, and the plain base model's, which vLLM serves as well
MODEL_NAME = "slt-networking-llama3-8b"
BASE_NAME = "llama-3-8b-base"

PORT = 8000
MINUTES = 60

# The training prompt (orpo_config.json's prompt_template), filled with the latest question
CHAT_TEMPLATE = (
    "{{ bos_token }}You are a computer networking expert. Answer the question accurately.\n\n"
    "### Question:\n{{ (messages | selectattr('role', 'equalto', 'user') | list | last).content | trim }}\n\n"
    # Written as an expression: Jinja drops a template's last newline
    "### Answer:{{ '\\n' }}"
)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("vllm==0.30.0", "huggingface_hub[hf_transfer]")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

# Downloads are kept between starts, so only the first start fetches the 16 GB base model
hf_cache = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache = modal.Volume.from_name("vllm-cache", create_if_missing=True)

# The tags let the Backend list the model by name without waking the server: only the fine-tuned model, not the
# base one, and not for Vision
app = modal.App("slt-networking-model", tags={"model": MODEL_NAME, "reads-images": "no"})


@app.server(
    port=PORT,
    image=image,
    gpu="L4",  # 24 GB: the 16 GB model plus room for requests; "A10G" works too
    secrets=[modal.Secret.from_name("huggingface")],
    volumes={"/root/.cache/huggingface": hf_cache, "/root/.cache/vllm": vllm_cache},
    startup_timeout=20 * MINUTES,  # the first start downloads the base model
    scaledown_window=5 * MINUTES,  # stops (and stops costing) after 5 idle minutes
    target_concurrency=8,
)
class NetworkingModel:
    @modal.enter()
    def start(self):
        with open("/root/chat_template.jinja", "w") as file:
            file.write(CHAT_TEMPLATE)

        self.process = subprocess.Popen(
            [
                "vllm", "serve", BASE_MODEL,
                "--served-model-name", BASE_NAME,
                "--enable-lora",
                "--lora-modules", f"{MODEL_NAME}={ADAPTER_REPO}",
                "--max-lora-rank", "16",
                "--chat-template", "/root/chat_template.jinja",
                "--max-model-len", "8192",
                "--gpu-memory-utilization", "0.90",
                "--host", "0.0.0.0",
                "--port", str(PORT),
            ]
        )

        # Ready once vLLM answers its health check
        while True:
            if self.process.poll() is not None:
                raise RuntimeError(f"vLLM stopped while starting (exit code {self.process.returncode})")
            try:
                with urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=5):
                    return
            except OSError:
                time.sleep(5)

    @modal.exit()
    def stop(self):
        self.process.terminate()
