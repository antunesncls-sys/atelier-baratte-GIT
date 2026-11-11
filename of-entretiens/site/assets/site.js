/* OF ENTRETIENS — script commun, léger (aucune bibliothèque).
   Le site reste utilisable sans JavaScript. */
(function () {
  document.documentElement.classList.add('js');

  /* ---------- menu mobile ---------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu-mobile');
  function fermer(focus) {
    if (!menu || menu.hidden) return;
    menu.hidden = true;
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Ouvrir le menu');
    if (focus) burger.focus();
  }
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var ouvrir = menu.hidden;
      menu.hidden = !ouvrir;
      burger.setAttribute('aria-expanded', String(ouvrir));
      burger.setAttribute('aria-label', ouvrir ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) fermer(false); });
  }

  /* ---------- sous-menu « Services » (clavier et tactile) ---------- */
  var boutonsSousMenu = document.querySelectorAll('.menu button[aria-controls]');
  Array.prototype.forEach.call(boutonsSousMenu, function (b) {
    b.addEventListener('click', function () {
      b.setAttribute('aria-expanded', String(b.getAttribute('aria-expanded') !== 'true'));
    });
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(boutonsSousMenu, function (b) {
      if (!b.parentNode.contains(e.target)) b.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    fermer(true);
    Array.prototype.forEach.call(boutonsSousMenu, function (b) {
      if (b.getAttribute('aria-expanded') === 'true') { b.setAttribute('aria-expanded', 'false'); b.focus(); }
    });
  });

  /* ---------- cookies (RGPD) ----------
     Aujourd'hui le site ne dépose AUCUN cookie de mesure d'audience ni de publicité :
     le bandeau ne s'affiche donc pas tout seul. Pour ajouter un outil de mesure plus tard,
     passer data-mesure-audience="on" sur <html> et charger l'outil dans chargerMesure(). */
  var CLE = 'of-cookies-choix';
  var bandeau = document.getElementById('cookies');
  var actif = document.documentElement.getAttribute('data-mesure-audience') === 'on';
  function lire() { try { return JSON.parse(localStorage.getItem(CLE)); } catch (e) { return null; } }
  function enregistrer(mesure) {
    try { localStorage.setItem(CLE, JSON.stringify({ mesure: mesure, date: new Date().toISOString() })); } catch (e) {}
    if (mesure) chargerMesure();
    if (bandeau) bandeau.hidden = true;
  }
  function chargerMesure() { /* à compléter le jour où un outil de mesure est installé */ }
  if (bandeau) {
    var case_ = bandeau.querySelector('input[name="mesure"]');
    var reglages = bandeau.querySelector('.reglages');
    bandeau.addEventListener('click', function (e) {
      var action = e.target.getAttribute('data-cookies');
      if (action === 'refuser') enregistrer(false);
      if (action === 'accepter') enregistrer(true);
      if (action === 'personnaliser') {
        if (reglages.hidden) { reglages.hidden = false; e.target.textContent = 'Enregistrer'; }
        else enregistrer(!!(case_ && case_.checked));
      }
    });
    var choix = lire();
    if (actif && !choix) bandeau.hidden = false;
    if (actif && choix && choix.mesure) chargerMesure();
    Array.prototype.forEach.call(document.querySelectorAll('[data-gerer-cookies]'), function (l) {
      l.addEventListener('click', function (e) {
        e.preventDefault();
        var c = lire();
        if (case_) case_.checked = !!(c && c.mesure);
        bandeau.hidden = false;
        bandeau.querySelector('button').focus();
      });
    });
  }
})();
