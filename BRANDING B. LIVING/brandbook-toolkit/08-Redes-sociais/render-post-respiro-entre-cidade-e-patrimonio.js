const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const input = path.resolve(__dirname, "post-respiro-entre-cidade-e-patrimonio.html");
  const output = path.resolve(__dirname, "post-respiro-entre-cidade-e-patrimonio.png");

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 2160, height: 2700 },
    deviceScaleFactor: 1,
  });

  await page.goto(`file:///${input.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
  await page.screenshot({ path: output, fullPage: false, type: "png" });
  await browser.close();

  console.log(output);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
