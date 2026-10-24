# NA Studio — site commercial

Site vitrine une page présentant l'offre de création de sites internet (artisans, TPE & PME, Île-de-France), avec portfolio des 4 réalisations en ligne.

## Avant mise en ligne — placeholders à remplacer

| Élément | Valeur actuelle (factice) | Où |
|---|---|---|
| Téléphone | `06 00 00 00 00` / `+33600000000` | `index.html` : section contact, footer, JSON-LD (`telephone`), liens `tel:` |
| Email | `contact@na-studio.fr` | `index.html` : section contact, footer, JSON-LD (`email`), liens `mailto:` |
| Domaine | — | ajouter `<link rel="canonical">` + `og:url` dans le `<head>`, et le `Sitemap:` dans `robots.txt` |
| Mentions légales | lien `#` | créer la page (raison sociale, SIRET, hébergeur) et pointer le lien du footer |

## Déploiement

Hébergement statique (Netlify recommandé : le formulaire utilise déjà `data-netlify="true"`, les envois arrivent dans l'onglet Forms sans aucune configuration). Publier le dossier `nastudio/` tel quel.

## Après mise en ligne (SEO / GEO)

1. Créer la fiche **Google Business Profile** (catégorie « Concepteur de sites web »), même téléphone/nom que le site.
2. Déclarer le site dans **Google Search Console** + envoyer un sitemap.
3. Inscrire l'entreprise sur 3–4 annuaires cohérents (CCI, PagesJaunes, LinkedIn) avec le même NAP.
4. Demander un lien « Site réalisé par NA Studio » en footer des sites clients (4 backlinks immédiats).
5. Collecter les premiers avis Google clients.
