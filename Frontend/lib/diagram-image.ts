import { iconFor, type NetworkLink } from "./diagram";

// A device as it sits on the canvas
export type PlacedDevice = {
  id: string;
  name: string;
  type: string;
  model: string;
  x: number;
  y: number;
  width: number;
  height: number;
};

const PADDING = 32;
const SCALE = 2;
const ICON_SIZE = 36;
const FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";

function escapeXml(text: string) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function iconDataUrl(type: string) {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const svg = await (await fetch(`${basePath}${iconFor(type)}`)).text();
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

// The diagram drawn as an SVG on a white background, the same way it looks on
// the canvas but without the toolbar, dots or selection
async function toSvg(devices: PlacedDevice[], links: NetworkLink[]) {
  const left = Math.min(...devices.map((d) => d.x)) - PADDING;
  const top = Math.min(...devices.map((d) => d.y)) - PADDING;
  const width = Math.max(...devices.map((d) => d.x + d.width)) - left + PADDING;
  const height =
    Math.max(...devices.map((d) => d.y + d.height)) - top + PADDING;

  const types = [...new Set(devices.map((d) => d.type))];
  const icons = new Map(
    await Promise.all(
      types.map(async (type) => [type, await iconDataUrl(type)] as const)
    )
  );

  const byId = new Map(devices.map((d) => [d.id, d]));
  const centre = (d: PlacedDevice) => ({
    x: d.x - left + d.width / 2,
    y: d.y - top + d.height / 2,
  });

  const cables = links.flatMap((link) => {
    const from = byId.get(link.source);
    const to = byId.get(link.target);

    if (!(from && to)) {
      return [];
    }

    const a = centre(from);
    const b = centre(to);
    return [
      `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="#9ca3af" stroke-width="1.5"/>`,
    ];
  });

  const cards = devices.map((d) => {
    const x = d.x - left;
    const y = d.y - top;
    const middle = d.width / 2;
    const model = d.model
      ? `<text x="${middle}" y="72" text-anchor="middle" font-size="10" fill="#6b7280">${escapeXml(d.model)}</text>`
      : "";

    return `<g transform="translate(${x} ${y})">
      <rect width="${d.width}" height="${d.height}" rx="12" fill="#ffffff" stroke="#e5e7eb"/>
      <image href="${icons.get(d.type)}" x="${middle - ICON_SIZE / 2}" y="8" width="${ICON_SIZE}" height="${ICON_SIZE}"/>
      <text x="${middle}" y="58" text-anchor="middle" font-size="11" font-weight="600" fill="#111827">${escapeXml(d.name)}</text>
      ${model}
    </g>`;
  });

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" font-family="${FONT}">
    <rect width="100%" height="100%" fill="#ffffff"/>
    ${cables.join("\n")}
    ${cards.join("\n")}
  </svg>`;

  return { height, svg, width };
}

async function toPng(devices: PlacedDevice[], links: NetworkLink[]) {
  const { height, svg, width } = await toSvg(devices, links);
  const url = URL.createObjectURL(
    new Blob([svg], { type: "image/svg+xml;charset=utf-8" })
  );

  try {
    const image = new Image();
    image.src = url;
    await image.decode();

    const canvas = document.createElement("canvas");
    canvas.width = width * SCALE;
    canvas.height = height * SCALE;
    const context = canvas.getContext("2d");

    if (!context) {
      throw new Error("This browser can't draw the image");
    }

    context.scale(SCALE, SCALE);
    context.drawImage(image, 0, 0, width, height);

    return await new Promise<Blob>((resolve, reject) =>
      canvas.toBlob(
        (blob) =>
          blob ? resolve(blob) : reject(new Error("Couldn't create the image")),
        "image/png"
      )
    );
  } finally {
    URL.revokeObjectURL(url);
  }
}

export async function downloadDiagramImage(
  devices: PlacedDevice[],
  links: NetworkLink[]
) {
  const url = URL.createObjectURL(await toPng(devices, links));
  const link = document.createElement("a");
  link.href = url;
  link.download = "network-diagram.png";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
