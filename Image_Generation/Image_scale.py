from PIL import Image
from pathlib import Path
import os ##

input_folder = Path("Images7")
output_folder = Path("Images7_process")
output_folder.mkdir(exist_ok=True)

TARGET_SIZE = 700

for img_path in input_folder.glob("*.*"):
    img = Image.open(img_path)
    w, h = img.size

    # Create a new white background
    new_img = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), (255, 255, 255))

    # If image is larger than TARGET_SIZE, crop equally
    left = max(0, (w - TARGET_SIZE) // 2)
    top = max(0, (h - TARGET_SIZE) // 2)
    right = left + min(w, TARGET_SIZE)
    bottom = top + min(h, TARGET_SIZE)
    cropped_img = img.crop((left, top, right, bottom))

    # Paste cropped image onto white background, centered
    paste_x = (TARGET_SIZE - cropped_img.width) // 2
    paste_y = (TARGET_SIZE - cropped_img.height) // 2
    new_img.paste(cropped_img, (paste_x, paste_y))

    # Save the new image
    new_img.save(output_folder / img_path.name)

print("Done!")
