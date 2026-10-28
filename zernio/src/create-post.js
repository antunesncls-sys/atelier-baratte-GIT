import { zernio } from './zernio-client.js';

// Publie ou programme un post sur un ou plusieurs comptes connectés.
//
// Usage :
//   npm run post -- --content "Texte du post" --account <platform>:<accountId> [--account ...] [--schedule 2026-11-01T10:00:00+01:00 | --now]
//
// Sans --schedule ni --now, le post est créé en brouillon dans Zernio.
// Exemple :
//   npm run post -- --content "Réparation d'horloges anciennes à Saint-Maur 🕰️" \
//     --account instagram:acc_xxx --account facebook:acc_yyy \
//     --schedule "2026-11-01T10:00:00+01:00"

const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
};
const getAll = (flag) =>
  args.flatMap((a, i) => (a === flag && args[i + 1] ? [args[i + 1]] : []));

const content = get('--content');
const accountArgs = getAll('--account');
const scheduledFor = get('--schedule');
const publishNow = args.includes('--now');

if (!content || !accountArgs.length) {
  console.error('Arguments requis : --content "..." et au moins un --account <platform>:<accountId>');
  console.error('Lancez `npm run accounts` pour obtenir les accountId.');
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

const body = { content, platforms };
if (publishNow) body.publishNow = true;
else if (scheduledFor) {
  body.scheduledFor = scheduledFor;
  body.timezone = 'Europe/Paris';
} else body.isDraft = true;

const { data } = await zernio.posts.createPost({ body });
const post = data?.post ?? data;
console.log(`Post créé (id: ${post?._id ?? post?.id ?? 'inconnu'})`);
console.log(publishNow ? 'Publication immédiate demandée.' : scheduledFor ? `Programmé pour ${scheduledFor} (Europe/Paris).` : 'Enregistré en brouillon.');
