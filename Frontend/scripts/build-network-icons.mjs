// Builds the diagram icons from "Image Generation/icons" and lib/network-icons.json
// (each icon's id, name, category, device type and source file):
//   - public/network-icons/<id>.svg, for the diagram editor
//   - ../Backend/icons/<id>.png at 4x, for the Graphviz picture (Graphviz can't read SVG)
//
// Run it after changing the catalog:  node scripts/build-network-icons.mjs
// It uses Playwright's Chromium (npx playwright install chromium), or the one at CHROMIUM_PATH.

import {
  copyFile,
  mkdir,
  readdir,
  readFile,
  rm,
  writeFile,
} from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const FRONTEND = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  ".."
);
const SOURCE = path.join(FRONTEND, "..", "Image Generation", "icons");
const SVG_DIR = path.join(FRONTEND, "public", "network-icons");
const PNG_DIR = path.join(FRONTEND, "..", "Backend", "icons");
const SCALE = 4;

const { icons } = JSON.parse(
  await readFile(path.join(FRONTEND, "lib", "network-icons.json"), "utf8")
);

// Start clean, so icons taken out of the catalog don't linger
async function clear(dir, extension) {
  await mkdir(dir, { recursive: true });
  const files = (await readdir(dir)).filter((file) => file.endsWith(extension));
  await Promise.all(files.map((file) => rm(path.join(dir, file))));
}
await Promise.all([clear(SVG_DIR, ".svg"), clear(PNG_DIR, ".png")]);

await Promise.all(
  icons.map((icon) =>
    copyFile(
      path.join(SOURCE, icon.source),
      path.join(SVG_DIR, `${icon.id}.svg`)
    )
  )
);

const browser = await chromium.launch(
  process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}
);
const page = await browser.newPage({ deviceScaleFactor: SCALE });

// One icon at a time, on the one page
for (const icon of icons) {
  // biome-ignore lint/performance/noAwaitInLoops: the page shows one icon at a time
  const svg = (await readFile(path.join(SOURCE, icon.source))).toString(
    "base64"
  );
  await page.setContent(
    `<body style="margin:0;background:transparent"><img id="icon" style="display:block" src="data:image/svg+xml;base64,${svg}"></body>`
  );
  await page.locator("#icon").evaluate((img) => img.decode());
  await writeFile(
    path.join(PNG_DIR, `${icon.id}.png`),
    await page.locator("#icon").screenshot({ omitBackground: true })
  );
}

await browser.close();
console.log(`Built ${icons.length} icons`);
