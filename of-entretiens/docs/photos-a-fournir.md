# Photos à fournir — OF ENTRETIENS

Le site utilise aujourd'hui de **vraies photos de chantier**, sauf là où c'est indiqué
« provisoire ». Envoyez les photos **telles qu'elles sortent du téléphone** (JPEG, pleine
résolution) : elles sont recadrées, converties en WebP et débarrassées de leurs métadonnées
(localisation GPS comprise) par `src/images.py`.

**Règles pour toutes les photos** : lumière du jour, téléphone tenu à l'horizontale (sauf
mention contraire), aucun visage de client ou de passant reconnaissable sans accord, aucune
plaque d'immatriculation lisible, pas d'enseigne ou de logo de client sans son accord écrit.

| # | Sujet | Où sur le site | Format conseillé | Statut actuel |
|---|-------|----------------|------------------|---------------|
| 1 | L'équipe ou le véhicule devant un chantier | Premier écran de l'accueil (fond assombri) + image de partage | Paysage, 1920 × 1200 px minimum, sujet au centre | Provisoire : nettoyage de façade en nacelle (vraie photo) |
| 2 | Le directeur général ou l'équipe au travail | Bloc « Qui sommes-nous » (accueil et page dédiée) | 4:3, 1600 × 1200 px | Provisoire : logo / préparation d'un logement |
| 3 | Carottage en cours (carotteuse sur une dalle ou un voile) | Page Carottage en urgence : bandeau + carte | Paysage, 2400 × 1200 px (2:1) | Provisoire : reprise de plâtrerie autour de gaines |
| 4 | Nettoyage de bureaux en intervention | Page Nettoyage : bandeau + carte de l'accueil | Paysage, 2400 × 1200 px | **Provisoire : image Unsplash** (à remplacer en priorité) |
| 5 | Base-vie de chantier propre (vestiaire, réfectoire) | Page Nettoyage | Paysage, 1600 × 1067 px | Absente |
| 6 | 3 à 4 paires **avant / après**, même cadrage, même endroit | Galerie de l'accueil et page Réalisations | Paysage, 1600 × 1200 px | 1 paire disponible (soubassement) |
| 7 | La façade en nacelle **une fois nettoyée** | Paire avant/après avec la photo actuelle | Même cadrage que l'original | Absente |
| 8 | Une réserve avant / après levée (menuiserie, plâtrerie) | Page Corvoyage | Paysage ou portrait, 1600 px | Seulement « avant » |
| 9 | Intervention sur plateforme logistique (bureaux, signalétique, marquage au sol) | Page Plateformes logistiques | Paysage, 1600 × 1067 px | Toiture, bardage, cuve disponibles |
| 10 | Photos envoyées en conversation mais jamais reçues en fichiers (cuisine professionnelle, façades, réserves) | Galerie Réalisations | Fichiers originaux | À renvoyer en pièces jointes |

## Après réception

1. Déposer les JPEG dans `src/photos-originales/` en reprenant le nom de l'image à remplacer
   (ex. `tuile-nettoyage.jpg` pour la photo n° 4).
2. Lancer `python3 -I src/images.py src/photos-originales site/assets/img`.
3. Lancer `python3 -I src/build.py`, vérifier les pages, puis refaire le zip.
