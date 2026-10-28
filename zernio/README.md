# Zernio — réseaux sociaux de Construisez

Outils en ligne de commande pour publier et programmer les posts de **Construisez**
(permis de construire en Île-de-France) via l'API [Zernio](https://zernio.com).

Par défaut, `npm run post` publie sur les comptes du profil Zernio **Construisez** :

- Instagram `@permis_de_construire_idf`
- Facebook `Construisez.idf`

La clé API ne doit **jamais** apparaître dans des pages web ni être committée.
Ces scripts s'exécutent en local (ou dans une CI) avec la clé dans un fichier `.env`
ignoré par git.

## Mise en place

```bash
cd zernio
npm install
cp .env.example .env
# puis renseignez ZERNIO_API_KEY dans .env
```

## Utilisation

Lister les profils, leurs comptes et leurs `accountId` :

```bash
npm run accounts
```

Vérifier un post sans rien envoyer (`--dry-run`) :

```bash
npm run post -- --content "Votre permis de construire en Île-de-France 🏗️" --media https://exemple.fr/plan.jpg --dry-run
```

Programmer un post sur Instagram et Facebook (heure de Paris) :

```bash
npm run post -- --content "Dépôt de permis de construire : on s'occupe de tout" --media https://exemple.fr/plan.jpg --schedule "2026-11-03T10:00:00+01:00"
```

Publier immédiatement, sur Facebook seulement :

```bash
npm run post -- --only facebook --content "Nouveau projet accepté en mairie ✅" --now
```

Sans `--schedule` ni `--now`, le post est créé en brouillon dans Zernio.

Instagram exige au moins une image ou une vidéo : passez son URL publique avec `--media`
(option répétable pour un carrousel).

### Programmer un calendrier de posts

Les posts prêts à l'emploi sont dans `posts/` (ex. `posts/novembre-2026.json` : 8 posts,
mardi et jeudi à 18h30). Chaque post a une date, un texte, une idée de visuel et une liste
`media` à remplir avec les URL publiques des images.

```bash
npm run schedule -- posts/novembre-2026.json --dry-run   # vérifier
npm run schedule -- posts/novembre-2026.json             # programmer
```

Un post sans image part uniquement sur Facebook (Instagram exige un visuel).
Les posts dont la date est passée sont ignorés.

### Autres profils

Le profil ciblé par défaut se change avec `ZERNIO_PROFILE` dans `.env`, ou ponctuellement
avec `--profile "<nom>"` (créez le profil et connectez ses comptes dans le tableau de bord
Zernio). On peut aussi viser des comptes précis avec `--account <platform>:<accountId>`.

## Référence

- Quickstart : https://zernio.com/agent-quickstart.md
- API complète : https://zernio.com/llms.txt · OpenAPI : https://zernio.com/openapi.yaml
- SDK Node : [`@zernio/node`](https://www.npmjs.com/package/@zernio/node)
