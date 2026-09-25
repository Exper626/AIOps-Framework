// Attached images are kept in the chat itself as base64 data URLs, so nothing
// is uploaded to a separate file store.

// Longest side in pixels. Screenshots up to this size are kept exactly as they
// are; larger images are scaled down. Vision models shrink images to about
// this size or less anyway, so more pixels wouldn't help them read it.
const MAX_SIDE = 2560;

// Largest image a chat message keeps, in bytes (before base64)
const MAX_BYTES = 5 * 1024 * 1024;

const JPEG_QUALITY = 0.9;
const ACCEPTED_TYPES = ["image/jpeg", "image/png"];

function readAsDataUrl(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(new Error("Couldn't read the image."));
    reader.readAsDataURL(blob);
  });
}

function drawScaled(
  bitmap: ImageBitmap,
  scale: number,
  type: string
): Promise<Blob> {
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(bitmap.width * scale);
  canvas.height = Math.round(bitmap.height * scale);

  const context = canvas.getContext("2d");
  if (!context) {
    return Promise.reject(new Error("Couldn't process the image."));
  }

  // JPEG has no transparency; without this, transparent areas turn black
  if (type === "image/jpeg") {
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
  }
  context.imageSmoothingQuality = "high";
  context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) =>
        blob ? resolve(blob) : reject(new Error("Couldn't process the image.")),
      type,
      JPEG_QUALITY
    );
  });
}

// PNGs stay PNG (lossless, so diagram lines and labels stay sharp) and JPEGs
// stay JPEG. Only an image still over the size limit is turned into a JPEG.
export async function imageToDataUrl(
  file: File
): Promise<{ url: string; contentType: string }> {
  if (!ACCEPTED_TYPES.includes(file.type)) {
    throw new Error("Only PNG and JPEG images can be attached.");
  }

  const bitmap = await createImageBitmap(file);

  try {
    const scale = Math.min(1, MAX_SIDE / Math.max(bitmap.width, bitmap.height));
    let image: Blob =
      scale < 1 ? await drawScaled(bitmap, scale, file.type) : file;

    if (image.size > MAX_BYTES) {
      image = await drawScaled(bitmap, scale, "image/jpeg");
    }

    if (image.size > MAX_BYTES) {
      throw new Error(
        "This image is too large, even after resizing (5 MB max)."
      );
    }

    return { contentType: image.type, url: await readAsDataUrl(image) };
  } finally {
    bitmap.close();
  }
}
