/* =====================================================================
   RIZ DJONDJON — CONFIGURATION DU SITE
   ---------------------------------------------------------------------
   Tout le contenu modifiable est ici : liens, horaires, carte,
   événements, Instagram, formulaire. Pas besoin de toucher au HTML.
   Les éléments marqués  ⚠ À VALIDER  sont des propositions à confirmer
   avec le restaurant (prix, plats, événements).
   ===================================================================== */

window.RDJ_CONFIG = {
  /* --- Identité & coordonnées (source : riz-djondjon.eatbu.com) --- */
  name: "Riz Djondjon",
  phone: "+33652921902",
  phoneDisplay: "06 52 92 19 02",
  email: "rizdjondjon@gmail.com",
  address: {
    street: "291 rue Saint-Denis",
    zip: "75002",
    city: "Paris",
    access: [
      { label: "Réaumur – Sébastopol", lines: ["3", "4"] },
      { label: "Strasbourg – Saint-Denis", lines: ["4", "8", "9"] },
    ],
  },

  /* --- Liens externes --- */
  links: {
    instagram: "https://www.instagram.com/rizdjondjon",
    instagramHandle: "@rizdjondjon",
    facebook: "https://www.facebook.com/resto.rizdjondjon",
    // ⚠ À VALIDER : remplacer par l'URL exacte de la fiche Uber Eats du restaurant
    //   (ex. https://www.ubereats.com/fr/store/riz-djondjon/XXXXXXXX)
    ubereats: "https://www.ubereats.com/fr/search?q=Riz%20Djondjon",
    // Widget de réservation Dish déjà utilisé par le restaurant
    reservation: "https://reservation.dish.co/widget/hydra-6b09669d-9671-4575-9212-6535734654ab",
    maps: "https://www.google.com/maps/search/?api=1&query=Riz+Djondjon+291+rue+Saint-Denis+75002+Paris",
    mapsDirections: "https://www.google.com/maps/dir/?api=1&destination=291+rue+Saint-Denis+75002+Paris",
    mapsEmbed: "https://www.google.com/maps?q=291+rue+Saint-Denis,+75002+Paris&z=16&output=embed",
  },

  /* --- Horaires (source : données structurées du site actuel) ---
     0 = dimanche … 6 = samedi. "24:00" = minuit. */
  hours: {
    0: [["10:00", "22:30"]],
    1: [["12:00", "23:00"]],
    2: [["12:00", "23:00"]],
    3: [["12:00", "23:00"]],
    4: [["12:00", "23:00"]],
    5: [["12:00", "24:00"]],
    6: [["12:00", "24:00"]],
  },

  /* --- Instagram ---
     Trois façons d'afficher les posts, par ordre de priorité :
     1. feedUrl  : URL JSON d'un service de flux (ex. Behold.so — gratuit,
                   connecté au compte Instagram, se met à jour tout seul).
     2. posts    : liste d'URLs de posts → intégrés avec l'embed officiel Instagram.
     3. fallback : grille de visuels du site avec lien vers le profil. */
  instagram: {
    feedUrl: "", // ex. "https://feeds.behold.so/XXXXXXXXXXXX"
    posts: [
      // "https://www.instagram.com/p/XXXXXXXXXXX/",
    ],
    fallback: [
      { img: "assets/img/hero-large", alt: "Assiette lalo et crabe, riz blanc et sauce pois", caption: "Lalo ak krab, riz blan & sos pwa 🇭🇹" },
      { img: "assets/img/jus-maison", alt: "Jus de fruits maison", caption: "Jus maison pressé du jour 🍹" },
      { img: "assets/img/decor-jungle", alt: "Décor tropical du restaurant", caption: "Notre petite jungle rue Saint-Denis 🌿" },
      { img: "assets/img/sos-pwa", alt: "Sauce pois maison", caption: "Sos pwa, la recette de la maison" },
      { img: "assets/img/plat-detail", alt: "Détail d'une assiette", caption: "Copieux, comme à la maison ✨" },
      { img: "assets/img/decor-jungle-2", alt: "Banquette et papier peint jungle", caption: "Réservez votre table ce week-end" },
    ],
  },

  /* --- Formulaire de contact ---
     Laisser vide → le formulaire ouvre la messagerie (mailto).
     Pour un envoi direct : créer un formulaire gratuit sur formspree.io
     et coller l'URL ici (ex. "https://formspree.io/f/abcdwxyz"). */
  formEndpoint: "",

  /* --- Carte ⚠ À VALIDER (plats inspirés des avis clients, prix indicatifs) --- */
  menu: [
    {
      id: "signature",
      title: "Plats signature",
      note: "Servis avec pikliz maison",
      items: [
        { name: "Riz djondjon & griot", desc: "Riz noir aux champignons djon djon, porc mariné aux agrumes puis frit, bananes pesées.", price: 17, tags: ["signature"] },
        { name: "Riz djondjon & tasso de bœuf", desc: "Bœuf mariné, frit et caramélisé, riz djondjon parfumé au clou de girofle.", price: 18, tags: ["signature"] },
        { name: "Lalo ak krab", desc: "Feuilles de lalo mijotées au crabe, riz blanc et sos pwa.", price: 19, tags: [] },
        { name: "Poulet en sauce créole", desc: "Poulet mijoté tomates, poivrons, piment bouc et épices.", price: 15, tags: [] },
        { name: "Pwason fri", desc: "Poisson entier frit, sauce ti-malice, bananes pesées.", price: 19, tags: [] },
        { name: "Riz tchiep", desc: "Riz rouge aux légumes et poisson, à la mode d'Afrique de l'Ouest.", price: 17, tags: [] },
        { name: "Legim lakay", desc: "Ragoût de légumes (aubergine, chou, chayotte, épinards), riz au choix.", price: 14, tags: ["végé"] },
      ],
    },
    {
      id: "cote",
      title: "À côté",
      note: "À partager… ou pas",
      items: [
        { name: "Akra", desc: "Beignets de malanga croustillants.", price: 6, tags: ["végé"] },
        { name: "Marinad", desc: "Beignets salés aux herbes.", price: 6, tags: ["végé"] },
        { name: "Bannann peze", desc: "Bananes plantain pesées et frites.", price: 5, tags: ["végé"] },
        { name: "Diri kole ak pwa", desc: "Riz collé aux haricots rouges.", price: 5, tags: ["végé"] },
        { name: "Pikliz maison", desc: "Chou, carotte et piment bouc marinés au vinaigre.", price: 3, tags: ["épicé"] },
      ],
    },
    {
      id: "douceurs",
      title: "Douceurs",
      note: "Faites maison",
      items: [
        { name: "Pain patate", desc: "Gâteau de patate douce, banane et coco, épices douces.", price: 6, tags: [] },
        { name: "Blanmanje coco", desc: "Flan coco, coulis fruits de la passion.", price: 6, tags: [] },
        { name: "Tablet nwa", desc: "Nougat de cacahuètes caramélisées au gingembre.", price: 4, tags: [] },
      ],
    },
    {
      id: "boissons",
      title: "Boissons",
      note: "Jus pressés chaque jour",
      items: [
        { name: "Jus maison", desc: "Grenadia (passion), corossol, chadèque ou mangue.", price: 5, tags: [] },
        { name: "Cola Couronne", desc: "Le soda fruité d'Haïti.", price: 4, tags: [] },
        { name: "Malta", desc: "Boisson maltée sans alcool.", price: 4, tags: [] },
        { name: "Bière Prestige", desc: "Lager haïtienne, 33 cl.", price: 6, tags: [] },
        { name: "Rhum Barbancourt", desc: "5 étoiles, 4 cl.", price: 8, tags: [] },
      ],
    },
  ],

  /* --- Formules ⚠ À VALIDER --- */
  formulas: [
    { title: "Formule midi", when: "Lun – Ven · 12h – 15h", price: "15 €", desc: "Plat du jour + jus maison ou soft.", cta: "Réserver le midi" },
    { title: "Menu Lakay", when: "Tous les jours", price: "27 €", desc: "Akra ou marinad + plat signature + douceur maison.", cta: "Réserver une table", featured: true },
    { title: "Brunch du dimanche", when: "Dimanche · 10h – 15h", price: "25 €", desc: "Spaghetti haïtien, banane, œufs, akra, pain patate, jus et café.", cta: "Réserver le brunch" },
    { title: "Groupes & privatisation", when: "Sur demande", price: "Sur devis", desc: "Anniversaires, afterworks, baptêmes : le restaurant est à vous.", cta: "Demander un devis", contact: true },
  ],

  /* --- Événements ⚠ À VALIDER (exemples de programmation) ---
     date : "AAAA-MM-JJ" · recurring : "weekly" + weekday (0 = dim.) pour un événement récurrent */
  events: [
    { id: "brunch", title: "Brunch lakay", recurring: "weekly", weekday: 0, start: "10:00", end: "15:00", type: "brunch", desc: "Le brunch haïtien du dimanche : spaghetti, akra, bananes, jus pressés. En famille ou entre amis." },
    { id: "konpa-nov", title: "Soirée Konpa", date: "2026-11-14", start: "20:00", end: "00:00", type: "soirée", desc: "DJ set kompa & zouk, cocktails au rhum Barbancourt. Pistes de danse entre les tables !" },
    { id: "twoubadou", title: "Live twoubadou", date: "2026-11-27", start: "20:30", end: "23:00", type: "concert", desc: "Musique twoubadou acoustique : guitare, maracas et chansons d'Haïti pendant le dîner." },
    { id: "pikliz", title: "Atelier pikliz", date: "2026-12-05", start: "16:00", end: "18:00", type: "atelier", desc: "Apprenez à faire le pikliz de la maison et repartez avec votre bocal. Places limitées." },
    { id: "noel", title: "Soirée Noël créole", date: "2026-12-19", start: "19:30", end: "00:00", type: "soirée", desc: "Menu de fête, kremas maison et musique. Ambiance réveillon avant l'heure." },
    { id: "reveillon", title: "Réveillon lakay", date: "2026-12-31", start: "20:00", end: "02:00", type: "soirée", desc: "Dîner de réveillon et passage à la nouvelle année en musique. Réservation obligatoire." },
    { id: "joumou", title: "Soup joumou — Jour de l'Indépendance", date: "2027-01-01", start: "10:00", end: "16:00", type: "tradition", desc: "Le 1er janvier, on célèbre l'indépendance d'Haïti avec la soupe joumou, symbole de liberté." },
    { id: "konpa-jan", title: "Soirée Konpa", date: "2027-01-16", start: "20:00", end: "00:00", type: "soirée", desc: "Retour de la soirée kompa du mois. DJ, danse et bonne humeur." },
  ],

  /* --- Avis clients (source : site actuel, avis vérifiés) --- */
  reviews: [
    { name: "Serge O.", date: "février 2026", text: "Chaleureux accueil ♥️ Un bon moment en famille autour de repas copieux et de qualité !" },
    { name: "Blueberry C.", date: "janvier 2026", text: "C'était délicieux ! Dans un cadre très sympa et dans un quartier animé." },
    { name: "Tania B.", date: "janvier 2026", text: "Tout était bon ! Le service est rapide." },
    { name: "Client vérifié", date: "janvier 2026", text: "Nous nous sommes régalés. Les plats étaient délicieux, très bien cuits." },
    { name: "Client vérifié", date: "octobre 2025", text: "Une première pour mes amies et moi. Nous avons très apprécié et reviendrons évidemment." },
  ],
};
