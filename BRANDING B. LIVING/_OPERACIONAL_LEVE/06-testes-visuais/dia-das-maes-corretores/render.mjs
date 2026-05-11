import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  ({ chromium } = require('C:/Users/vini1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
}

const root = path.dirname(fileURLToPath(import.meta.url));
const html = path.join(root, 'index.html');
const out = path.join(root, 'renders', 'marta-tretto-dia-das-maes.png');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(html).href, { waitUntil: 'networkidle' });
await page.locator('#story-marta-tretto').screenshot({ path: out, animations: 'disabled' });
await browser.close();

console.log(out);
