// Fabrique un carrousel « éditorial » clair (grand titre en italique, phrases courtes) à partir d'un fichier JSON.
// Usage : node visuels/make-editorial.cjs visuels/editorial/<nom>.json
//
// Le JSON : { "kicker": "AVANT DE DÉPOSER", "title": "…", "sub": "…",
//   "steps": [ { "title": "…", "text": ["ligne", "ligne", "", "ligne"], "quote": "…" } ],   // "" = saut de paragraphe
//   "end": "…", "meta": ["Île-de-France.", "construisez.fr"], "cta": "Écrivez « DOSSIER » en commentaire" }
//
// Écrit :
//   visuels/<nom>/<nom>-eN.png          1080x1350, pour Instagram et Facebook
//   visuels/<nom>/tiktok/<nom>-eN.jpg   1080x1920, pour TikTok (textes dans la zone visible)
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const cfgPath = path.resolve(process.argv[2]);
const d = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const name = path.basename(cfgPath, '.json');
const visuels = __dirname;
const nb = (s) => s.replace(/ ([?!:;»])/g, '&nbsp;$1').replace(/« /g, '«&nbsp;');
const total = d.steps.length + 2;
const head = (i) => `<div class="head"><span>ÉDUCATIF · ${i}/${total}</span><b><img src="brand/logo-mark.png" alt="">CONSTRUISEZ</b></div>`;
const paras = (lines) => lines.join('\n').split('\n\n').map((p) => `<p>${nb(p).replace(/\n/g, '<br>')}</p>`).join('\n  ');

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="brand/construisez.css"><style>
@font-face { font-family: 'Newsreader'; font-style: italic; font-weight: 500; src: url('brand/fonts/newsreader-latin-italic-500.woff2') format('woff2'); }
/* Zone visible TikTok : y entre 220 et 1440, marge droite 160 px. La version Instagram recadre y 160 → 1510. */
.slide.ed { width: 1080px; height: 1920px; padding: 0 160px 180px 110px; background: #f4f2ee; color: #1c1d21; display: flex; flex-direction: column; justify-content: center; }
.ed .head { position: absolute; left: 110px; right: 160px; top: 230px; display: flex; justify-content: space-between; align-items: center; font-family: 'IBM Plex Mono', monospace; font-size: 26px; letter-spacing: .22em; color: #8a8c92; }
.ed .head b { font-family: 'Public Sans', sans-serif; font-weight: 700; color: #1c1d21; letter-spacing: .26em; display: flex; align-items: center; gap: 14px; }
.ed .head img { width: 40px; height: 40px; }
.ed .num { font-family: 'Newsreader', Georgia, serif; font-style: italic; font-size: 48px; color: #3e6b5c; margin-bottom: 26px; }
.ed h1 { font-family: 'Newsreader', Georgia, serif; font-style: italic; font-weight: 500; font-size: 118px; line-height: 1.05; letter-spacing: -.015em; color: #1c1d21; }
.ed h1.big { font-size: 126px; }
.ed .rule { width: 70px; height: 2px; background: #3e6b5c; margin: 52px 0 46px; }
.ed .kick + .rule { margin: 0 0 44px; background: #c9c6bf; }
.ed p { font-family: 'Public Sans', sans-serif; font-size: 44px; line-height: 1.55; color: #4a4c52; }
.ed p + p { margin-top: 34px; }
.ed .sub { font-family: 'Newsreader', Georgia, serif; font-style: italic; font-size: 50px; line-height: 1.3; color: #6b6d73; margin-top: 54px; }
.ed blockquote { margin-top: 58px; padding-left: 44px; border-left: 2px solid #c9c6bf; font-family: 'Newsreader', Georgia, serif; font-style: italic; font-size: 56px; line-height: 1.3; color: #5d5f65; }
.ed .kick { font-family: 'IBM Plex Mono', monospace; font-size: 28px; letter-spacing: .22em; color: #8a8c92; margin-bottom: 30px; }
.ed .meta { font-family: 'Public Sans', sans-serif; font-size: 40px; line-height: 1.6; color: #6b6d73; margin-top: 50px; }
.ed .body { display: flex; flex-direction: column; }
.ed .cta { margin-top: 56px; align-self: flex-start; font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 40px; color: #f4f2ee; background: #3e6b5c; padding: 26px 42px; border-radius: 4px; }
</style></head><body>
<section class="slide ed" id="e1">
  ${head(1)}
  <div class="body"><div class="kick">${d.kicker}</div><div class="rule"></div>
  <h1 class="big">${nb(d.title)}</h1>
  ${d.sub ? `<div class="sub">${nb(d.sub)}</div>` : ''}</div>
</section>
${d.steps.map((s, k) => `<section class="slide ed" id="e${k + 2}">
  ${head(k + 2)}
  <div class="body"><div class="num">0${k + 1}</div>
  <h1>${nb(s.title)}</h1>
  <div class="rule"></div>
  ${paras(s.text)}
  ${s.quote ? `<blockquote>${nb(s.quote)}</blockquote>` : ''}</div>
</section>`).join('\n')}
<section class="slide ed" id="e${total}">
  ${head(total)}
  <div class="body"><div class="kick">CONSTRUISEZ</div><div class="rule"></div>
  <h1>${nb(d.end)}</h1>
  <div class="meta">${d.meta.join('<br>')}</div>
  ${d.cta ? `<div class="cta">${nb(d.cta)}</div>` : ''}</div>
</section>
</body></html>`;

(async () => {
  const page = path.join(visuels, `.editorial-${name}.html`);
  fs.writeFileSync(page, html);
  const dir = path.join(visuels, name);
  fs.mkdirSync(path.join(dir, 'tiktok'), { recursive: true });
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(pathToFileURL(page).href);
  await p.evaluate(() => document.fonts.ready);
  // Une image trop chargée est réduite jusqu'à tenir dans la zone visible (1 100 px de haut au plus)
  await p.evaluate(() => document.querySelectorAll('.body').forEach((b) => { let z = 1; while (b.getBoundingClientRect().height > 1100 && z > 0.6) { z -= 0.02; b.style.zoom = z; } }));
  // Contrôle : aucun texte hors de la zone visible (TikTok y 220 → 1440, Instagram y 160 → 1510)
  const bad = await p.evaluate(() => [...document.querySelectorAll('.slide')].flatMap((s) => {
    const top = s.getBoundingClientRect().top;
    return [...s.querySelectorAll('h1, p, blockquote, .sub, .meta, .cta, .num, .kick')].map((e) => e.getBoundingClientRect())
      .filter((r) => r.top - top < 300 || r.bottom - top > 1450).map((r) => `${s.id} : y ${Math.round(r.top - top)} → ${Math.round(r.bottom - top)}`);
  }));
  if (bad.length) console.warn('⚠️  texte hors zone :\n' + bad.join('\n'));
  for (let i = 1; i <= total; i++) {
    const full = path.join(dir, `.plein-e${i}.png`);
    await p.locator('#e' + i).screenshot({ path: full });
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', full, '-vf', 'crop=1080:1350:0:160', path.join(dir, `${name}-e${i}.png`)]);
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', full, '-q:v', '2', path.join(dir, 'tiktok', `${name}-e${i}.jpg`)]);
    fs.rmSync(full);
  }
  await browser.close();
  fs.rmSync(page);
  console.log(`${total} images dans visuels/${name}/ et visuels/${name}/tiktok/`);
})();
