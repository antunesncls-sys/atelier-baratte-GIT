import 'dotenv/config';
import Zernio from '@zernio/node';

if (!process.env.ZERNIO_API_KEY) {
  console.error('ZERNIO_API_KEY manquante. Copiez .env.example vers .env et renseignez votre clé.');
  process.exit(1);
}

export const zernio = new Zernio();

export const DEFAULT_PROFILE = process.env.ZERNIO_PROFILE || 'Construisez';

const idOf = (ref) => (typeof ref === 'object' && ref ? ref._id : ref);

// Profils Zernio (un par entreprise) avec leurs comptes sociaux rattachés.
export async function getProfilesWithAccounts() {
  const [{ data: p }, { data: a }] = await Promise.all([
    zernio.profiles.listProfiles(),
    zernio.accounts.listAccounts(),
  ]);
  const accounts = a?.accounts ?? a ?? [];
  return (p?.profiles ?? p ?? []).map((profile) => ({
    ...profile,
    accounts: accounts.filter((acc) => idOf(acc.profileId) === profile._id),
  }));
}

// Retrouve un profil par son nom (insensible à la casse) ou son identifiant.
export async function findProfile(nameOrId) {
  const profiles = await getProfilesWithAccounts();
  const wanted = nameOrId.trim().toLowerCase();
  const profile = profiles.find((p) => p._id === nameOrId || p.name.toLowerCase() === wanted);
  if (!profile) {
    const names = profiles.map((p) => `"${p.name}"`).join(', ');
    throw new Error(`Profil "${nameOrId}" introuvable. Profils disponibles : ${names}`);
  }
  return profile;
}
