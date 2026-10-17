/* ══════════════════════════════════════════════════════════════════
   TALOS · LE CONSENTEMENT AUX COOKIES
   (palette sombre fixe : les pages n'ont pas toutes les mêmes variables
   de thème, et un bandeau mi-clair mi-sombre devenait illisible)

   Un bandeau au premier passage, tant qu'aucun choix n'est fait :
   « Tout refuser », « Personnaliser », « Tout accepter », à égalité.
   Le choix vit dans un cookie `talos_consentement` posé sur
   .talos-ai.tech : il vaut pour le site ET l'espace client
   (app.talos-ai.tech, composant components/Consentement.tsx — même
   format, à garder identique). Durée : 6 mois, puis on redemande.

   Catégories :
   - nécessaires : thème, panier, session de l'espace client — toujours
     actifs, ils ne demandent pas d'accord ;
   - mesure : Vercel Speed Insights dans l'espace client — chargé
     seulement après « Accepter ».

   Le lien « Cookies » ajouté au pied de page rouvre le choix.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var NOM = 'talos_consentement';
  var VERSION = 'v1';
  var DUREE_S = 182 * 24 * 3600;

  function lire() {
    var m = document.cookie.match(new RegExp('(?:^|; )' + NOM + '=([^;]*)'));
    if (!m) return null;
    var p = decodeURIComponent(m[1]).split('.');
    if (p[0] !== VERSION || (p[1] !== 'm0' && p[1] !== 'm1')) return null;
    return { mesure: p[1] === 'm1', le: Number(p[2]) || 0 };
  }

  function ecrire(mesure) {
    var v = VERSION + '.' + (mesure ? 'm1' : 'm0') + '.' + Date.now();
    var dom = /(^|\.)talos-ai\.tech$/.test(location.hostname) ? '; Domain=.talos-ai.tech' : '';
    var sec = location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = NOM + '=' + encodeURIComponent(v) + '; Max-Age=' + DUREE_S + '; Path=/; SameSite=Lax' + dom + sec;
    try { window.dispatchEvent(new CustomEvent('talos-consentement', { detail: { mesure: mesure } })); } catch (e) {}
  }

  var CSS = '' +
    '.tc-boite{position:fixed;z-index:9999;left:16px;right:16px;bottom:16px;max-width:520px;margin:0 auto 0 0;' +
    'background:#1C1611;color:#F6EEE7;border:1px solid rgba(246,238,231,.16);' +
    'border-radius:18px;padding:20px 20px 16px;box-shadow:0 24px 60px -20px rgba(0,0,0,.55);font:14px/1.5 var(--font-sans,system-ui,sans-serif)}' +
    '.tc-boite h2{margin:0 0 6px;font-size:16px;font-weight:700;letter-spacing:-.01em;color:inherit}' +
    '.tc-boite p{margin:0;color:#C9BDB1;font-size:13.5px}' +
    '.tc-boite a{color:inherit;text-decoration:underline;text-underline-offset:2px}' +
    '.tc-act{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}' +
    '.tc-act button{flex:1 1 auto;min-height:42px;padding:0 16px;border-radius:100px;border:1px solid rgba(246,238,231,.16);' +
    'background:transparent;color:inherit;font-family:inherit;font-size:13.5px;font-weight:600;line-height:1;cursor:pointer}' +
    '.tc-act button.tc-plein{background:#E0631F;border-color:#E0631F;color:#fff}' +
    '.tc-act button:focus-visible,.tc-ligne input:focus-visible{outline:2px solid #E0631F;outline-offset:2px}' +
    '.tc-choix{margin-top:14px;display:grid;gap:10px}' +
    '.tc-ligne{display:flex;gap:12px;align-items:flex-start;padding:12px;border-radius:12px;background:rgba(246,238,231,.06)}' +
    '.tc-ligne input{width:18px;height:18px;margin-top:2px;flex-shrink:0;accent-color:#E0631F}' +
    '.tc-ligne b{display:block;font-size:13.5px}' +
    '@media (max-width:560px){.tc-boite{left:12px;right:12px;bottom:12px;padding:18px 16px 14px}.tc-act button{flex:1 1 100%}}';

  var boite = null;

  function fermer() { if (boite) { boite.remove(); boite = null; } }

  function ouvrir(detail) {
    fermer();
    var actuel = lire();
    if (!document.getElementById('tc-css')) {
      var st = document.createElement('style'); st.id = 'tc-css'; st.textContent = CSS;
      document.head.appendChild(st);
    }
    boite = document.createElement('section');
    boite.className = 'tc-boite';
    boite.setAttribute('role', 'dialog');
    boite.setAttribute('aria-labelledby', 'tc-titre');
    boite.innerHTML =
      '<h2 id="tc-titre">Vos cookies, votre choix</h2>' +
      '<p>Le site n’utilise que ce qui est nécessaire à son fonctionnement (thème, panier, connexion). ' +
      'Avec votre accord, votre espace client mesure aussi la vitesse d’affichage de ses pages (Vercel Speed Insights, sans publicité ni suivi d’un site à l’autre). ' +
      'Ce choix vaut pour le site et l’espace client, pendant 6 mois. <a href="confidentialite.html#cookies">En savoir plus</a></p>' +
      (detail
        ? '<div class="tc-choix">' +
            '<label class="tc-ligne"><input type="checkbox" checked disabled><span><b>Nécessaires</b>Thème, panier, session de l’espace client. Toujours actifs.</span></label>' +
            '<label class="tc-ligne"><input type="checkbox" id="tc-mesure"' + (actuel && actuel.mesure ? ' checked' : '') + '><span><b>Mesure de performance</b>Vitesse d’affichage de l’espace client, statistiques agrégées.</span></label>' +
          '</div>' +
          '<div class="tc-act"><button type="button" data-tc="refuser">Tout refuser</button><button type="button" class="tc-plein" data-tc="enregistrer">Enregistrer mon choix</button></div>'
        : '<div class="tc-act"><button type="button" data-tc="refuser">Tout refuser</button><button type="button" data-tc="detail">Personnaliser</button><button type="button" class="tc-plein" data-tc="accepter">Tout accepter</button></div>');
    boite.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-tc]');
      if (!b) return;
      var a = b.getAttribute('data-tc');
      if (a === 'detail') return ouvrir(true);
      if (a === 'accepter') ecrire(true);
      else if (a === 'refuser') ecrire(false);
      else if (a === 'enregistrer') ecrire(!!(document.getElementById('tc-mesure') || {}).checked);
      fermer();
    });
    document.body.appendChild(boite);
    if (detail) { var p = boite.querySelector('#tc-mesure'); if (p) p.focus(); }
  }

  /* « Cookies » dans la ligne des liens légaux du pied de page. */
  function lienPied() {
    var legal = document.querySelector('.ft-bottom .legal');
    if (!legal || legal.querySelector('[data-tc-lien]')) return;
    var dot = document.createElement('span'); dot.className = 'dot'; dot.textContent = '·';
    var a = document.createElement('a'); a.href = '#cookies'; a.textContent = 'Cookies'; a.setAttribute('data-tc-lien', '');
    a.addEventListener('click', function (e) { e.preventDefault(); ouvrir(true); });
    legal.appendChild(dot); legal.appendChild(a);
  }

  window.talosCookies = { ouvrir: function () { ouvrir(true); }, lire: lire };

  function demarrer() {
    lienPied();
    if (!lire()) ouvrir(false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', demarrer);
  else demarrer();
})();
