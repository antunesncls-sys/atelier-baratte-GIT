// Génère un PNG 1080x1350 par <section class="slide" id="..."> d'un fichier HTML de visuels.
// Usage : node visuels/generate.cjs visuels/novembre-2026.html
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require('playwright');

const input = process.argv[2];
if (!input) {
  console.error('Usage : node visuels/generate.cjs visuels/<fichier>.html');
  process.exit(1);
}
const outDir = path.join(path.dirname(input), path.basename(input, '.html'));
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
  await page.goto('file://' + path.resolve(input));
  await page.evaluate(() => document.fonts.ready);
  for (const slide of await page.$$('section.slide')) {
    const id = await slide.getAttribute('id');
    const file = path.join(outDir, `${id}.png`);
    await slide.screenshot({ path: file });
    console.log(file);
  }
  await browser.close();
})();
