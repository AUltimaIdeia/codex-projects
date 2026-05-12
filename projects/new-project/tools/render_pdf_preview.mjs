import fs from "node:fs/promises";
import path from "node:path";

const { createCanvas } = await import(
  "file:///C:/Users/vini1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas/index.js"
);
const { getDocument } = await import(
  "file:///C:/Users/vini1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pdfjs-dist/legacy/build/pdf.mjs"
);

const pdfPath = "C:/Users/vini1/OneDrive/Documentos/New project/output/pdf/Relatorio_Cliente_B_Living_Abril_2026.pdf";
const outDir = "C:/Users/vini1/OneDrive/Documentos/New project/output/pdf/previews";

await fs.mkdir(outDir, { recursive: true });
const data = new Uint8Array(await fs.readFile(pdfPath));
const pdf = await getDocument({ data, disableWorker: true }).promise;

for (let pageNum = 1; pageNum <= pdf.numPages; pageNum += 1) {
  const page = await pdf.getPage(pageNum);
  const viewport = page.getViewport({ scale: 1.6 });
  const canvas = createCanvas(Math.ceil(viewport.width), Math.ceil(viewport.height));
  const context = canvas.getContext("2d");
  await page.render({ canvasContext: context, viewport }).promise;
  const png = await canvas.encode("png");
  await fs.writeFile(path.join(outDir, `page-${String(pageNum).padStart(2, "0")}.png`), png);
}

console.log(JSON.stringify({ pages: pdf.numPages, outDir }, null, 2));
