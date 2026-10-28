# Zernio — publication sur les réseaux sociaux

Outils en ligne de commande pour publier et programmer des posts sur les réseaux
sociaux via l'API [Zernio](https://zernio.com), qui gère Instagram, Facebook, Google
Business Profile, TikTok, X/Twitter et d'autres plateformes avec une seule intégration.

Un même compte Zernio peut servir plusieurs entreprises : chaque entreprise a son
**profil** Zernio, et les scripts ciblent un profil par son nom.

| Profil Zernio      | Comptes connectés                                                        |
| ------------------ | ------------------------------------------------------------------------ |
| Construisez        | Instagram `@permis_de_construire_idf`, Facebook `Construisez.idf`        |
| Atelier Baratte    | à connecter                                                              |

La clé API ne doit **jamais** apparaître dans les pages du site ni être committée.
Ces scripts s'exécutent en local (ou dans une CI) avec la clé dans un fichier `.env`
ignoré par git.

## Mise en place

```bash
cd zernio
npm install
cp .env.example .env
# puis renseignez ZERNIO_API_KEY dans .env
```

Dans le tableau de bord Zernio (https://zernio.com) :

1. Renommez le profil « Default » en **Construisez** (il contient déjà les comptes Construisez).
2. Pour l'Atelier Baratte, créez un profil **Atelier Baratte** et connectez-y ses comptes.

## Utilisation

Lister les profils, leurs comptes et leurs `accountId` :

```bash
npm run accounts
```

Vérifier un post sans rien envoyer (`--dry-run`) :

```bash
npm run post -- --profile Construisez --content "Votre permis de construire en Île-de-France 🏗️" --media https://exemple.fr/plan.jpg --dry-run
```

Programmer un post sur tous les comptes d'un profil (heure de Paris) :

```bash
npm run post -- --profile Construisez --content "Dépôt de permis de construire : on s'occupe de tout" --media https://exemple.fr/plan.jpg --schedule "2026-11-03T10:00:00+01:00"
```

Publier immédiatement, sur Facebook seulement :

```bash
npm run post -- --profile Construisez --only facebook --content "Nouveau projet accepté en mairie ✅" --now
```

Sans `--schedule` ni `--now`, le post est créé en brouillon dans Zernio.
On peut aussi cibler des comptes précis avec `--account <platform>:<accountId>` au lieu de `--profile`.

Instagram exige au moins une image ou une vidéo : passez son URL publique avec `--media`
(option répétable pour un carrousel).

## Référence

- Quickstart : https://zernio.com/agent-quickstart.md
- API complète : https://zernio.com/llms.txt · OpenAPI : https://zernio.com/openapi.yaml
- SDK Node : [`@zernio/node`](https://www.npmjs.com/package/@zernio/node)
