import { readFile, writeFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

// Prépare une variante de l'image de couverture de chaque post, l'envoie sur Zernio
// et enregistre son URL dans le post :
//   story  : image 1080x1920, champ "story"
//   google : image 1200x900 pour Google Business Profile, champ "google.image"
//
// Usage : npm run stories -- posts/<fichier>.json [...]
//         npm run google -- posts/<fichier>.json [...]

const KINDS = {
  story: { script: 'visuels/generate-stories.cjs', prefix: 'story-', set: (post, url) => { post.story = url; }, has: (post) => post.story },
  google: { script: 'visuels/generate-google.cjs', prefix: 'google-', set: (post, url) => { if (post.google) post.google.image = url; }, has: (post) => post.google?.image },
};
const [kindName, ...files] = process.argv.slice(2);
const kind = KINDS[kindName];
if (!kind || !files.length) {
  console.error('Usage : node src/add-variants.js <story|google> posts/<fichier>.json [...]');
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
      console.warn(`⚠️  ${post.date} : couverture introuvable en local, ignoré`);
      continue;
    }
    if (kindName === 'google' && !post.google) continue;
    post._local = path.join(path.dirname(cover), `${kind.prefix}${path.basename(cover)}`);
    if (!existsSync(post._local)) toRender.add(cover);
  }
}

if (toRender.size) {
  execFileSync('node', [kind.script, ...toRender], { stdio: 'inherit', env: { ...process.env, NODE_PATH: nodePath } });
}
const dirs = new Set(calendars.flatMap((c) => c.posts.filter((p) => p._local).map((p) => path.dirname(p._local))));
for (const dir of dirs) execFileSync('npm', ['run', '-s', 'upload', '--', dir], { stdio: 'inherit' });

const { byPath } = await loadUrls();
for (const { file, posts } of calendars) {
  for (const post of posts) {
    if (post._local) kind.set(post, byPath[post._local]);
    delete post._local;
  }
  await writeFile(file, JSON.stringify(posts, null, 2) + '\n');
  console.log(`✅ ${file} : ${posts.filter(kind.has).length}/${posts.length} variantes « ${kindName} » prêtes`);
}
