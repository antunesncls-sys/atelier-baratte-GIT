/* Formulaire d'estimation en plusieurs étapes, avec barre de progression.
   Sans JavaScript, toutes les étapes s'affichent l'une sous l'autre et le formulaire fonctionne. */
(function () {
  var form = document.getElementById('form-estimation');
  if (!form) return;
  var etapes = form.querySelectorAll('.etape');
  var barre = document.querySelector('.progression-barre span');
  var info = document.querySelector('.progression-info');
  var precedent = form.querySelector('[data-precedent]');
  var suivant = form.querySelector('[data-suivant]');
  var envoyer = form.querySelector('[data-envoyer]');
  var erreur = form.querySelector('.erreur');
  var courant = 0;
  var titres = ['Votre besoin', 'L’ampleur', 'Le lieu', 'Vos coordonnées'];

  // L'étape 2 s'adapte au service choisi
  var aides = {
    'Carottage en urgence': ['Nombre de carottages et support', 'Ex. : 5 carottages dans une dalle béton, diamètre si connu'],
    'Corvoyage et levée de réserves': ['Nombre de logements et échéance', 'Ex. : 40 logements, livraison prévue en mars'],
    'Nettoyage de bureaux, locaux ou base-vie': ['Type de locaux et fréquence souhaitée', 'Ex. : 300 m² de bureaux, 2 passages par semaine'],
    'Plateforme logistique': ['Nature des travaux ou de l’entretien', 'Ex. : bureaux et locaux sociaux, défaut d’étanchéité…'],
    'Nettoyage de façade ou de bardage': ['Hauteur et longueur approximatives', 'Ex. : bâtiment de 2 étages, façade de 40 m'],
    'Autres travaux': ['Décrivez les travaux', 'Ex. : reprise de plâtrerie, serrurerie, menuiserie…']
  };
  var labelDetail = form.querySelector('[data-detail-label]');
  var champDetail = form.querySelector('#est-detail');
  form.addEventListener('change', function (e) {
    if (e.target.name === 'service' && aides[e.target.value]) {
      labelDetail.textContent = aides[e.target.value][0];
      champDetail.placeholder = aides[e.target.value][1];
    }
  });
  // Service présélectionné par l'adresse (ex. /estimation/?service=carottage)
  var cle = new URLSearchParams(location.search).get('service');
  if (cle) {
    var radio = form.querySelector('input[name="service"][data-cle="' + cle + '"]');
    if (radio) { radio.checked = true; radio.dispatchEvent(new Event('change', { bubbles: true })); }
  }

  function afficher(i) {
    Array.prototype.forEach.call(etapes, function (et, n) { et.classList.toggle('active', n === i); });
    barre.style.width = ((i + 1) / etapes.length * 100) + '%';
    info.innerHTML = '<span>Étape ' + (i + 1) + ' sur ' + etapes.length + '</span><span>' + titres[i] + '</span>';
    precedent.hidden = i === 0;
    suivant.hidden = i === etapes.length - 1;
    envoyer.hidden = i !== etapes.length - 1;
    erreur.textContent = '';
    courant = i;
  }
  function valide(i) {
    var champs = etapes[i].querySelectorAll('input, select, textarea');
    for (var k = 0; k < champs.length; k++) {
      if (!champs[k].checkValidity()) {
        erreur.textContent = champs[k].type === 'radio' ? 'Choisissez une option pour continuer.' : 'Merci de compléter ce champ : ' + (champs[k].getAttribute('data-nom') || 'champ obligatoire') + '.';
        champs[k].focus();
        return false;
      }
    }
    return true;
  }
  suivant.addEventListener('click', function () {
    if (!valide(courant)) return;
    afficher(courant + 1);
    etapes[courant].querySelector('legend').focus();
  });
  precedent.addEventListener('click', function () {
    afficher(courant - 1);
    etapes[courant].querySelector('legend').focus();
  });
  form.addEventListener('submit', function (e) { if (!valide(courant)) e.preventDefault(); });
  Array.prototype.forEach.call(etapes, function (et) { et.querySelector('legend').setAttribute('tabindex', '-1'); });
  afficher(0);
})();
