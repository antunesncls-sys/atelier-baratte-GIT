// Génère l'image Google Business Profile (1200x900, format 4:3) à partir de la couverture d'un post.
// Usage : node visuels/generate-google.cjs visuels/<dossier>/<couverture>.png [...]
// Écrit visuels/<dossier>/google-<couverture>.png à côté de chaque couverture.
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const covers = process.argv.slice(2);
if (!covers.length) {
  console.error('Usage : node visuels/generate-google.cjs visuels/<dossier>/<couverture>.png [...]');
  process.exit(1);
}

const css = pathToFileURL(path.join(__dirname, 'brand/construisez.css')).href;
const logo = pathToFileURL(path.join(__dirname, 'brand/logo-mark.png')).href;

const html = (cover) => `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="${css}">
<style>
  body { padding: 0; background: var(--bg); }
  .g { width: 1200px; height: 900px; position: relative; overflow: hidden; background: var(--bg); display: flex; align-items: center; justify-content: center; }
  .g::before { content: ''; position: absolute; inset: 0; background: url('${cover}') center / cover; filter: blur(40px) brightness(.35); transform: scale(1.2); }
  .card { position: relative; width: 656px; border-radius: 12px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,.6); border: 2px solid var(--line); background: var(--bg); }
  .crop { height: 731px; overflow: hidden; }
  .crop img { display: block; width: 656px; }
  .foot { height: 89px; display: flex; align-items: center; justify-content: space-between; padding: 0 55px; border-top: 2px solid var(--line);
    font-family: 'IBM Plex Mono', monospace; font-size: 16px; letter-spacing: .12em; color: var(--dim); }
  .brand { display: flex; align-items: center; gap: 11px; font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 17px; letter-spacing: .24em; color: var(--fg); }
  .brand img { width: 27px; height: 27px; }
</style></head><body>
<div class="g"><div class="card"><div class="crop"><img src="${cover}" alt=""></div>
<div class="foot"><span class="brand"><img src="${logo}" alt="">CONSTRUISEZ</span><span>construisez.fr</span></div></div></div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  const tmp = path.join(__dirname, '.google-tmp.html');
  for (const cover of covers) {
    const abs = path.resolve(cover);
    fs.writeFileSync(tmp, html(pathToFileURL(abs).href));
    await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(path.dirname(abs), `google-${path.basename(abs)}`);
    await page.locator('.g').screenshot({ path: out });
    console.log(path.relative(process.cwd(), out));
  }
  await browser.close();
  fs.rmSync(tmp, { force: true });
})();
