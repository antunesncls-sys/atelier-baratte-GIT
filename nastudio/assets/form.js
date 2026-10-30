(function(){
  var form = document.querySelector('form[name=devis]');
  if (!form) return;

  function esc(s){ return s.replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }

  function showSent(firstName){
    var box = document.createElement('div');
    box.className = 'sent';
    box.setAttribute('role', 'status');
    box.tabIndex = -1;
    box.innerHTML =
      '<div class="sent-ic" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg></div>' +
      '<p class="sent-k">Demande envoyée</p>' +
      '<h3 class="sent-t">Merci' + (firstName ? ' ' + esc(firstName) : '') + '.</h3>' +
      '<p class="sent-p">Votre demande est bien arrivée. Nicolas vous rappelle <b>sous un jour ouvré</b> pour convenir d\'un rendez-vous chez vous.</p>' +
      '<ol class="sent-steps">' +
        '<li>On vous rappelle pour comprendre votre besoin</li>' +
        '<li>On se déplace pour l\'audit gratuit, sur place</li>' +
        '<li>Vous recevez un devis précis sous 48&nbsp;h</li>' +
      '</ol>' +
      '<div class="sent-a">' +
        '<a class="cta" href="tel:+33761705359">Pressé&nbsp;? 07&nbsp;61&nbsp;70&nbsp;53&nbsp;59</a>' +
        '<a class="sent-l" href="/sites">Voir nos réalisations →</a>' +
      '</div>';
    form.replaceWith(box);
    try { box.focus({ preventScroll: true }); } catch (e) {}
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var nom = form.querySelector('[name=nom]');
    var firstName = nom ? nom.value.trim().split(/\s+/)[0] : '';

    if (location.protocol !== 'https:') { showSent(firstName); return; }

    var btn = form.querySelector('button[type=submit]');
    if (btn) { btn.disabled = true; btn.textContent = 'Envoi en cours…'; }

    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(form)).toString()
    }).then(function(r){
      if (!r.ok) throw new Error(r.status);
      showSent(firstName);
    }).catch(function(){
      form.submit();
    });
  });
})();
