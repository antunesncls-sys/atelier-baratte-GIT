// Monte un Reel avant/après 1080x1920 (≈9 s) aux couleurs de Construisez.
// Usage : node visuels/reels/make-reel.cjs visuels/reels/<nom>.json
// Le JSON décrit : avant, apres (chemins d'images), fit ("cover" ou "contain"), boxHeight,
// tagAvant, tagApres, hook1, hook2, bottom1, bottom2, endKicker, endTitle, endSub, endButton.
// hook*, bottom* et endTitle acceptent <em> et <b>. Écrit visuels/reels/<nom>.mp4.
// Les textes restent dans la zone visible de TikTok et des Reels Instagram/Facebook :
// rien au-dessus de y=240 (onglets), rien sous y=1440 (légende, pseudo, musique),
// et une marge droite de 150 px (boutons j'aime / commentaire / partage).
// La photo se place sous l'accroche et rétrécit si besoin pour laisser la place au texte du bas.
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
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), `reel-${name}-`));
const out = path.join(__dirname, `${name}.mp4`);

const SAFE_BOTTOM = 1440;
const nb = (s) => s.replace(/ ([?!:;»])/g, '&nbsp;$1').replace(/« /g, '«&nbsp;');
const brand = `<span class="brand"><img src="brand/logo-mark.png" alt="">CONSTRUISEZ</span>`;

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="brand/construisez.css"><style>
body { background: transparent; padding: 0; gap: 0; }
.ov { width: 1080px; height: 1920px; position: relative; background: transparent; color: var(--fg); }
.top { position: absolute; left: 80px; right: 150px; top: 240px; }
.row { display: flex; justify-content: space-between; align-items: center; }
.tag { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 34px; letter-spacing: .16em; padding: 14px 24px; border-radius: 6px; background: rgba(11,12,15,.85); color: var(--fg); border: 2px solid var(--line); }
.tag.after { background: var(--acc); border-color: var(--acc); }
.hook { font-family: var(--display); font-weight: var(--display-weight); letter-spacing: var(--display-track); font-size: 88px; line-height: 1.02; margin-top: 26px; }
.hook em, .end h1 em { font-style: normal; color: var(--acc-l); }
.bottom { position: absolute; left: 80px; right: 150px; top: 0; font-size: 40px; line-height: 1.3; color: #d5d9dd; }
.bottom b { color: var(--fg); }
.brand { display: flex; align-items: center; gap: 14px; font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .22em; color: var(--fg); }
.brand img { width: 44px; height: 44px; }
.end { background: var(--bg); display: flex; flex-direction: column; justify-content: center; padding: 0 150px 0 90px; }
.end .site { margin-top: 80px; display: flex; gap: 36px; align-items: center; font-family: 'IBM Plex Mono', monospace; font-size: 30px; letter-spacing: .1em; color: var(--dim); }
.end .kicker { font-size: 34px; }
.end h1 { font-family: var(--display); font-weight: var(--display-weight); letter-spacing: var(--display-track); font-size: 108px; line-height: 1.02; }
.end .sub { font-size: 42px; margin-top: 40px; }
.end .btn { margin-top: 70px; font-size: 50px; padding: 34px 54px; align-self: flex-start; }
</style></head><body>
<div class="ov" id="o1"><div class="top"><div class="row"><span class="tag">${cfg.tagAvant || 'AVANT'}</span>${brand}</div><div class="hook">${nb(cfg.hook1)}</div></div><div class="bottom">${nb(cfg.bottom1)}</div></div>
<div class="ov" id="o2"><div class="top"><div class="row"><span class="tag after">${cfg.tagApres || 'APRÈS · PROJET'}</span>${brand}</div><div class="hook">${nb(cfg.hook2)}</div></div><div class="bottom">${nb(cfg.bottom2)}</div></div>
<div class="ov end" id="o3"><div class="kicker">${nb(cfg.endKicker)}</div><h1>${nb(cfg.endTitle)}</h1><div class="sub">${nb(cfg.endSub)}</div><div class="btn">${nb(cfg.endButton)}</div><div class="site">${brand}<span>construisez.fr</span></div></div>
</body></html>`;

(async () => {
  const page = path.join(visuels, `.reel-${name}.html`);
  fs.writeFileSync(page, html);
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(pathToFileURL(page).href);
  await p.evaluate(() => document.fonts.ready);
  // Place la photo sous l'accroche la plus haute, puis le texte du bas sous la photo, sans dépasser SAFE_BOTTOM.
  const { boxY, boxH, worst } = await p.evaluate(({ wanted, safeBottom }) => {
    const q = (s) => [...document.querySelectorAll(s)];
    const rel = (e) => e.getBoundingClientRect().bottom - e.closest('.ov').getBoundingClientRect().top;
    const topEnd = Math.max(...q('.ov:not(.end) .top').map(rel));
    const bottomH = Math.max(...q('.ov:not(.end) .bottom').map((e) => e.getBoundingClientRect().height));
    const boxY = Math.ceil(topEnd + 40);
    let boxH = Math.min(wanted, safeBottom - 36 - Math.ceil(bottomH) - boxY);
    boxH -= boxH % 2;
    q('.ov:not(.end) .bottom').forEach((e) => (e.style.top = `${boxY + boxH + 36}px`));
    const worst = Math.max(...q('.ov *').map(rel));
    return { boxY, boxH, worst };
  }, { wanted: cfg.boxHeight || 760, safeBottom: SAFE_BOTTOM });
  if (worst > SAFE_BOTTOM) console.warn(`⚠️  du texte descend jusqu'à y=${Math.round(worst)} (zone masquée sous ${SAFE_BOTTOM})`);
  console.log(`photo : y=${boxY}, hauteur ${boxH}px`);
  for (const id of ['o1', 'o2', 'o3']) await p.locator('#' + id).screenshot({ path: path.join(tmp, id + '.png'), omitBackground: true });
  await browser.close();
  fs.rmSync(page);

  const img = (rel, out) => execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(visuels, rel), out]);
  img(cfg.avant, path.join(tmp, 'a.png'));
  img(cfg.apres, path.join(tmp, 'b.png'));

  const W2 = 2160, H2 = boxH * 2;
  const fit = cfg.fit === 'contain'
    ? `scale=${W2}:${H2}:force_original_aspect_ratio=decrease,pad=${W2}:${H2}:(ow-iw)/2:(oh-ih)/2:color=${cfg.pad || 'white'}`
    : `scale=${W2}:${H2}:force_original_aspect_ratio=increase,crop=${W2}:${H2}`;
  const zoom = (from, to, frames) => `zoompan=z='${from}+(${to}-${from})*on/${frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames}:s=1080x${boxH}:fps=30`;
  const filter = [
    `[0:v]${fit},setsar=1,${zoom(1, 1.08, 102)}[p0]`,
    `[1:v]${fit},setsar=1,${zoom(1.08, 1, 120)}[p1]`,
    `[5:v][p0]overlay=0:${boxY}:shortest=1[a0];[a0][2:v]overlay=0:0:shortest=1,format=yuv420p,setsar=1[A]`,
    `[6:v][p1]overlay=0:${boxY}:shortest=1[b0];[b0][3:v]overlay=0:0:shortest=1,format=yuv420p,setsar=1[B]`,
    `[4:v]fps=30,format=yuv420p,setsar=1[C]`,
    `[A][B]xfade=transition=slideleft:duration=0.5:offset=2.9[AB];[AB][C]xfade=transition=fade:duration=0.4:offset=6.4,format=yuv420p[v]`,
  ].join(';');
  execFileSync('ffmpeg', ['-v', 'error', '-y',
    '-i', path.join(tmp, 'a.png'), '-i', path.join(tmp, 'b.png'),
    '-loop', '1', '-t', '3.4', '-i', path.join(tmp, 'o1.png'),
    '-loop', '1', '-t', '4.0', '-i', path.join(tmp, 'o2.png'),
    '-loop', '1', '-t', '2.8', '-i', path.join(tmp, 'o3.png'),
    '-f', 'lavfi', '-t', '3.4', '-i', 'color=c=0x0b0c0f:s=1080x1920:r=30',
    '-f', 'lavfi', '-t', '4.0', '-i', 'color=c=0x0b0c0f:s=1080x1920:r=30',
    '-f', 'lavfi', '-t', '9.2', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-filter_complex', filter, '-map', '[v]', '-map', '7:a', '-shortest',
    '-r', '30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out]);
  for (const t of [1, 5, 8.5]) execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i', out, '-frames:v', '1', path.join(tmp, `f${t}.png`)]);
  console.log(out);
  console.log(tmp);
})();
