# Vidéos Higgsfield pour Construisez : reprise en nouvelle session

Ce fichier permet à une nouvelle session Claude Code de reprendre le travail sans rien redemander.

## Ce que veut le client

- Des vidéos avant / après **haut de gamme**, faites **avec Higgsfield** (plan Ultra), pour Instagram, Facebook, TikTok, puis le site construisez.fr.
- C'est Claude qui fait tout : le client ne veut plus générer lui-même sur higgsfield.ai.
- Pas d'habillage « maison » (bandeaux, volets, textes superposés du script `visuels/reels/make-reel.cjs`) : il l'a refusé. Au plus, « AVANT » / « APRÈS » très discrets et le logo à la fin, à valider avec lui.
- Les volumes, la pente de toit et les ouvertures des projets ne doivent jamais changer.
- Rien ne se publie ni ne se programme sans lui montrer le résultat.

## Première chose à vérifier

La session précédente n'avait pas les outils de génération du connecteur Higgsfield. Vérifier avec ToolSearch que
`generate_image`, `generate_video`, `media_upload`, `media_confirm` et `jobs_wait` sont disponibles.
S'ils manquent encore, le dire tout de suite au client : inutile de lui redonner des consignes à copier.

Higgsfield impose de faire valider le coût en crédits avant chaque génération payante.

## Images de départ (dépôt public, branche `claude/beautiful-ritchie-9o5e4z`)

Dossier `zernio/visuels/brand/photos/projets/` :

| Fichier | Contenu |
| --- | --- |
| `sannois-rendu-avant.webp` | Sannois, maison actuelle, paysage 4:3 |
| `sannois-rendu-apres.webp` | Sannois, rendu réaliste du projet, même cadrage 4:3 |
| `sannois-rendu-9x16.webp` | Sannois, rendu réaliste vertical 9:16 (validé par le client) |
| `sannois-rue-avant.webp`, `sannois-rue-apres.webp` | Photo d'origine et photomontage SketchUp |
| `eragny-*`, `servon-*`, `argenteuil2-*` | Photos, photomontages et vues 3D des trois autres dossiers |

## Consigne d'image qui a donné un bon résultat (Nano Banana Pro, 2K)

Image de référence : le photomontage SketchUp du projet.

```
Turn this 3D model view into a realistic, natural architectural photograph. Keep exactly the same volumes, height, roof pitch, and the same position and size of every window and door, and the same street around it. Replace the 3D-model look with real materials: lightly textured off-white render, brown clay roof tiles, anthracite grey window frames, glass reflecting the sky. Natural late-afternoon light, soft consistent shadows. No text, no logo, no people.
```

Adapter les matériaux au dossier (Éragny : toiture gris anthracite, enduit blanc ; Servon : tuile plate rouge ; Argenteuil : tuile mécanique rouge, menuiseries blanches).

## Ce qui n'a pas marché

- Une seule vidéo avec la maison actuelle en image de début et le rendu en image de fin, consigne « transformation » : le toit flotte, les murs s'étirent. Le client a trouvé ça laid.
- La retouche automatique des photomontages (script supprimé) : refusée.

## Plan proposé pour la vidéo de Sannois (9:16, plans séparés, coupes franches)

1. Étendre la photo de la maison actuelle en 9:16 (ciel et route en plus, rien d'autre ne change).
2. Créer une version « tombée de la nuit » du rendu 9:16 (heure bleue, lumières intérieures allumées, architecture identique).
3. Plan 1 : lent travelling avant sur la maison actuelle, lumière froide.
4. Plan 2 : même travelling sur le rendu, lumière dorée.
5. Plan 3 : du rendu de jour au rendu du soir (seule la lumière change), mouvement de grue lent.
6. Montage bout à bout, puis validation par le client.

Avant publication : vérifier qu'aucune plaque d'immatriculation, aucun numéro de rue ni aucun nom n'est lisible.

## Publication

Voir `zernio/README.md` (Zernio : Instagram, Facebook, TikTok). Zones visibles des formats verticaux : rien au-dessus de y=240 ni sous y=1440, marge droite de 150 px.
