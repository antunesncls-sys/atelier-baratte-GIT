# JMC Couverture — refonte SEO de jmccouverture.com

Site statique (HTML/CSS, sans dépendance) prêt à déployer sur Netlify, OVH ou tout hébergement.

## Structure
- Les URL de l'ancien site sont **conservées** (`/charpente/`, `/couverture/`, `/zinguerie/`, `/nos-references/`, `/contact/`) pour garder le référencement acquis.
- Nouvelles pages ciblant des requêtes locales : `/renovation-toiture/` (remplacement de toiture), `/nettoyage-toiture/` (nettoyage, démoussage), `/toiture-maison-neuve/` (particuliers qui font construire), `/zones-intervention/` (toute l'Île-de-France), plus `/mentions-legales/`, `/merci/`, `/404.html`.
- `sitemap.xml`, `robots.txt`, logo officiel 40 ans (SVG), favicons, image de partage `assets/og-jmc-couverture.jpg`.

## SEO intégré
- Title / meta description uniques par page, ciblés « couvreur + ville / département ».
- Un seul H1 par page, hiérarchie H2/H3, maillage interne entre services.
- Données structurées JSON-LD : `RoofingContractor` (NAP, zones desservies, QUALIBAT/RGE), `Service`, `FAQPage`, `BreadcrumbList`.
- Canonical, Open Graph, mobile-first, bouton d'appel fixe sur mobile, aucun JS bloquant.

## Modifier le site
Le contenu se trouve dans `_build/build.py`. Après modification :

```bash
python3 _build/build.py
```

## À compléter avant mise en ligne
- Mentions légales : SIRET, RCS, directeur de publication, assureur décennal, hébergeur.
- Photos : déjà intégrées (accueil en mosaïque, pages services). Pour en ajouter, voir `assets/photos/LISEZMOI.txt`.
- Instagram : renseigner l'adresse du compte dans `BIZ["instagram"]` (`_build/build.py`) puis relancer le build.
- Formulaire : fonctionne nativement sur Netlify (Netlify Forms). Ailleurs, brancher un service d'envoi.
- Créer / mettre à jour la fiche Google Business Profile avec exactement les mêmes nom, adresse et téléphone.
