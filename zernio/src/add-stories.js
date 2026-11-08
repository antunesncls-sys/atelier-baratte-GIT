import { readFile, writeFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

// Prépare la story de chaque post : génère l'image 1080x1920 à partir de sa couverture,
// l'envoie sur Zernio et enregistre son URL dans le champ "story" du post.
//
// Usage : npm run stories -- posts/<fichier>.json [...]

const files = process.argv.slice(2);
if (!files.length) {
  console.error('Usage : npm run stories -- posts/<fichier>.json [...]');
  process.exit(1);
}

const visuels = 'visuels';
const loadUrls = async () => {
  const byUrl = {};
  const byPath = {};
  for (const dir of await readdir(visuels, { withFileTypes: true })) {
    const f = path.join(visuels, dir.name, 'urls.json');
    if (!dir.isDirectory() || !existsSync(f)) continue;
    for (const [name, url] of Object.entries(JSON.parse(await readFile(f, 'utf8')))) {
      const local = path.join(visuels, dir.name, name);
      byUrl[url] = local;
      byPath[local] = url;
    }
  }
  return { byUrl, byPath };
};

const nodePath = process.env.NODE_PATH || execFileSync('npm', ['root', '-g'], { encoding: 'utf8' }).trim();
let { byUrl } = await loadUrls();

const calendars = [];
const toRender = new Set();
for (const file of files) {
  const posts = JSON.parse(await readFile(file, 'utf8'));
  calendars.push({ file, posts });
  for (const post of posts) {
    const cover = byUrl[post.media?.[0]];
    if (!cover) {
      console.warn(`⚠️  ${post.date} : couverture introuvable en local, pas de story`);
      continue;
    }
    post._storyLocal = path.join(path.dirname(cover), `story-${path.basename(cover)}`);
    if (!existsSync(post._storyLocal)) toRender.add(cover);
  }
}

if (toRender.size) {
  execFileSync('node', ['visuels/generate-stories.cjs', ...toRender], { stdio: 'inherit', env: { ...process.env, NODE_PATH: nodePath } });
}
const dirs = new Set(calendars.flatMap((c) => c.posts.filter((p) => p._storyLocal).map((p) => path.dirname(p._storyLocal))));
for (const dir of dirs) execFileSync('npm', ['run', '-s', 'upload', '--', dir], { stdio: 'inherit' });

const { byPath } = await loadUrls();
for (const { file, posts } of calendars) {
  for (const post of posts) {
    if (post._storyLocal) post.story = byPath[post._storyLocal];
    delete post._storyLocal;
  }
  await writeFile(file, JSON.stringify(posts, null, 2) + '\n');
  console.log(`✅ ${file} : ${posts.filter((p) => p.story).length}/${posts.length} stories prêtes`);
}
