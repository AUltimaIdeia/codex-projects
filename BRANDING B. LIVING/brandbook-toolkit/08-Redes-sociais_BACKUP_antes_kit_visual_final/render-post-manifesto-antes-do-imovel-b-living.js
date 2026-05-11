const { chromium } = require("playwright");
const path = require("path");

async function main() {
  const htmlPath = path.resolve(__dirname, "post-manifesto-antes-do-imovel-b-living.html");
  const outputPath = path.resolve(__dirname, "post-manifesto-antes-do-imovel-b-living.png");

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 2160, height: 2700 },
    deviceScaleFactor: 1,
  });

  await page.goto(`file://${htmlPath.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
  await page.screenshot({ path: outputPath, fullPage: false, type: "png" });
  await browser.close();

  console.log(outputPath);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
