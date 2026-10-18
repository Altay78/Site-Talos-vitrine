/* ══════════════════════════════════════════════════════════════════
   TALOS · MENUS VOLANTS DE LA BARRE
   Un bouton-icône ouvre un panneau ; une entrée à sous-menu fait
   glisser la vue vers la gauche, « Retour » la ramène.

   La sortie est jouée avant de masquer — le principe d'AnimatePresence :
   data-state="closing", on attend la fin de l'animation, puis hidden.
   Sans JS, les déclencheurs restent des boutons inertes et le menu du
   téléphone garde les mêmes liens : rien n'est perdu.

   Habillage dans talos-ui.css.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var ouvert = null;   // le .tfly dont le panneau est ouvert

  function vues(fly) { return fly.querySelectorAll('.tfly-view'); }

  /* la hauteur du panneau suit la vue affichée : mesurée, jamais devinée */
  function caler(fly, i) {
    var pan = fly.querySelector('.tfly-pan');
    var track = fly.querySelector('.tfly-track');
    var v = vues(fly);
    track.style.transform = 'translateX(' + (-100 * i) + '%)';
    v.forEach(function (el, k) { el.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
    pan.style.height = v[i].offsetHeight + 2 + 'px';   // + les deux filets du bord
    fly.dataset.vue = i;
  }

  function aller(fly, i) {
    caler(fly, i);
    var cible = vues(fly)[i].querySelector('.tfly-back, .tfly-it');
    if (cible) cible.focus({ preventScroll: true });
  }

  function ouvrir(fly) {
    if (ouvert && ouvert !== fly) fermer(ouvert, false);
    var pan = fly.querySelector('.tfly-pan');
    var t = fly.querySelector('.tfly-t');
    pan.hidden = false;
    pan.dataset.state = 'open';
    t.setAttribute('aria-expanded', 'true');
    pan.style.height = '';
    caler(fly, 0);
    ouvert = fly;
  }

  function fermer(fly, rendreFocus) {
    var pan = fly.querySelector('.tfly-pan');
    var t = fly.querySelector('.tfly-t');
    if (pan.hidden || pan.dataset.state === 'closing') return;
    t.setAttribute('aria-expanded', 'false');
    pan.dataset.state = 'closing';
    var fini = false;
    function fin() {
      if (fini || pan.dataset.state !== 'closing') return;
      fini = true;
      pan.hidden = true;
      pan.dataset.state = 'closed';
      caler(fly, 0);
    }
    pan.addEventListener('animationend', fin, { once: true });
    setTimeout(fin, 260);   // filet de sécurité : animation coupée, onglet masqué
    if (ouvert === fly) ouvert = null;
    if (rendreFocus) t.focus({ preventScroll: true });
  }

  function poser(fly) {
    var t = fly.querySelector('.tfly-t');
    var pan = fly.querySelector('.tfly-pan');
    if (!t || !pan) return;

    t.addEventListener('click', function () {
      if (pan.hidden || pan.dataset.state === 'closing') {
        ouvrir(fly);
        var premier = pan.querySelector('.tfly-it');
        if (premier && t.matches(':focus-visible')) premier.focus({ preventScroll: true });
      } else {
        fermer(fly, false);
      }
    });

    fly.addEventListener('click', function (e) {
      var sub = e.target.closest('[data-tfly-sub]');
      if (sub) { e.preventDefault(); aller(fly, +sub.getAttribute('data-tfly-sub')); return; }
      if (e.target.closest('.tfly-back')) { e.preventDefault(); aller(fly, 0); }
    });

    fly.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        e.stopPropagation();
        if (+fly.dataset.vue > 0) aller(fly, 0);
        else fermer(fly, true);
        return;
      }
      /* flèches haut / bas : on circule dans les entrées de la vue affichée */
      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
      var v = vues(fly)[+fly.dataset.vue || 0];
      if (!v || pan.hidden) return;
      var items = Array.prototype.slice.call(v.querySelectorAll('.tfly-back, .tfly-it'));
      var i = items.indexOf(document.activeElement);
      if (i < 0 && document.activeElement !== t) return;
      e.preventDefault();
      var n = e.key === 'ArrowDown' ? i + 1 : i - 1;
      if (n < 0) n = items.length - 1;
      if (n >= items.length) n = 0;
      items[n].focus({ preventScroll: true });
    });
  }

  function init() {
    document.querySelectorAll('.tfly').forEach(poser);

    document.addEventListener('pointerdown', function (e) {
      if (ouvert && !ouvert.contains(e.target)) fermer(ouvert, false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ouvert) fermer(ouvert, true);
    });
    /* le focus part ailleurs au clavier : le panneau se replie */
    document.addEventListener('focusin', function (e) {
      if (ouvert && !ouvert.contains(e.target)) fermer(ouvert, false);
    });
    window.addEventListener('resize', function () {
      if (ouvert) caler(ouvert, +ouvert.dataset.vue || 0);
    }, { passive: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
