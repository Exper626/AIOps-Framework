from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_single_file(
    "/content/gdrive/MyDrive/Fast-Dreambooth/Sessions/abcdef/abcdef.ckpt",
    torch_dtype=torch.float16,
    safety_checker=None,

).to("cuda")

image = pipe(
    prompt="cisco_packet_tracer_switch_manith switch",
    negative_prompt="blurry, unfinished, bad",
    guidance_scale=6,
    num_inference_steps=30,
    generator=torch.Generator("cuda").manual_seed(40),
).images[0]

image.save("abc.png")
display(image)