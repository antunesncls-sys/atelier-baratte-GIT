# JMC Couverture — refonte SEO de jmccouverture.com

Site statique (HTML/CSS, sans dépendance) prêt à déployer sur Netlify, OVH ou tout hébergement.

## Structure
- Les URL de l'ancien site sont **conservées** (`/charpente/`, `/couverture/`, `/zinguerie/`, `/nos-references/`, `/contact/`) pour garder le référencement acquis.
- Nouvelles pages ciblant des requêtes locales : `/urgence-fuite-toiture/`, `/zones-intervention/`, plus `/mentions-legales/`, `/merci/`, `/404.html`.
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
- Photos : les déposer dans `assets/photos/` avec les noms indiqués dans `assets/photos/LISEZMOI.txt`, puis relancer le build. Elles s'intègrent automatiquement (accueil, couverture, zinguerie, références, contact).
- Formulaire : fonctionne nativement sur Netlify (Netlify Forms). Ailleurs, brancher un service d'envoi.
- Créer / mettre à jour la fiche Google Business Profile avec exactement les mêmes nom, adresse et téléphone.
