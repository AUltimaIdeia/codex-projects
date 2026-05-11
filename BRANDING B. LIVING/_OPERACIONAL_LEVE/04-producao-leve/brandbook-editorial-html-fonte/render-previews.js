const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const htmlPath = path.join(root, "index.html");
const outDir = path.join(root, "previews");

fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2,
  });

  await page.goto(`file://${htmlPath.replace(/\\/g, "/")}`, {
    waitUntil: "networkidle",
  });

  await page.evaluate(() => document.fonts.ready);

  const ids = await page.$$eval(".page", (nodes) => nodes.map((node) => node.id));

  for (const id of ids) {
    const element = await page.$(`#${id}`);
    const pageNumber = await element.evaluate((node) => node.dataset.page || id.replace(/\D/g, ""));
    const filename = path.join(outDir, `brandbook-b-living-p${pageNumber}.png`);
    await element.screenshot({ path: filename });
  }

  await browser.close();
  console.log(`Rendered ${ids.length} previews to ${outDir}`);
})();
