# NA Studio — site commercial

Site commercial présentant l'offre de création de sites internet et d'applications de gestion (artisans, TPE & PME, Île-de-France).

Pages : `index.html` (accueil), `sites.html` (catégorie sites web + portfolio), `applications.html` (catégorie applications : devis/facturation Atelier Baratte, bons de commande, Excel communicant, écrans d'entrepôt, flotte & réparations). CSS partagé dans `assets/style.css`.

## Avant mise en ligne — placeholders à remplacer

| Élément | Valeur actuelle (factice) | Où |
|---|---|---|
| Email | `contact@na-studio.fr` | `index.html` : section contact, footer, JSON-LD (`email`), liens `mailto:` — aussi dans `llms.txt` |
| Domaine | — | ajouter `<link rel="canonical">` + `og:url` dans le `<head>`, et le `Sitemap:` dans `robots.txt` |
| Mentions légales | lien `#` | créer la page (raison sociale, SIRET, hébergeur) et pointer le lien du footer |

Pas de téléphone affiché (choix assumé) : le contact passe par le formulaire et l'email. Si un numéro arrive un jour, l'ajouter dans la section contact, le footer, le JSON-LD (`telephone`) et `llms.txt` — c'est un plus pour le SEO local (cohérence NAP avec la fiche Google).

## Déploiement

Hébergement statique (Netlify recommandé : le formulaire utilise déjà `data-netlify="true"`, les envois arrivent dans l'onglet Forms sans aucune configuration). Publier le dossier `nastudio/` tel quel.

## Après mise en ligne (SEO / GEO)

1. Créer la fiche **Google Business Profile** (catégorie « Concepteur de sites web »), même téléphone/nom que le site.
2. Déclarer le site dans **Google Search Console** + envoyer un sitemap.
3. Inscrire l'entreprise sur 3–4 annuaires cohérents (CCI, PagesJaunes, LinkedIn) avec le même NAP.
4. Demander un lien « Site réalisé par NA Studio » en footer des sites clients (4 backlinks immédiats).
5. Collecter les premiers avis Google clients.
