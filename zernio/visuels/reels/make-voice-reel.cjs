// Monte une vidéo verticale 1080x1920 racontée par une voix : une image plein écran par phrase,
// léger mouvement de caméra, sous-titre synchronisé, « MAIS » et « DONC » mis en avant.
// Usage : node visuels/reels/make-voice-reel.cjs visuels/reels/<nom>.json
//
// Le JSON : { "beats": [ { "img": "brand/photos/projets/x.webp", "audio": "reels/voix/l00.mp3", "text": "…",
//   "from": 0.45, "to": 0.55,   // centre du cadrage, en fraction de la largeur de l'image (début → fin)
//   "cy": 0.55,                 // hauteur du sujet dans l'image (fraction), placé dans la moitié haute de l'écran
//   "fit": true,                // image entière sur fond sombre (plans), au lieu du plein écran
//   "tag": "IMAGE DU PROJET",   // petite mention en haut
//   "cta": true } ] }           // dernière image : appel à l'action et marque
// Les chemins sont relatifs à visuels/. Les textes restent dans la zone visible de TikTok et des Reels :
// rien au-dessus de y=240, rien sous y=1440, marge droite de 150 px. Écrit visuels/reels/<nom>.mp4.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { execFileSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const cfgPath = path.resolve(process.argv[2]);
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const name = path.basename(cfgPath, '.json');
const visuels = path.resolve(__dirname, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), `voice-${name}-`));
const out = path.join(__dirname, `${name}.mp4`);
const ff = (args) => execFileSync('ffmpeg', ['-v', 'error', '-y', ...args]);
const probe = (f) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
const size = (f) => execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', f]).toString().trim().split(',').map(Number);

const nb = (s) => s.replace(/ ([?!:;»])/g, '&nbsp;$1').replace(/« /g, '«&nbsp;');
const caption = (b) => nb(b.text).replace(/^(Mais|Donc)\b/, (m) => `<em>${m.toUpperCase()}</em>`).replace(/«&nbsp;([^»]+)&nbsp;»/g, '<em>«&nbsp;$1&nbsp;»</em>');

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="brand/construisez.css"><style>
body { background: transparent; padding: 0; gap: 0; }
.ov { width: 1080px; height: 1920px; position: relative; background: linear-gradient(to bottom, rgba(11,12,15,.55) 0, rgba(11,12,15,0) 420px, rgba(11,12,15,0) 880px, rgba(11,12,15,.86) 1300px, rgba(11,12,15,.94) 1920px); color: var(--fg); }
.ov.fit { background: none; }
.brand { position: absolute; left: 80px; top: 244px; display: flex; align-items: center; gap: 14px; font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .22em; text-shadow: 0 2px 12px rgba(0,0,0,.6); }
.brand img { width: 44px; height: 44px; }
.tag { position: absolute; right: 150px; top: 246px; font-family: 'IBM Plex Mono', monospace; font-size: 24px; letter-spacing: .14em; padding: 9px 16px; border-radius: 4px; background: var(--acc); }
.say { text-transform: none; position: absolute; left: 80px; right: 150px; bottom: 500px; font-family: var(--display); font-weight: var(--display-weight); letter-spacing: var(--display-track); font-size: 74px; line-height: 1.08; text-shadow: 0 3px 22px rgba(0,0,0,.75); }
.say.long { font-size: 60px; }
.say em { font-style: normal; color: var(--acc-l); }
.site { position: absolute; left: 80px; bottom: 500px; font-family: 'IBM Plex Mono', monospace; font-size: 30px; letter-spacing: .1em; color: #d5d9dd; }
.cta .say { bottom: 580px; }
</style></head><body>
${cfg.beats.map((b, i) => `<div class="ov${b.fit ? ' fit' : ''}${b.cta ? ' cta' : ''}" id="b${i}"><span class="brand"><img src="brand/logo-mark.png" alt="">CONSTRUISEZ</span>${b.tag ? `<span class="tag">${b.tag}</span>` : ''}<div class="say${b.text.length > 70 ? ' long' : ''}">${caption(b)}</div>${b.cta ? '<div class="site">construisez.fr · devis sous 24 h</div>' : ''}</div>`).join('\n')}
</body></html>`;

(async () => {
  const page = path.join(visuels, `.voice-${name}.html`);
  fs.writeFileSync(page, html);
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(pathToFileURL(page).href);
  await p.evaluate(() => document.fonts.ready);
  const low = await p.evaluate(() => Math.max(...[...document.querySelectorAll('.say, .site')].map((e) => e.getBoundingClientRect().bottom - e.closest('.ov').getBoundingClientRect().top)));
  if (low > 1440) console.warn(`⚠️  du texte descend jusqu'à y=${Math.round(low)}`);
  for (let i = 0; i < cfg.beats.length; i++) await p.locator('#b' + i).screenshot({ path: path.join(tmp, `o${i}.png`), omitBackground: true });
  await browser.close();
  fs.rmSync(page);

  const H = 2400;                                            // image plus haute que l'écran : le sujet remonte au-dessus du sous-titre
  const segs = [];
  cfg.beats.forEach((b, i) => {
    const audio = path.join(visuels, b.audio);
    const D = Math.max(1.7, probe(audio) + (b.cta ? 1.1 : 0.38));
    const src = path.join(tmp, `i${i}.png`);
    ff(['-i', path.join(visuels, b.img), src]);
    const [iw, ih] = size(src);
    let video;
    if (b.fit) {
      const h = Math.round(1080 * ih / iw / 2) * 2;
      video = `color=c=0x0b0c0f:s=1080x1920:r=30:d=${D}[bg];[0:v]scale=1080:${h},setsar=1[im];[bg][im]overlay=0:320:shortest=0[v0]`;
    } else {
      const W = Math.round(iw * H / ih / 2) * 2;
      const x = (c) => Math.min(W - 1080, Math.max(0, Math.round(c * W - 540)));
      const x0 = x(b.from ?? 0.5), x1 = x(b.to ?? b.from ?? 0.5);
      const y0 = Math.min(H - 1920 - 40, Math.max(40, Math.round((b.cy ?? 0.52) * H - 800)));
      video = `[0:v]scale=${W}:${H},setsar=1,crop=1080:1920:'${x0}+(${x1 - x0})*t/${D}':'${y0}${i % 2 ? '-' : '+'}40*t/${D}'[v0]`;
    }
    const seg = path.join(tmp, `s${i}.mp4`);
    ff(['-loop', '1', '-framerate', '30', '-t', String(D), '-i', src, '-loop', '1', '-framerate', '30', '-t', String(D), '-i', path.join(tmp, `o${i}.png`), '-i', audio,
      '-filter_complex', `${video};[v0][1:v]overlay=0:0,format=yuv420p[v];[2:a]adelay=${i ? 60 : 150}:all=1,apad,aresample=44100,aformat=channel_layouts=stereo[a]`,
      '-map', '[v]', '-map', '[a]', '-t', String(D), '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '160k', seg]);
    segs.push(seg);
  });
  const list = path.join(tmp, 'list.txt');
  fs.writeFileSync(list, segs.map((s) => `file '${s}'`).join('\n'));
  ff(['-f', 'concat', '-safe', '0', '-i', list, '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]);
  console.log(out, probe(out).toFixed(1) + ' s');
})();
