/* ══════════════════════════════════════════════════════════════════
   TALOS · « EN SAVOIR PLUS »
   Repère les paragraphes gris — l'intro d'une section, le corps d'une
   carte — et les replie à trois lignes sur téléphone, derrière une
   pastille qui s'élargit en même temps qu'elle change de texte.

   « Gris » n'est pas une liste de classes : c'est une couleur de
   texte plus faible que celle de la section qui la contient. La
   règle tient donc sans qu'on ait à la tenir à jour page par page.

   Habillage dans talos-more.css. Sans JS, rien ne bouge.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var LINES  = 2;          // lignes laissées visibles
  var MINLEN = 100;        // en deçà, replier ne gagne rien
  var GAIN   = 1.5;        // lignes gagnées minimum : sous ce seuil la
                           // pastille coûterait plus de place qu'elle
                           // n'en rend, donc on laisse le texte entier
  var LEDE_LINES = 3;      // un chapeau replié en montre trois
  var LEDE_MAX   = 5.4;    // et n'est replié qu'au-delà de cinq lignes
  var EASE   = 'cubic-bezier(.22,1,.36,1)';

  var MQ_SMALL  = window.matchMedia('(max-width:860px)');
  var MQ_CALM   = window.matchMedia('(prefers-reduced-motion:reduce)');

  /* là où replier n'a pas de sens : navigation, pied de page,
     cartes de carrousel, feuilles du simulateur, formulaires… */
  var SKIP = [
    'nav', 'header', 'footer', 'form', 'button', 'a', 'label', 'table',
    'details', 'summary', 'li', 'figcaption',
    '.tnav-wrap', '.tnav-menu', '.t-ft', '.sheet', '.crew-c', '.fx-card',
    '.tf-panel', '[data-tx-skip]',
    /* CGU, CGV, mentions, confidentialité : un texte juridique se lit
       en entier ou ne vaut rien. Quinze pastilles y seraient quinze
       façons de ne pas lire ce qu'on signe. */
    '.t-legal'
  ].join(',');

  var CHEV =
    '<svg class="tx-chev" width="12" height="12" viewBox="0 0 24 24" fill="none" ' +
    'stroke="currentColor" stroke-width="3" stroke-linecap="round" ' +
    'stroke-linejoin="round" aria-hidden="true"><path d="M6 9.5l6 6 6-6"/></svg>';

  var uid = 0;
  var entries = [];

  /* ── repérage ─────────────────────────────────────────────────── */

  function rgba(v) {
    var m = (v || '').match(/[\d.]+/g) || [];
    return [+m[0] || 0, +m[1] || 0, +m[2] || 0, m[3] === undefined ? 1 : +m[3]];
  }

  /* gris = plus pâle que le texte courant de la section, soit par
     transparence (rgba(...,.7)) soit par teinte (--lin, --ink-soft) */
  function isMuted(el) {
    var c = rgba(getComputedStyle(el).color);
    if (c[3] < 0.96) return true;
    var host = el.closest('section, main, body') || document.body;
    var h = rgba(getComputedStyle(host).color);
    return Math.abs(c[0] - h[0]) + Math.abs(c[1] - h[1]) + Math.abs(c[2] - h[2]) > 40;
  }

  /* le chapeau d'une page — le paragraphe qui suit le <h1> — porte la
     promesse du site : on le laisse entier tant qu'il se lit d'un coup
     d'œil (voir LEDE_MAX). Au-delà, c'est un mur comme un autre, et il
     se replie sur trois lignes plutôt que deux. */
  function isLede(el) {
    var n = el.previousElementSibling;
    while (n) {
      if (/^H[1-6]$/.test(n.tagName)) return n.tagName === 'H1';
      n = n.previousElementSibling;
    }
    return false;
  }

  function eligible(el) {
    if (el.closest(SKIP)) return false;
    /* un paragraphe, pas un conteneur déguisé */
    if (el.querySelector('div,p,ul,ol,h1,h2,h3,h4,button,img,table,input')) return false;
    if (el.textContent.trim().length < MINLEN) return false;
    return isMuted(el);
  }

  function collect() {
    var found = [];
    [].forEach.call(document.querySelectorAll('p, [data-tx-more]'), function (el) {
      if (el.dataset.txSeen) return;
      if (!eligible(el)) return;
      el.dataset.txSeen = '1';
      found.push({ el: el, pill: null, lbl: null, on: false, open: false,
                   lede: isLede(el) });
    });
    return found;
  }

  /* ── mesures ──────────────────────────────────────────────────── */

  function lineOf(el) {
    var cs = getComputedStyle(el);
    var lh = parseFloat(cs.lineHeight);
    if (!lh) lh = parseFloat(cs.fontSize) * 1.6;
    return lh;
  }

  /* hauteur pleine et hauteur de coupe, mesurées sans le rognage.
     Renvoie faux quand le repli ne ferait pas gagner deux lignes. */
  function measure(entry) {
    var el = entry.el, keep = el.style.maxHeight;
    el.style.maxHeight = 'none';
    var line = lineOf(el);
    var full = el.scrollHeight;
    el.style.maxHeight = keep;

    entry.line = line;
    entry.cut = Math.round(line * (entry.lede ? LEDE_LINES : LINES));
    var floor = entry.lede ? line * LEDE_MAX : entry.cut + line * GAIN;
    return full > floor;
  }

  /* ── pastille ─────────────────────────────────────────────────── */

  function build(entry) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'tx-pill';
    b.setAttribute('aria-expanded', 'false');
    b.innerHTML = '<span class="tx-lbl">En savoir plus</span>' + CHEV;
    entry.el.insertAdjacentElement('afterend', b);
    entry.pill = b;
    entry.lbl = b.querySelector('.tx-lbl');
    b.addEventListener('click', function () { toggle(entry); });
  }

  function toggle(entry) {
    var el = entry.el, b = entry.pill;
    var open = entry.open = !entry.open;

    b.setAttribute('aria-expanded', open ? 'true' : 'false');
    el.classList.toggle('is-open', open);

    /* hauteur : on part toujours d'une valeur en pixels, sinon la
       transition n'a pas de point de départ à interpoler */
    if (open) {
      el.style.maxHeight = el.scrollHeight + 'px';
    } else {
      el.style.maxHeight = el.scrollHeight + 'px';
      void el.offsetHeight;
      el.style.maxHeight = entry.cut + 'px';
    }

    /* largeur : mesurée avant et après le changement de libellé,
       puis animée entre les deux — la pastille reprend sa largeur
       automatique dès que l'animation est finie (fill:'none') */
    var w0 = b.getBoundingClientRect().width;
    entry.lbl.textContent = open ? 'Réduire' : 'En savoir plus';
    var w1 = b.getBoundingClientRect().width;

    if (!MQ_CALM.matches && b.animate && Math.abs(w1 - w0) > 1) {
      b.animate([{ width: w0 + 'px' }, { width: w1 + 'px' }],
                { duration: 420, easing: EASE, fill: 'none' });
      entry.lbl.animate([{ opacity: 0, transform: 'translateY(-5px)' },
                         { opacity: 1, transform: 'none' }],
                { duration: 240, delay: 70, easing: 'ease-out', fill: 'none' });
    }
  }

  /* ── activation / retrait ─────────────────────────────────────── */

  function enable(entry) {
    if (entry.on) return;
    if (!measure(entry)) return;
    entry.on = true;

    var el = entry.el;
    if (!el.id) el.id = 'tx-txt-' + (++uid);
    el.classList.add('tx-txt');
    el.style.maxHeight = entry.cut + 'px';

    if (!entry.pill) {
      build(entry);
      /* une fois déplié, la hauteur redevient libre : une rotation
         d'écran ou une police qui arrive ne doit plus rien couper */
      el.addEventListener('transitionend', function (e) {
        if (e.propertyName === 'max-height' && entry.open) el.style.maxHeight = 'none';
      });
    }
    entry.pill.hidden = false;
    entry.pill.setAttribute('aria-controls', el.id);
  }

  function disable(entry) {
    if (!entry.on) return;
    entry.on = entry.open = false;
    entry.el.classList.remove('tx-txt', 'is-open');
    entry.el.style.maxHeight = '';
    if (entry.pill) {
      entry.pill.hidden = true;
      entry.pill.setAttribute('aria-expanded', 'false');
      entry.lbl.textContent = 'En savoir plus';
    }
  }

  /* ── cycle de vie ─────────────────────────────────────────────── */

  function apply() {
    var small = MQ_SMALL.matches;
    entries.forEach(function (entry) {
      if (small) enable(entry); else disable(entry);
    });
  }

  /* la largeur du paragraphe change → la coupe de trois lignes aussi */
  function remeasure() {
    if (!MQ_SMALL.matches) return;
    entries.forEach(function (entry) {
      if (!entry.on) return;
      measure(entry);
      entry.el.style.maxHeight = entry.open ? 'none' : entry.cut + 'px';
    });
  }

  var timer;
  function debounced() {
    clearTimeout(timer);
    timer = setTimeout(remeasure, 180);
  }

  function init() {
    entries = entries.concat(collect());
    apply();

    /* les polices arrivent après le premier rendu : la hauteur de
       ligne mesurée avant elles est fausse de quelques pixels */
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);

    window.addEventListener('resize', debounced, { passive: true });
    window.addEventListener('orientationchange', debounced, { passive: true });

    if (MQ_SMALL.addEventListener) MQ_SMALL.addEventListener('change', apply);
    else if (MQ_SMALL.addListener) MQ_SMALL.addListener(apply);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
