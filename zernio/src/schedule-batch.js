import { readFile } from 'node:fs/promises';
import { zernio, findProfile, DEFAULT_PROFILE } from './zernio-client.js';

// Programme tous les posts d'un fichier de calendrier (ex. posts/novembre-2026.json) sur le profil par défaut.
//
// Usage :
//   npm run schedule -- posts/novembre-2026.json [--profile "<nom>"] [--dry-run]
//
// Chaque post est un objet { date, content, media: [urls publiques] }.
// Instagram exige une image ou une vidéo : un post sans media part uniquement sur les autres plateformes.
// Les posts dont la date est déjà passée sont ignorés.

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--') && args[args.indexOf(a) - 1] !== '--profile');
const profileArg = args.includes('--profile') ? args[args.indexOf('--profile') + 1] : DEFAULT_PROFILE;
const dryRun = args.includes('--dry-run');

if (!file) {
  console.error('Usage : npm run schedule -- posts/<fichier>.json [--profile "<nom>"] [--dry-run]');
  process.exit(1);
}

const posts = JSON.parse(await readFile(file, 'utf8'));
let profile;
try {
  profile = await findProfile(profileArg);
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
const accounts = profile.accounts.filter((acc) => acc.isActive !== false);
const mediaType = (url) =>
  /\.(mp4|mov|webm|m4v)(\?|$)/i.test(url) ? 'video' : /\.gif(\?|$)/i.test(url) ? 'gif' : 'image';

console.log(`Profil "${profile.name}" — ${posts.length} posts${dryRun ? ' (--dry-run : rien ne sera envoyé)' : ''}\n`);

let scheduled = 0;
for (const post of posts) {
  const label = `${post.date} — ${post.theme ?? post.content.split('\n')[0].slice(0, 60)}`;
  if (new Date(post.date) <= new Date()) {
    console.log(`⏭️  ${label} : date passée, ignoré`);
    continue;
  }
  const media = post.media ?? [];
  const targets = accounts.filter((acc) => media.length || acc.platform !== 'instagram');
  if (!targets.length) {
    console.log(`⚠️  ${label} : aucun compte possible sans visuel, ignoré`);
    continue;
  }
  const body = {
    content: post.content,
    profileId: profile._id,
    platforms: targets.map((acc) => ({ platform: acc.platform, accountId: acc._id })),
    scheduledFor: post.date,
    timezone: 'Europe/Paris',
  };
  if (media.length) body.mediaItems = media.map((url) => ({ type: mediaType(url), url }));

  const where = targets.map((acc) => acc.platform).join(' + ');
  const note = media.length ? '' : ' (pas de visuel → sans Instagram)';
  if (dryRun) {
    console.log(`🧪 ${label} → ${where}${note}`);
    continue;
  }
  const { data, error } = await zernio.posts.createPost({ body });
  if (error) {
    console.error(`❌ ${label} : ${JSON.stringify(error)}`);
    continue;
  }
  scheduled++;
  console.log(`✅ ${label} → ${where}${note} (id: ${data?.post?._id ?? data?._id})`);
}

if (!dryRun) console.log(`\n${scheduled}/${posts.length} posts programmés.`);
