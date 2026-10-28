import { zernio, findProfile } from './zernio-client.js';

// Publie ou programme un post sur les comptes d'un profil (une entreprise) ou sur des comptes précis.
//
// Usage :
//   npm run post -- --content "Texte du post" (--profile "<nom du profil>" [--only instagram,facebook] | --account <platform>:<accountId> ...)
//                   [--media <url publique> ...] [--schedule 2026-11-01T10:00:00+01:00 | --now] [--dry-run]
//
// --profile  cible tous les comptes actifs du profil Zernio (ex. "Construisez", "Atelier Baratte").
// --only     limite --profile à certaines plateformes.
// --media    image ou vidéo accessible publiquement (obligatoire pour Instagram), répétable.
// --dry-run  affiche la requête sans rien envoyer à Zernio.
// Sans --schedule ni --now, le post est créé en brouillon dans Zernio.

const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
};
const getAll = (flag) =>
  args.flatMap((a, i) => (a === flag && args[i + 1] ? [args[i + 1]] : []));

const content = get('--content');
const profileArg = get('--profile');
const only = get('--only')?.split(',').map((s) => s.trim().toLowerCase());
const accountArgs = getAll('--account');
const scheduledFor = get('--schedule');
const publishNow = args.includes('--now');
const dryRun = args.includes('--dry-run');

if (!content || (!profileArg && !accountArgs.length)) {
  console.error('Arguments requis : --content "..." et --profile "<nom>" ou au moins un --account <platform>:<accountId>');
  console.error('Lancez `npm run accounts` pour voir les profils et les accountId.');
  process.exit(1);
}
if (publishNow && scheduledFor) {
  console.error('--now et --schedule sont incompatibles.');
  process.exit(1);
}

const platforms = accountArgs.map((pair) => {
  const [platform, accountId] = pair.split(':');
  if (!platform || !accountId) {
    console.error(`Format invalide pour --account "${pair}" (attendu <platform>:<accountId>)`);
    process.exit(1);
  }
  return { platform, accountId };
});

const body = { content };

if (profileArg) {
  let profile;
  try {
    profile = await findProfile(profileArg);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
  body.profileId = profile._id;
  const targets = profile.accounts.filter(
    (acc) => acc.isActive !== false && (!only || only.includes(acc.platform)),
  );
  if (!targets.length) {
    console.error(`Aucun compte actif${only ? ` (${only.join(', ')})` : ''} dans le profil "${profile.name}".`);
    process.exit(1);
  }
  for (const acc of targets) platforms.push({ platform: acc.platform, accountId: acc._id });
  console.log(`Profil "${profile.name}" : ${targets.map((a) => `${a.platform} @${a.username}`).join(', ')}`);
}

body.platforms = platforms;

const mediaUrls = getAll('--media');
if (mediaUrls.length) {
  body.mediaItems = mediaUrls.map((url) => ({
    type: /\.(mp4|mov|webm|m4v)(\?|$)/i.test(url) ? 'video' : /\.gif(\?|$)/i.test(url) ? 'gif' : 'image',
    url,
  }));
} else if (platforms.some((p) => p.platform === 'instagram')) {
  console.warn('Attention : Instagram exige une image ou une vidéo. Ajoutez --media <url publique>.');
}
if (publishNow) body.publishNow = true;
else if (scheduledFor) {
  body.scheduledFor = scheduledFor;
  body.timezone = 'Europe/Paris';
} else body.isDraft = true;

if (dryRun) {
  console.log('--dry-run : rien n\'a été envoyé. Requête qui serait envoyée :');
  console.log(JSON.stringify(body, null, 2));
  process.exit(0);
}

const { data } = await zernio.posts.createPost({ body });
const post = data?.post ?? data;
console.log(`Post créé (id: ${post?._id ?? post?.id ?? 'inconnu'})`);
console.log(publishNow ? 'Publication immédiate demandée.' : scheduledFor ? `Programmé pour ${scheduledFor} (Europe/Paris).` : 'Enregistré en brouillon.');
