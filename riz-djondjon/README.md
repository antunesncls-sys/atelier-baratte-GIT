# Riz Djondjon — proposition de site

Site vitrine immersif et responsive pour **Riz Djondjon**, restaurant haïtien et afro-caribéen au 291 rue Saint-Denis, Paris 2e.
Site 100 % statique (HTML, CSS et JS sans dépendance) : il s'héberge gratuitement sur Netlify, GitHub Pages, OVH, etc.

## Aperçu local

```bash
cd riz-djondjon && python3 -m http.server 8000
```

Puis ouvrir http://localhost:8000

## Contenu

| Section | Contenu |
|---|---|
| Hero | Plein écran, titre animé, parallaxe, statut **Ouvert / Fermé en direct** (heure de Paris), boutons Réserver et Uber Eats |
| La maison | Histoire, compteurs animés, services (terrasse, PMR, Wi-Fi, privatisation…) |
| La carte | Onglets (plats, à côté, douceurs, boissons), bloc commande Uber Eats, 4 formules |
| Événements | Prochain événement avec compte à rebours, **calendrier mensuel** interactif, fiche événement, ajout à Google Agenda / Apple / Outlook (.ics) |
| Instagram | Flux automatique des derniers posts (voir plus bas) |
| Avis | Les 5 avis vérifiés du site actuel |
| Nous trouver | Horaires (jour courant en surbrillance), métros, plan Google Maps, itinéraire |
| Réservation | Le module **DISH** déjà utilisé par le restaurant, ouvert dans une fenêtre sur le site |
| Contact | Formulaire (groupe, privatisation, traiteur, question) |
| Mobile | Barre d'actions fixe : Appeler · Réserver · Livraison · Y aller |

Animations : préchargement, lettres du titre, parallaxe des feuilles (inspirées du papier peint du restaurant), bandeau défilant, apparitions au scroll, curseur personnalisé et boutons magnétiques sur ordinateur. Tout est désactivé si le visiteur a choisi de réduire les animations.

## À personnaliser : tout se trouve dans `assets/js/config.js`

Les informations marquées **⚠ À VALIDER** sont des propositions :

1. **Lien Uber Eats** : remplacer la recherche par l'URL exacte de la fiche du restaurant (`links.ubereats`).
2. **Carte et prix** : plats inspirés des avis clients et des classiques haïtiens, avec des prix indicatifs.
3. **Événements** : programmation d'exemple (konpa, brunch, soup joumou…). Chaque événement a une date, des horaires, un type et une description. `recurring: "weekly"` sert pour un événement hebdomadaire.
4. **Instagram**, deux options :
   - **Automatique (recommandé)** : créer un flux gratuit sur [behold.so](https://behold.so), le connecter au compte @rizdjondjon et coller l'URL JSON dans `instagram.feedUrl`. Les nouveaux posts s'affichent alors tout seuls.
   - **Manuelle** : coller les URLs des posts choisis dans `instagram.posts`. Ils sont intégrés avec le lecteur officiel d'Instagram.
   - Sans réglage, une grille de photos du restaurant renvoie vers le profil.
5. **Formulaire** : par défaut, il ouvre la messagerie du visiteur avec le message déjà rempli. Pour un envoi direct, créer un formulaire gratuit sur [formspree.io](https://formspree.io) et coller l'URL dans `formEndpoint`.
6. **Photos** : les visuels actuels sont tirés de l'unique photo disponible sur le site eatbu. Pour un rendu vraiment immersif, prévoir un shooting (plats, salle, équipe, soirées) et remplacer les fichiers de `assets/img/` (garder les mêmes noms, en `.webp` et `.jpg`).
7. **Mentions légales** (`mentions-legales.html`) : compléter le directeur de la publication et l'hébergeur.
8. **Domaine** : mettre à jour `<link rel="canonical">` dans `index.html`.

## Sources des informations réelles

Adresse, téléphone, e-mail, horaires, liens Instagram et Facebook, module de réservation, services, moyens de paiement et avis viennent du site actuel : https://riz-djondjon.eatbu.com/?lang=fr
