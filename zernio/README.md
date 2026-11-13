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

Les posts prêts à l'emploi sont dans `posts/` (ex. `posts/calendrier-nov-dec-2026.json` : 13 posts,
mardi et jeudi à 19h45). Chaque post a une date, un texte, une idée de visuel et une liste
`media` à remplir avec les URL publiques des images.

```bash
npm run schedule -- posts/calendrier-nov-dec-2026.json --dry-run   # vérifier
npm run schedule -- posts/calendrier-nov-dec-2026.json             # programmer
```

Un post sans image part uniquement sur Facebook (Instagram exige un visuel).
Les posts dont la date est passée, ou dont une image ne répond plus, sont ignorés.

### Stories

Chaque post a sa story (1080×1920, couverture du post + « À voir sur notre profil »),
publiée 5 minutes après le post sur Instagram et Facebook :

```bash
npm run stories -- posts/<fichier>.json                    # génère, envoie et enregistre les stories
npm run schedule -- posts/<fichier>.json                   # programme les posts et leurs stories
npm run schedule -- posts/<fichier>.json --stories-only    # stories seules (posts déjà programmés)
```

### Google Business Profile

Chaque post a aussi une version Google (champ `google` : texte court sans hashtags,
image 1200×900, bouton « En savoir plus » vers construisez.fr). Elle part à la même heure
que le post dès qu'un compte Google Business Profile est connecté au profil Zernio.

```bash
npm run google -- posts/<fichier>.json                     # génère, envoie et enregistre les images Google
npm run schedule -- posts/<fichier>.json --google-only     # programme les versions Google seules
```

Google refuse les numéros de téléphone dans le texte des posts : renvoyer vers le site.

### Créer les visuels

Les visuels (1080×1350, format portrait Instagram) sont décrits en HTML dans `visuels/`
(ex. `visuels/novembre-2026.html`, une `<section class="slide">` par image). Pour les
modifier : éditez le HTML, puis régénérez les PNG et envoyez-les sur le stockage Zernio.

```bash
npm run visuels -- visuels/novembre-2026.html   # génère visuels/novembre-2026/*.png (Playwright)
npm run upload -- visuels/novembre-2026         # envoie les PNG, URL dans visuels/novembre-2026/urls.json
```

Copiez ensuite les URL de `urls.json` dans le champ `media` des posts.

### Autres profils

Le profil ciblé par défaut se change avec `ZERNIO_PROFILE` dans `.env`, ou ponctuellement
avec `--profile "<nom>"` (créez le profil et connectez ses comptes dans le tableau de bord
Zernio). On peut aussi viser des comptes précis avec `--account <platform>:<accountId>`.

## Référence

- Quickstart : https://zernio.com/agent-quickstart.md
- API complète : https://zernio.com/llms.txt · OpenAPI : https://zernio.com/openapi.yaml
- SDK Node : [`@zernio/node`](https://www.npmjs.com/package/@zernio/node)

## Zones visibles (formats verticaux 1080x1920)

Les Reels, TikTok et stories sont recouverts par l'interface des applications. Les générateurs gardent les textes à l'intérieur :

| Format | Rien au-dessus de | Rien en dessous de | Marge droite |
| --- | --- | --- | --- |
| Reels / TikTok (`make-reel.cjs`, `tiktok-*.html`) | y = 220–240 | y = 1440 (légende, pseudo, musique) | 150 px (boutons) |
| Stories (`generate-stories.cjs`) | y = 250 (barre de progression) | y = 1650 (« Envoyer un message ») | — |

Formats : feed Instagram/Facebook 1080x1350 (4:5, la grille du profil le recadre en 3:4 : garder 90 px de marge sur les côtés), stories/Reels/TikTok 1080x1920 (9:16), Google 1200x900 (4:3), vidéos H.264 + AAC 30 i/s.
