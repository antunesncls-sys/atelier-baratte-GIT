# Checklist de mise en ligne — OF ENTRETIENS

## 1. Avant de publier (à faire valider par le dirigeant)
- [ ] Relire tous les textes (accueil, 4 pages de service, qui sommes-nous).
- [ ] Confirmer « devis gratuit et sans engagement » (affiché partout).
- [ ] Carottage : diamètres, épaisseurs, matériaux, interventions hors heures ouvrées
      (voir `docs/base-de-reference.md`). Le site n'annonce volontairement ni « 24h/24 » ni délai garanti.
- [ ] Horaires d'ouverture → à ajouter au JSON-LD de l'accueil (`openingHoursSpecification` dans `src/build.py`).
- [ ] Lien de la fiche Google Business Profile → à ajouter dans `sameAs` du JSON-LD.
- [ ] Remplacer au moins la photo provisoire Unsplash du nettoyage (voir `docs/photos-a-fournir.md`).

## 2. Publication sur Netlify
- [ ] Netlify → projet *ofentretiens* → **Deploys** → glisser `of-entretiens-site.zip`.
- [ ] **Forms** : vérifier que les formulaires `estimation` et `contact` sont détectés.
- [ ] **Forms → Notifications** : e-mail vers mike.ofentretiens@gmail.com pour chaque formulaire.
- [ ] Envoyer une demande test depuis `/estimation/` et `/contact/` (arrivée sur `/merci/` + e-mail reçu).
- [ ] Tester les anciennes adresses (doivent rediriger en 301) : `/corvoyage.html`,
      `/promoteurs.html`, `/plateformes-logistiques.html`, `/carottage-urgence.html`, `/mentions-legales.html`.
- [ ] Tester une adresse inexistante → page 404.
- [ ] **Domain management → HTTPS** : cliquer sur « Renouveler le certificat » si l'avertissement est toujours affiché.

## 3. Google Search Console
- [ ] Ajouter la propriété **Domaine** `ofentretiens.com` (vérification par enregistrement TXT dans Netlify DNS).
- [ ] **Sitemaps** : soumettre `https://www.ofentretiens.com/sitemap.xml`.
- [ ] **Inspection d'URL** : demander l'indexation de l'accueil et des 4 pages de service.
- [ ] **Pages** : vérifier après quelques jours que les anciennes URL sont bien « redirigées » et les nouvelles « indexées ».
- [ ] **Améliorations** : contrôler les données structurées (FAQ, fil d'Ariane) sans erreur.
- [ ] Optionnel : importer le site dans Bing Webmaster Tools depuis la Search Console.

## 4. Fiche Google Business Profile
- [ ] Créer ou revendiquer la fiche « OF ENTRETIENS ».
- [ ] Catégorie principale (ex. « Entreprise de nettoyage » ou « Entrepreneur général ») + catégories secondaires.
- [ ] Adresse du siège : si vous ne recevez pas de clients sur place, **masquer l'adresse** et définir une **zone desservie** (Seine-Saint-Denis, Seine-et-Marne, Paris…).
- [ ] Téléphone 06 62 06 93 22, site `https://www.ofentretiens.com/`, horaires.
- [ ] Services : un par page du site, avec le lien vers la page correspondante.
- [ ] 10 photos réelles minimum (chantiers, équipe, véhicule), puis 1 à 2 par mois.
- [ ] Demander un avis à chaque client satisfait (lien court de la fiche).
- [ ] **Dès qu'il y a de vrais avis** : remplacer le bloc « Ils nous font confiance » de l'accueil par la note,
      le nombre d'avis et 3 à 6 avis réels, et ajouter `aggregateRating` au JSON-LD **avec les mêmes chiffres**
      (emplacement signalé par un commentaire dans `site/index.html`). Jamais d'avis inventés.

## 5. Vérifications techniques sur le site en ligne
- [ ] PageSpeed Insights (mobile) sur l'accueil, une page de service et `/estimation/` : objectif > 90.
      (Mesure locale Lighthouse avant publication : 95 / 99 / 100 en performance, 100 en accessibilité, bonnes pratiques et SEO.)
- [ ] Test des résultats enrichis Google sur une page de service (Service, FAQPage, BreadcrumbList).
- [ ] Aperçu de partage : coller l'URL dans LinkedIn Post Inspector ou le débogueur de partage Facebook.
- [ ] Mobile réel : appel depuis la barre du bas, menu, sous-menu Services, formulaire d'estimation complet.
- [ ] Cookies : aucun outil de mesure n'est installé, le bandeau ne s'affiche donc pas tout seul
      (« Gérer les cookies » l'ouvre). Si vous ajoutez un outil de mesure d'audience, passer
      `data-mesure-audience="on"` dans `src/build.py` et charger l'outil dans `chargerMesure()` (`assets/site.js`).
