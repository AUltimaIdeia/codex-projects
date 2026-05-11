const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const htmlPath = path.join(root, "prancha-aprovacao-abertura-premium-v2.html");
const outPath = path.join(root, "previews", "brandbook-b-living-prancha-aprovacao-abertura-premium-v2.png");

fs.mkdirSync(path.dirname(outPath), { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 3840, height: 2160 },
    deviceScaleFactor: 1,
  });

  await page.goto(`file://${htmlPath.replace(/\\/g, "/")}`, {
    waitUntil: "networkidle",
  });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: outPath, fullPage: false });
  await browser.close();

  console.log(`Rendered approval board v2 to ${outPath}`);
})();
