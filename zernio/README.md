# Zernio — réseaux sociaux de l'Atelier Baratte

Outils en ligne de commande pour publier et programmer les posts de l'Atelier Baratte
(bijouterie-horlogerie à Saint-Maur-des-Fossés) sur les réseaux sociaux via
l'API [Zernio](https://zernio.com), qui gère Instagram, Facebook, Google Business
Profile, TikTok, X/Twitter et d'autres plateformes avec une seule intégration.

Le site lui-même est statique : la clé API ne doit **jamais** apparaître dans les
pages HTML ni être committée. Ces scripts s'exécutent en local (ou dans une CI)
avec la clé dans un fichier `.env` ignoré par git.

## Mise en place

```bash
cd zernio
npm install
cp .env.example .env
# puis renseignez ZERNIO_API_KEY dans .env
```

Connectez d'abord vos comptes sociaux dans le tableau de bord Zernio
(https://zernio.com), sinon aucune publication n'est possible.

## Utilisation

Lister les comptes connectés et leurs `accountId` :

```bash
npm run accounts
```

Créer un brouillon :

```bash
npm run post -- --content "Changement de pile de montre en 10 minutes à Saint-Maur ⌚" --account instagram:acc_xxx
```

Programmer un post (heure de Paris) :

```bash
npm run post -- --content "Rachat d'or : estimation gratuite à l'atelier" --account facebook:acc_yyy --schedule "2026-11-03T10:00:00+01:00"
```

Publier immédiatement :

```bash
npm run post -- --content "L'atelier est ouvert ce samedi !" --account instagram:acc_xxx --account facebook:acc_yyy --now
```

## Référence

- Quickstart : https://zernio.com/agent-quickstart.md
- API complète : https://zernio.com/llms.txt · OpenAPI : https://zernio.com/openapi.yaml
- SDK Node : [`@zernio/node`](https://www.npmjs.com/package/@zernio/node)
