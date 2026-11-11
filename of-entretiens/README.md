# Site OF ENTRETIENS

- `site/` : le site tel qu'il est publié (déposer **ce dossier** sur Netlify).
- `docs/base-de-reference.md` : document interne (faits confirmés, points à valider).
  Il n'est **pas** publié — l'ancien déploiement le rendait accessible en ligne.

## Mise en ligne (Netlify, glisser-déposer)

1. Netlify → site *ofentretiens* → **Deploys** → glisser le dossier `site/`
   (ou le zip `of-entretiens-site.zip`).
2. Formulaire de devis (Netlify Forms) : **Forms** → activer *Form detection*, puis
   **Forms → Notifications** → ajouter une notification e-mail vers
   mike.ofentretiens@gmail.com. Les demandes arrivent aussi dans l'onglet *Forms*.

## Nom de domaine

Le site est publié sur https://www.ofentretiens.com/ (projet Netlify *ofentretiens*).
Cette adresse est écrite dans les balises canonical, Open Graph, le JSON-LD,
`sitemap.xml` et `robots.txt` : la changer partout si le domaine change.
