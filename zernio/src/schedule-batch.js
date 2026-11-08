import { readFile } from 'node:fs/promises';
import { zernio, findProfile, DEFAULT_PROFILE } from './zernio-client.js';

// Programme tous les posts d'un fichier de calendrier (ex. posts/novembre-2026.json) sur le profil par défaut.
//
// Usage :
//   npm run schedule -- posts/<fichier>.json [--profile "<nom>"] [--dry-run] [--stories-only]
//
// Chaque post est un objet { date, content, media: [urls publiques], story?: url }.
// Instagram exige une image ou une vidéo : un post sans media part uniquement sur les autres plateformes.
// Si le post a une story (voir `npm run stories`), elle est publiée 5 minutes après le post,
// sur Instagram et Facebook. --stories-only programme uniquement les stories (posts déjà programmés).
// Si un compte Google Business Profile est connecté et que le post a une version "google"
// (voir `npm run google`), elle est publiée à la même heure avec un bouton vers construisez.fr.
// --google-only programme uniquement les versions Google.
// Les posts dont la date est déjà passée sont ignorés.

const STORY_DELAY_MS = 5 * 60 * 1000;

// Lieu Instagram par ville (champ "city" du post) : identifiant de la page Facebook du lieu.
// N'ajouter que des identifiants vérifiés : un identifiant invalide fait échouer la publication.
// Les stories n'acceptent pas de lieu.
const LOCATIONS = JSON.parse(await readFile(new URL('../posts/lieux.json', import.meta.url), 'utf8').catch(() => '{}'));

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--') && args[args.indexOf(a) - 1] !== '--profile');
const profileArg = args.includes('--profile') ? args[args.indexOf('--profile') + 1] : DEFAULT_PROFILE;
const dryRun = args.includes('--dry-run');
const storiesOnly = args.includes('--stories-only');
const googleOnly = args.includes('--google-only');
const GOOGLE_URL = 'https://www.construisez.fr/?utm_source=google&utm_medium=gbp&utm_campaign=posts';

if (!file) {
  console.error('Usage : npm run schedule -- posts/<fichier>.json [--profile "<nom>"] [--dry-run] [--stories-only]');
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
const active = profile.accounts.filter((acc) => acc.isActive !== false);
const google = active.find((acc) => acc.platform === 'googlebusiness');
const accounts = active.filter((acc) => acc.platform !== 'googlebusiness');
const mediaType = (url) =>
  /\.(mp4|mov|webm|m4v)(\?|$)/i.test(url) ? 'video' : /\.gif(\?|$)/i.test(url) ? 'gif' : 'image';

const isOnline = async (url) => (await fetch(url, { method: 'HEAD' }).catch(() => null))?.ok;

console.log(`Profil "${profile.name}" — ${posts.length} posts${dryRun ? ' (--dry-run : rien ne sera envoyé)' : ''}${storiesOnly ? ' (stories uniquement)' : ''}${googleOnly ? ' (Google uniquement)' : ''}\n`);

let scheduled = 0;
let stories = 0;
let googlePosts = 0;
for (const post of posts) {
  const label = `${post.date} — ${post.theme ?? post.content.split('\n')[0].slice(0, 60)}`;

  if (!storiesOnly && !googleOnly) {
    if (new Date(post.date) <= new Date()) {
      console.log(`⏭️  ${label} : date passée, ignoré`);
      continue;
    }
    const media = post.media ?? [];
    const broken = [];
    for (const url of media) if (!(await isOnline(url))) broken.push(url);
    if (broken.length) {
      console.log(`❌ ${label} : image introuvable, ignoré (${broken.join(', ')})`);
      continue;
    }
    const targets = accounts.filter((acc) => media.length || acc.platform !== 'instagram');
    if (!targets.length) {
      console.log(`⚠️  ${label} : aucun compte possible sans visuel, ignoré`);
      continue;
    }
    const body = {
      content: post.content,
      profileId: profile._id,
      platforms: targets.map((acc) => ({
        platform: acc.platform,
        accountId: acc._id,
        ...(acc.platform === 'instagram' && LOCATIONS[post.city] ? { platformSpecificData: { locationId: LOCATIONS[post.city] } } : {}),
      })),
      scheduledFor: post.date,
      timezone: 'Europe/Paris',
    };
    if (media.length) body.mediaItems = media.map((url) => ({ type: mediaType(url), url }));

    const where = targets.map((acc) => acc.platform).join(' + ');
    const note = media.length ? '' : ' (pas de visuel → sans Instagram)';
    if (dryRun) {
      console.log(`🧪 ${label} → ${where}${note}`);
    } else {
      const { data, error } = await zernio.posts.createPost({ body });
      if (error) {
        console.error(`❌ ${label} : ${JSON.stringify(error)}`);
        continue;
      }
      scheduled++;
      console.log(`✅ ${label} → ${where}${note} (id: ${data?.post?._id ?? data?._id})`);
    }
  }

  if (post.google?.image && (googleOnly || !storiesOnly) && new Date(post.date) > new Date()) {
    if (!google) {
      if (googleOnly) console.log(`⚠️  Google ${label} : aucun compte Google Business Profile connecté`);
    } else if (!(await isOnline(post.google.image))) {
      console.log(`❌ Google ${label} : image introuvable (${post.google.image})`);
    } else {
      const googleBody = {
        content: post.google.content,
        profileId: profile._id,
        platforms: [{
          platform: 'googlebusiness',
          accountId: google._id,
          platformSpecificData: { languageCode: 'fr', callToAction: { type: 'LEARN_MORE', url: GOOGLE_URL } },
        }],
        mediaItems: [{ type: 'image', url: post.google.image }],
        scheduledFor: post.date,
        timezone: 'Europe/Paris',
      };
      if (dryRun) {
        console.log(`🧪 Google ${label} → googlebusiness`);
      } else {
        const { data, error } = await zernio.posts.createPost({ body: googleBody });
        if (error) console.error(`❌ Google ${label} : ${JSON.stringify(error)}`);
        else {
          googlePosts++;
          console.log(`✅ Google ${label} (id: ${data?.post?._id ?? data?._id})`);
        }
      }
    }
  }

  if (!post.story || googleOnly) continue;
  const storyDate = new Date(new Date(post.date).getTime() + STORY_DELAY_MS);
  if (storyDate <= new Date()) {
    console.log(`⏭️  story ${label} : date passée, ignorée`);
    continue;
  }
  if (!(await isOnline(post.story))) {
    console.log(`❌ story ${label} : image introuvable (${post.story})`);
    continue;
  }
  const storyTargets = accounts.filter((acc) => ['instagram', 'facebook'].includes(acc.platform));
  const storyBody = {
    content: '',
    profileId: profile._id,
    platforms: storyTargets.map((acc) => ({ platform: acc.platform, accountId: acc._id, platformSpecificData: { contentType: 'story' } })),
    mediaItems: [{ type: 'image', url: post.story }],
    scheduledFor: storyDate.toISOString(),
    timezone: 'Europe/Paris',
  };
  if (dryRun) {
    console.log(`🧪 story ${label} → ${storyTargets.map((a) => a.platform).join(' + ')} à ${storyDate.toLocaleTimeString('fr-FR', { timeZone: 'Europe/Paris', hour: '2-digit', minute: '2-digit' })}`);
    continue;
  }
  const { data, error } = await zernio.posts.createPost({ body: storyBody });
  if (error) {
    console.error(`❌ story ${label} : ${JSON.stringify(error)}`);
    continue;
  }
  stories++;
  console.log(`✅ story ${label} (id: ${data?.post?._id ?? data?._id})`);
}

if (!dryRun) console.log(`\n${scheduled} posts, ${stories} stories et ${googlePosts} posts Google programmés.`);
