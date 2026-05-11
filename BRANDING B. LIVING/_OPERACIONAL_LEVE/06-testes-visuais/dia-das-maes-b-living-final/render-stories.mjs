import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import './build-map.mjs';

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  ({ chromium } = require('C:/Users/vini1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
}

const root = path.dirname(fileURLToPath(import.meta.url));
const html = path.join(root, 'index.html');
const out = path.join(root, 'renders');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(html).href, { waitUntil: 'networkidle' });

const items = [
  ['story-01', '01-antes-de-chegar.png'],
  ['story-02', '02-casa-aprendeu-ritmo.png'],
  ['story-03', '03-quartos-maiores.png'],
  ['story-04', '04-proxima-fase.png'],
  ['story-05', '05-feliz-dia-das-maes.png'],
];

for (const [id, filename] of items) {
  const locator = page.locator(`#${id}`);
  await locator.screenshot({ path: path.join(out, filename), animations: 'disabled' });
  console.log(path.join(out, filename));
}

await browser.close();
