/* OF ENTRETIENS — comportements communs à toutes les pages.
   Le site reste entièrement utilisable sans JavaScript. */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduit = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- menu mobile ---------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu-mobile');
  function fermerMenu(rendreFocus) {
    if (!menu || menu.hidden) return;
    menu.hidden = true;
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Ouvrir le menu');
    if (rendreFocus) burger.focus();
  }
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var ouvrir = menu.hidden;
      menu.hidden = !ouvrir;
      burger.setAttribute('aria-expanded', String(ouvrir));
      burger.setAttribute('aria-label', ouvrir ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) fermerMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') fermerMenu(true);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1080) fermerMenu(false);
    });
  }

  /* ---------- en-tête : ombre dès qu'on fait défiler ---------- */
  var entete = document.querySelector('.site-header');
  if (entete) {
    var majEntete = function () { entete.classList.toggle('scrolled', window.scrollY > 8); };
    majEntete();
    window.addEventListener('scroll', majEntete, { passive: true });
  }

  /* ---------- barre d'appel mobile : masquée quand le formulaire est à l'écran ---------- */
  var barre = document.querySelector('.barre-mobile');
  var contact = document.getElementById('contact');
  if (barre && contact && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entrees) {
      barre.classList.toggle('cachee', entrees[0].isIntersecting);
    }, { threshold: 0.15 }).observe(contact);
  }

  /* ---------- apparition douce des blocs au défilement ---------- */
  if (reduit || !('IntersectionObserver' in window)) return;
  var cibles = document.querySelectorAll(
    '.section-head, .card, .public-link, .bloc-liste li, .methode-pas li, .galerie figure,' +
    ' .avant-apres figure, .engagements article, .recente, .refs, .faq-liste details,' +
    ' .cta-band .wrap, .situations li, .page-photo, .logo-carte, .coord li'
  );
  var obs = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-visible'); obs.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  Array.prototype.forEach.call(cibles, function (el) {
    // les éléments déjà visibles au chargement ne sont pas animés (pas de « flash »)
    if (el.getBoundingClientRect().top < window.innerHeight * 0.92) return;
    var rang = Array.prototype.indexOf.call(el.parentNode.children, el) % 4;
    el.style.transitionDelay = (rang * 70) + 'ms';
    el.classList.add('reveal');
    obs.observe(el);
  });
})();
