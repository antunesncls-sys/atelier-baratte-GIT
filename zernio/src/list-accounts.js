import { getProfilesWithAccounts } from './zernio-client.js';

// Liste les profils Zernio (un par entreprise) et leurs comptes sociaux connectés.
// Le nom du profil s'utilise avec `npm run post -- --profile "<nom>"`,
// les accountId avec `--account <platform>:<accountId>`.
const profiles = await getProfilesWithAccounts();

if (!profiles.some((p) => p.accounts.length)) {
  console.log('Aucun compte social connecté. Connectez vos comptes dans le tableau de bord Zernio (https://zernio.com).');
}

for (const profile of profiles) {
  console.log(`\nProfil "${profile.name}"${profile.isDefault ? ' (par défaut)' : ''} — profileId: ${profile._id}`);
  if (!profile.accounts.length) console.log('  (aucun compte connecté)');
  for (const acc of profile.accounts) {
    const label = acc.displayName ?? acc.username ?? '';
    const handle = acc.username && acc.username !== label ? ` (@${acc.username})` : '';
    console.log(`  - [${acc.platform}] ${label}${handle} — accountId: ${acc._id}${acc.isActive === false ? ' (inactif)' : ''}`);
  }
}
