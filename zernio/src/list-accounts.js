import { zernio } from './zernio-client.js';

// Liste les comptes sociaux connectés au compte Zernio.
// Les accountId affichés ici sont à utiliser avec `npm run post`.
const { data } = await zernio.accounts.listAccounts();
const accounts = data?.accounts ?? data ?? [];

if (!accounts.length) {
  console.log('Aucun compte social connecté. Connectez vos comptes dans le tableau de bord Zernio (https://zernio.com).');
} else {
  console.log('Comptes connectés :');
  for (const acc of accounts) {
    console.log(`- [${acc.platform}] ${acc.displayName ?? acc.username ?? ''} — accountId: ${acc._id ?? acc.id}${acc.isActive === false ? ' (inactif)' : ''}`);
  }
}
