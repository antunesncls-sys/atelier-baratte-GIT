// Génère une story 1080x1920 à partir de l'image de couverture de chaque post.
// Usage : node visuels/generate-stories.cjs visuels/<dossier>/<couverture>.png [...]
// Écrit visuels/<dossier>/story-<couverture>.png à côté de chaque couverture.
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const covers = process.argv.slice(2);
if (!covers.length) {
  console.error('Usage : node visuels/generate-stories.cjs visuels/<dossier>/<couverture>.png [...]');
  process.exit(1);
}

const css = pathToFileURL(path.join(__dirname, 'brand/construisez.css')).href;
const logo = pathToFileURL(path.join(__dirname, 'brand/logo-mark.png')).href;

const html = (cover) => `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="${css}">
<style>
  body { padding: 0; background: var(--bg); }
  .story { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: var(--bg); color: var(--fg);
    display: flex; flex-direction: column; align-items: center; padding: 150px 80px 0; }
  .story::before { content: ''; position: absolute; inset: 0; background: url('${cover}') center / cover; filter: blur(40px) brightness(.35); transform: scale(1.2); }
  .story > * { position: relative; }
  .kicker { margin: 0 0 44px; font-size: 30px; }
  .cover { width: 900px; border-radius: 14px; box-shadow: 0 40px 90px rgba(0,0,0,.6); border: 2px solid var(--line); }
  .cta { margin-top: 64px; font-family: 'Bodoni Moda', serif; font-size: 64px; font-weight: 500; text-align: center; line-height: 1.1; }
  .cta em { font-style: italic; color: var(--acc-l); }
  .foot { position: absolute; bottom: 120px; display: flex; align-items: center; gap: 18px; font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 30px; letter-spacing: .24em; }
  .foot img { width: 50px; height: 50px; }
</style></head><body>
<div class="story">
  <div class="kicker">Nouveau post</div>
  <img class="cover" src="${cover}" alt="">
  <div class="cta">À voir sur <em>notre profil</em></div>
  <div class="foot"><img src="${logo}" alt="">CONSTRUISEZ</div>
</div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const cover of covers) {
    const abs = path.resolve(cover);
    const tmp = path.join(__dirname, '.story-tmp.html');
    fs.writeFileSync(tmp, html(pathToFileURL(abs).href));
    await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(path.dirname(abs), `story-${path.basename(abs)}`);
    await page.locator('.story').screenshot({ path: out });
    console.log(path.relative(process.cwd(), out));
  }
  await browser.close();
  fs.rmSync(path.join(__dirname, '.story-tmp.html'), { force: true });
})();
