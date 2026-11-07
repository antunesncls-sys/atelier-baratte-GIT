# JMC Couverture — refonte SEO de jmccouverture.com

Site statique (HTML/CSS, sans dépendance) prêt à déployer sur Netlify, OVH ou tout hébergement.

## Structure
- Les URL de l'ancien site sont **conservées** (`/charpente/`, `/couverture/`, `/zinguerie/`, `/nos-references/`, `/contact/`) pour garder le référencement acquis.
- Nouvelles pages ciblant des requêtes locales : `/renovation-toiture/` (remplacement de toiture), `/nettoyage-toiture/` (nettoyage, démoussage), `/toiture-maison-neuve/` (particuliers qui font construire), `/zones-intervention/` (toute l'Île-de-France), plus `/mentions-legales/`, `/merci/`, `/404.html`.
- `sitemap.xml`, `robots.txt`, logo officiel 40 ans (SVG), favicons, image de partage `assets/og-jmc-couverture.jpg`.

## Pages spécialités
Rénovation, isolation, maison neuve, zinc & bardage (architecte), copropriétés & syndics,
fenêtres de toit VELUX & lucarnes, nettoyage, + couverture / charpente / zinguerie.

## Pages villes (28)
Données dans `VILLES` (`_build/build.py`) : 94 (Saint-Maur, Nogent, Le Perreux), 77 (Lagny, Ozoir,
Bussy-Saint-Georges, Fontainebleau, Barbizon), 78 (Versailles, Le Vésinet, Saint-Germain-en-Laye…),
92 (Neuilly, Boulogne, Saint-Cloud, Sceaux…). Pour en ajouter une : un appel `_v(...)` avec un texte propre à la ville.

## Migration depuis l'ancien site WordPress
`_redirects` (Netlify) : 301 des anciennes pages /portfolio/, /testimonial/, /_light_image_gallery/,
/portfolio-categories/ vers les nouvelles pages ; 410 pour les pages de démo /team/ et /wp-*.
`_headers` : cache des polices et images, en-têtes de sécurité.

## Pages départements
/couvreur-seine-et-marne-77/, /couvreur-val-de-marne-94/, /couvreur-yvelines-78/,
/couvreur-hauts-de-seine-92/, /couvreur-seine-saint-denis-93/, /couvreur-paris/ (données `DEPTS_PAGES`).

## GEO (référencement dans les IA : ChatGPT, Perplexity, Gemini…)
- `llms.txt` : présentation du site pour les assistants IA (généré par le build).
- `robots.txt` : autorise explicitement les robots IA (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended…).
- Encadré « En bref » (faits citables) et date de mise à jour sur chaque page ; WebPage + dateModified en JSON-LD.
- Pages `/qui-sommes-nous/` (fiche d'identité) et `/questions-frequentes-toiture/` (toutes les FAQ).
- IndexNow : après chaque mise en ligne, lancer `python3 _build/indexnow.py` (clé dans `<clé>.txt` à la racine).

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
- Instagram : https://www.instagram.com/jmc.couverture/ (modifiable dans `BIZ["instagram"]`).
- Formulaire : fonctionne nativement sur Netlify (Netlify Forms). Ailleurs, brancher un service d'envoi.
- Créer / mettre à jour la fiche Google Business Profile avec exactement les mêmes nom, adresse et téléphone.
