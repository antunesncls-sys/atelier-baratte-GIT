import { readFile, writeFile, readdir, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

// Prépare la version TikTok de chaque carrousel : les images 4:5 sont replacées dans un cadre vertical
// 1080x1920 (JPEG), à l'intérieur de la zone visible de TikTok, puis envoyées sur Zernio.
// Le post reçoit un champ "tiktok" : { media: [urls], content, music }.
// Les Reels (format "reel") et les posts déjà destinés à TikTok sont ignorés.
//
// Usage : npm run tiktok -- posts/<fichier>.json [...]

// Titres de la bibliothèque commerciale TikTok (voir accounts.listTikTokCommercialMusic), utilisés à tour de rôle.
const MUSIC = ['7395017880255989776', '6867622442538371073', '6716010812382644226', '7338118640749365249', '7244681450854975489'];

const files = process.argv.slice(2);
if (!files.length) {
  console.error('Usage : npm run tiktok -- posts/<fichier>.json [...]');
  process.exit(1);
}

const visuels = 'visuels';
const byUrl = {};
for (const dir of await readdir(visuels, { withFileTypes: true })) {
  const f = path.join(visuels, dir.name, 'urls.json');
  if (!dir.isDirectory() || !existsSync(f)) continue;
  for (const [name, url] of Object.entries(JSON.parse(await readFile(f, 'utf8')))) byUrl[url] = path.join(visuels, dir.name, name);
}

// Légende TikTok : l'accroche, l'appel à l'action (en commentaire plutôt qu'en message privé) et les hashtags.
const caption = (content) => {
  const blocks = content.split('\n\n');
  const cta = blocks.find((b) => b.startsWith('👉'));
  const tags = blocks.filter((b) => b.startsWith('#')).pop();
  return [blocks[0], cta, tags].filter(Boolean).join('\n\n').replace(/ en (DM|message privé)/g, ' en commentaire');
};

let n = 0;
for (const file of files) {
  const posts = JSON.parse(await readFile(file, 'utf8'));
  for (const post of posts) {
    if (post.format === 'reel' || post.platforms?.includes('tiktok') || !post.media?.length) continue;
    const locals = post.media.map((url) => byUrl[url]);
    if (locals.some((l) => !l || !/\.(png|jpe?g|webp)$/i.test(l))) {
      console.warn(`⚠️  ${post.date} : image introuvable en local, ignoré`);
      continue;
    }
    const dir = path.join(path.dirname(locals[0]), 'tiktok');
    await mkdir(dir, { recursive: true });
    const names = locals.map((l) => `${path.basename(l, path.extname(l))}.jpg`);
    locals.forEach((l, i) => {
      const out = path.join(dir, names[i]);
      if (existsSync(out)) return;
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', l, '-vf',
        'scale=994:1242:force_original_aspect_ratio=decrease,pad=1080:1920:16+(994-iw)/2:200+(1242-ih)/2:color=0x0b0c0f',
        '-q:v', '2', out]);
    });
    execFileSync('npm', ['run', '-s', 'upload', '--', dir], { stdio: 'ignore' });
    const urls = JSON.parse(await readFile(path.join(dir, 'urls.json'), 'utf8'));
    post.tiktok = { media: names.map((name) => urls[name]), content: caption(post.content), music: post.tiktok?.music ?? MUSIC[n % MUSIC.length] };
    n++;
    console.log(`✅ ${post.date} : ${names.length} images`);
  }
  await writeFile(file, JSON.stringify(posts, null, 2) + '\n');
}
console.log(`\n${n} versions TikTok prêtes.`);
