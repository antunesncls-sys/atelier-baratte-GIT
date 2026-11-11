# Site OF ENTRETIENS

Site vitrine statique (HTML + CSS + JavaScript léger, sans framework), publié sur
https://www.ofentretiens.com/ via Netlify.

## Arborescence

```
of-entretiens/
├── site/                         ← dossier publié (à glisser dans Netlify)
│   ├── index.html                  accueil
│   ├── carottage-urgence-montfermeil/index.html
│   ├── corvoyage-montfermeil/index.html
│   ├── nettoyage-bureaux-montfermeil/index.html
│   ├── plateformes-logistiques/index.html
│   ├── estimation/index.html       devis en 4 étapes (Netlify Forms « estimation »)
│   ├── realisations/index.html
│   ├── qui-sommes-nous/index.html
│   ├── contact/index.html          formulaire (Netlify Forms « contact »)
│   ├── merci/index.html            confirmation (noindex)
│   ├── mentions-legales/index.html
│   ├── 404.html
│   ├── assets/
│   │   ├── style.css               feuille de styles commune (variables CSS)
│   │   ├── site.js                 menu, sous-menu, cookies (≈ 4 Ko)
│   │   ├── estimation.js           formulaire en étapes (≈ 4 Ko)
│   │   ├── fonts/                  Gabarito + Outfit (hébergées sur le site)
│   │   └── img/                    images WebP + images de partage 1200×630
│   ├── sitemap.xml · robots.txt
│   ├── _redirects                  anciennes URL → nouvelles (301)
│   ├── _headers                    sécurité + cache
│   └── netlify.toml
├── src/
│   ├── build.py                  ← génère toutes les pages (textes, en-tête, pied, JSON-LD)
│   ├── images.py                 ← recadre et convertit les photos en WebP
│   └── photos-originales/          photos JPEG d'origine
├── docs/
│   ├── base-de-reference.md        faits confirmés / à valider (interne, non publié)
│   ├── photos-a-fournir.md
│   ├── checklist-mise-en-ligne.md
│   └── apercus/
└── of-entretiens-site.zip          ← zip prêt à déposer sur Netlify
```

## Modifier le site

1. Modifier les textes dans `src/build.py` (ou le style dans `site/assets/style.css`).
2. `python3 -I src/build.py` — régénère les pages et vérifie titres (< 60 car.),
   descriptions (< 155 car.) et 600 mots minimum par page de service.
3. Refaire le zip : `cd site && zip -qr ../of-entretiens-site.zip . -x '.*'`

Photos : voir `docs/photos-a-fournir.md`. Mise en ligne : `docs/checklist-mise-en-ligne.md`.
