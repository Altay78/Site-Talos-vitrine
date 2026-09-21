/* ═══════════════════════════════════════════════════════════════════════════
   LE PANIER — composer son équipe et commander sans passer par une démo.

   Une seule source de vérité pour la grille tarifaire : le tableau PALIERS
   ci-dessous. La page Tarifs garde sa propre copie pour l'instant ; le jour
   où on la régénérera, elle lira celle-ci.

   Le script s'auto-installe : il pose le bouton dans la barre, construit le
   tiroir, et réveille tout élément portant data-panier="<slug>". Aucune page
   n'a besoin de savoir comment il marche — il suffit de l'inclure.

   Ce qu'on envoie à l'application à la commande : la sélection, pas les
   montants. Les prix se recalculent de l'autre côté — une URL, ça se
   bricole.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── où part la commande ────────────────────────────────────────────────
     L'application ne sert aujourd'hui que sa racine : on y pose la
     configuration en paramètres. Le jour où /inscription existe, il n'y a
     que cette constante à changer.
     Contrat : ?agents=commercial,client&engagement=6&formule=business&src=site
       agents      les identifiants choisis, séparés par des virgules
       engagement  la durée en mois — 1, 3, 6 ou 12
       formule     starter | business | evolution (déduite du nombre d'agents)
       src         d'où vient la commande, pour vos statistiques           */
  var APP = 'https://app.talos-ai.tech/';

  /* ── la grille, telle qu'annoncée sur la page Tarifs ────────────────────
     Les prix engagés sont écrits en dur : ce sont ceux du barème, pas un
     pourcentage recalculé qui produirait des 89,10 €. */
  var PALIERS = [
    { id: 'starter',   nom: 'Starter',   max: 1, setup: 149, p: { m: 99,  n: 89,  y: 82  } },
    { id: 'business',  nom: 'Business',  max: 3, setup: 449, p: { m: 299, n: 269, y: 249 } },
    { id: 'evolution', nom: 'Évolution', max: 5, setup: 690, p: { m: 449, n: 399, y: 369 } }
  ];

  var ENGAGEMENTS = [
    { k: 'm', lab: 'Mensuel', mois: 1,  off: 0,  setup: true,
      note: 'Sans engagement, résiliable à tout moment.' },
    { k: 'n', lab: '6 mois',  mois: 6,  off: 10, setup: false,
      note: '−10 % sur l\'abonnement, et la mise en place offerte. Engagement ferme de six mois.' },
    { k: 'y', lab: '12 mois', mois: 12, off: 17, setup: false,
      note: 'Deux mois offerts, la mise en place offerte. Engagement ferme de douze mois — la formule la plus rentable.' }
  ];

  var AGENTS = [
    { id: 'commercial',    nom: 'Assistant commercial',    sous: 'Devis, signature, relances' },
    { id: 'tresorerie',    nom: 'Assistante trésorerie',   sous: 'Impayés et prévision' },
    { id: 'client',        nom: 'Assistante client',       sous: 'Réponses et rendez-vous' },
    { id: 'facturation',   nom: 'Assistant facturation',   sous: 'Factures conformes 2026' },
    { id: 'administratif', nom: 'Assistante administrative', sous: 'Tri des mails et classement' }
  ];

  var PAR_ID = {};
  AGENTS.forEach(function (a) { PAR_ID[a.id] = a; });

  var CLE = 'talos-panier';
  var MAX = AGENTS.length;

  /* ── icônes ─────────────────────────────────────────────────────────── */
  function svg(d, trait) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="' +
      (trait || 1.8) + '" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      d + '</svg>';
  }
  var I = {
    sac: svg('<path d="M 6.69 11.38C 7.38 10.23 8.12 9.1 8.85 7.97L 6.87 4.28C 6.87 4.28 7.02 4.15 ' +
      '7.4 3.85C 8.53 2.98 9.76 2.76 11.09 3.27C 12.36 3.77 13.65 4.14 15.02 4.06C 15.42 4.04 16.96 ' +
      '3.84 16.96 3.84L 15.16 7.96C 15.88 9.09 16.62 10.23 17.31 11.38C 18.44 13.26 19.53 15.37 ' +
      '18.65 17.56C 17.63 20.11 14.64 20.96 12 21C 9.35 20.96 6.37 20.11 5.35 17.56C 4.47 15.37 ' +
      '5.56 13.26 6.69 11.38Z"/><path d="M 8.85 7.98C 10.95 8.46 13.05 8.46 15.16 7.98"/>'),
    croix: svg('<path d="M6 6l12 12M18 6L6 18"/>', 2.2),
    plus:  svg('<path d="M12 5v14M5 12h14"/>', 2.4),
    check: svg('<path d="M20 6 9 17l-5-5"/>', 2.6),
    fleche: svg('<path d="M5 12h14M13 6l6 6-6 6"/>', 2.4),
    chev:  svg('<path d="M9 6l6 6-6 6"/>', 2.4)
  };

  /* ── l'état, gardé d'une page à l'autre ─────────────────────────────── */
  var etat = { agents: [], eng: 'n' };

  function lire() {
    try {
      var brut = JSON.parse(localStorage.getItem(CLE) || 'null');
      if (!brut) return;
      if (Array.isArray(brut.agents)) {
        etat.agents = brut.agents.filter(function (id) { return PAR_ID[id]; }).slice(0, MAX);
      }
      if (ENGAGEMENTS.some(function (e) { return e.k === brut.eng; })) etat.eng = brut.eng;
    } catch (e) { /* navigation privée, stockage refusé : on repart à vide */ }
  }

  function ecrire() {
    try { localStorage.setItem(CLE, JSON.stringify(etat)); } catch (e) {}
    rendre();
    /* le panier peut être modifié depuis deux endroits de la même page */
    document.dispatchEvent(new CustomEvent('panier:change', { detail: calcul() }));
  }

  function dedans(id) { return etat.agents.indexOf(id) >= 0; }

  function basculer(id) {
    if (!PAR_ID[id]) return;
    var i = etat.agents.indexOf(id);
    if (i >= 0) etat.agents.splice(i, 1);
    else if (etat.agents.length < MAX) etat.agents.push(id);
    ecrire();
  }

  function vider() { etat.agents = []; ecrire(); }

  /* ── le calcul ──────────────────────────────────────────────────────── */
  function engagement() {
    for (var i = 0; i < ENGAGEMENTS.length; i++) {
      if (ENGAGEMENTS[i].k === etat.eng) return ENGAGEMENTS[i];
    }
    return ENGAGEMENTS[0];
  }

  function palier() {
    var n = etat.agents.length;
    if (!n) return null;
    for (var i = 0; i < PALIERS.length; i++) {
      if (n <= PALIERS[i].max) return PALIERS[i];
    }
    return PALIERS[PALIERS.length - 1];
  }

  function calcul() {
    var pal = palier(), eng = engagement();
    if (!pal) return { n: 0, agents: [], eng: eng, palier: null };
    var mensuel = pal.p[eng.k];
    var install = eng.setup ? pal.setup : 0;
    return {
      n: etat.agents.length,
      agents: etat.agents.slice(),
      eng: eng,
      palier: pal,
      mensuel: mensuel,
      /* ce qu'on économise sur la durée par rapport au tarif mensuel,
         mise en place comprise quand elle est offerte */
      economie: (pal.p.m - mensuel) * eng.mois + (eng.setup ? 0 : pal.setup),
      install: install,
      premier: mensuel + install,
      total: mensuel * eng.mois + install,
      /* il reste de la place dans le palier : autant le dire */
      restants: pal.max - etat.agents.length
    };
  }

  var euros = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
  function eur(v) { return euros.format(v).replace(/ /g, ' ') + ' €'; }

  /* la sélection, sous une forme qui suit la commande partout */
  function parametres(c) {
    return 'agents=' + encodeURIComponent(c.agents.join(',')) +
      '&engagement=' + c.eng.mois +
      '&formule=' + c.palier.id +
      '&src=site';
  }

  /* Le lien de paiement Stripe existe → on y va, la commande se règle en
     ligne. Il n'existe pas encore → on n'envoie surtout pas le client sur
     une page qui ne sait pas l'encaisser : il part vers le formulaire avec
     sa sélection déjà constituée, et on le rappelle.
     (APP reste là pour le jour où l'application aura sa page d'inscription :
     il n'y aura que cette fonction à rebrancher.) */
  function lien() {
    var c = calcul();
    if (!c.palier) return 'reserver.html';
    var stripe = window.TalosPaiement &&
      window.TalosPaiement.lien(c.palier.id, c.eng.k, c.agents.join('-'));
    if (stripe) return stripe;
    return 'reserver.html?' + parametres(c);
  }

  function achatPret() {
    return !!(window.TalosPaiement && window.TalosPaiement.pret());
  }

  /* ═══ LE BOUTON DE LA BARRE ═══════════════════════════════════════════ */
  function poserBouton() {
    var act = document.querySelector('.tnav-act');
    if (act && !act.querySelector('.pn-btn')) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pn-btn';
      b.setAttribute('aria-haspopup', 'dialog');
      b.innerHTML = I.sac + '<span class="pn-btn-t">Mon équipe</span><span class="pn-n" aria-hidden="true">0</span>';
      b.addEventListener('click', ouvrir);
      var cta = act.querySelector('.tnav-cta');
      act.insertBefore(b, cta || act.firstChild);
    }
    /* le menu mobile a sa propre liste : la barre y est trop serrée */
    var menu = document.getElementById('tnav-menu');
    if (menu && !menu.querySelector('.m-panier')) {
      var a = document.createElement('button');
      a.type = 'button';
      a.className = 'm-panier';
      a.innerHTML = 'Mon équipe <span class="pn-n" aria-hidden="true">0</span>';
      a.addEventListener('click', function () { ouvrir(); });
      var esp = menu.querySelector('.m-esp');
      menu.insertBefore(a, esp || null);
    }
  }

  /* ═══ LE TIROIR ═══════════════════════════════════════════════════════ */
  var tiroir, scrim, corps, dernierFocus;

  function poserTiroir() {
    if (tiroir) return;
    scrim = document.createElement('div');
    scrim.className = 'pn-scrim';
    scrim.hidden = true;
    scrim.addEventListener('click', fermer);

    tiroir = document.createElement('aside');
    tiroir.className = 'pn-tiroir';
    tiroir.hidden = true;
    tiroir.setAttribute('role', 'dialog');
    tiroir.setAttribute('aria-modal', 'true');
    tiroir.setAttribute('aria-label', 'Mon équipe Talos');
    tiroir.innerHTML =
      '<header class="pn-hd">' +
        '<b>Mon équipe</b>' +
        '<button type="button" class="pn-x" aria-label="Fermer">' + I.croix + '</button>' +
      '</header>' +
      '<div class="pn-corps"></div>';
    tiroir.querySelector('.pn-x').addEventListener('click', fermer);

    document.body.appendChild(scrim);
    document.body.appendChild(tiroir);
    corps = tiroir.querySelector('.pn-corps');
  }

  function ouvrir() {
    poserTiroir();
    dernierFocus = document.activeElement;
    scrim.hidden = false;
    tiroir.hidden = false;
    /* deux images successives, sinon la transition ne part pas */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { document.documentElement.classList.add('pn-ouvert'); });
    });
    rendre();
    var cible = tiroir.querySelector('.pn-x');
    if (cible) cible.focus();
  }

  function fermer() {
    if (!tiroir || tiroir.hidden) return;
    document.documentElement.classList.remove('pn-ouvert');
    var fin = function () {
      tiroir.hidden = true;
      scrim.hidden = true;
      tiroir.removeEventListener('transitionend', fin);
    };
    tiroir.addEventListener('transitionend', fin);
    /* si les transitions sont coupées, transitionend ne vient jamais */
    setTimeout(fin, 420);
    if (dernierFocus && dernierFocus.focus) dernierFocus.focus();
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') fermer();
    if (e.key !== 'Tab' || !tiroir || tiroir.hidden) return;
    /* tant que le tiroir est ouvert, la tabulation y reste */
    var f = tiroir.querySelectorAll('button, [href], input, select, [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var premier = f[0], dernier = f[f.length - 1];
    if (e.shiftKey && document.activeElement === premier) { e.preventDefault(); dernier.focus(); }
    else if (!e.shiftKey && document.activeElement === dernier) { e.preventDefault(); premier.focus(); }
  });

  /* ═══ LE RÉCAPITULATIF — le même dans le tiroir et sur la page ════════ */
  function htmlChoix(c) {
    return AGENTS.map(function (a) {
      var on = dedans(a.id);
      return '<li><button type="button" class="pn-ag' + (on ? ' on' : '') +
        '" data-bascule="' + a.id + '" aria-pressed="' + (on ? 'true' : 'false') + '">' +
        '<img src="perso/avatar-' + a.id + '.webp" width="40" height="40" alt="" loading="lazy">' +
        '<span class="pn-ag-t"><b>' + a.nom + '</b><small>' + a.sous + '</small></span>' +
        '<span class="pn-ag-x" aria-hidden="true">' + (on ? I.check : I.plus) + '</span>' +
        '</button></li>';
    }).join('');
  }

  function htmlEngagement() {
    return ENGAGEMENTS.map(function (e) {
      return '<button type="button" class="pn-eng' + (e.k === etat.eng ? ' on' : '') +
        '" data-eng="' + e.k + '" aria-pressed="' + (e.k === etat.eng ? 'true' : 'false') + '">' +
        e.lab + (e.off ? '<i>−' + e.off + ' %</i>' : '') + '</button>';
    }).join('');
  }

  function htmlTotal(c) {
    if (!c.palier) {
      return '<p class="pn-vide">Choisissez au moins un assistant pour voir le tarif.</p>';
    }
    var offerte = !c.eng.setup;
    return '<div class="pn-formule">' +
        '<span class="pn-formule-l">Formule</span>' +
        '<b>' + c.palier.nom + '</b>' +
        '<small>' + c.n + (c.n > 1 ? ' assistants' : ' assistant') +
          (c.restants > 0 ? ' · ' + c.restants + ' de plus sans surcoût' : '') + '</small>' +
      '</div>' +
      '<dl class="pn-lignes">' +
        '<div><dt>Abonnement</dt><dd>' + eur(c.mensuel) + ' <span>par mois</span></dd></div>' +
        '<div><dt>Mise en place</dt><dd>' +
          (offerte ? '<s>' + eur(c.palier.setup) + '</s> <em>offerte</em>' : eur(c.install)) +
        '</dd></div>' +
        '<div class="pn-fort"><dt>À régler le premier mois</dt><dd>' + eur(c.premier) + '</dd></div>' +
      '</dl>' +
      (c.economie > 0
        ? '<p class="pn-eco">' + I.check + 'Vous économisez <b>' + eur(c.economie) +
          '</b> sur ' + c.eng.mois + ' mois.</p>'
        : '') +
      '<p class="pn-note">' + c.eng.note + '</p>';
  }

  function htmlActions(c) {
    var pret = !!c.palier;
    var paie = achatPret();
    /* deux mondes, deux promesses — on n'écrit « payer en ligne » que
       lorsque la page suivante sait réellement encaisser */
    var label = paie ? 'Commander et payer en ligne' : 'Recevoir ma proposition';
    var second = paie
      ? 'J\'ai une question, je préfère en parler'
      : 'Je préfère voir une démonstration d\'abord';
    return '<a class="pn-cta' + (pret ? '' : ' off') + '" href="' + (pret ? lien() : '#') + '"' +
        (pret ? '' : ' aria-disabled="true" tabindex="-1"') + '>' +
        label + ' ' + I.fleche + '</a>' +
      (pret && paie
        ? '<p class="pn-rassure">' + I.check + c.eng.note + '</p>'
        : '') +
      '<a class="pn-cta2" href="reserver.html">' + second + '</a>' +
      (c.n ? '<button type="button" class="pn-vider" data-vider>Vider mon équipe</button>' : '');
  }

  /* ── ce qui est réellement peint, à chaque changement ─────────────────── */
  function rendre() {
    var c = calcul();

    /* les compteurs de la barre */
    [].forEach.call(document.querySelectorAll('.pn-n'), function (n) {
      n.textContent = c.n;
      n.classList.toggle('zero', c.n === 0);
    });
    [].forEach.call(document.querySelectorAll('.pn-btn'), function (b) {
      b.setAttribute('aria-label', c.n
        ? 'Mon équipe — ' + c.n + (c.n > 1 ? ' assistants choisis' : ' assistant choisi')
        : 'Mon équipe — aucun assistant choisi');
    });

    /* les boutons « ajouter » posés dans les pages */
    [].forEach.call(document.querySelectorAll('[data-panier]'), function (b) {
      var id = b.getAttribute('data-panier');
      var on = dedans(id);
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      /* le libellé et l'icône vivent dans deux enfants : on ne réécrit pas
         le bouton entier, sinon on perdrait le focus à chaque changement */
      var lab = b.querySelector('[data-panier-label]');
      var ico = b.querySelector('[data-panier-ico]');
      var nom = PAR_ID[id] ? PAR_ID[id].nom : '';
      if (lab) {
        lab.textContent = on
          ? (b.getAttribute('data-panier-dedans') || 'Dans mon équipe')
          : (b.getAttribute('data-panier-texte') || 'Ajouter à mon équipe');
      }
      if (ico) ico.innerHTML = on ? I.check : I.plus;
      b.title = on ? 'Retirer ' + nom + ' de mon équipe' : 'Ajouter ' + nom + ' à mon équipe';
    });

    /* le tiroir */
    if (corps) {
      corps.innerHTML =
        '<section class="pn-sec"><h3>Vos assistants</h3><ul class="pn-ags">' + htmlChoix(c) + '</ul></section>' +
        '<section class="pn-sec"><h3>Votre engagement</h3><div class="pn-engs">' + htmlEngagement() + '</div></section>' +
        '<section class="pn-sec pn-recap">' + htmlTotal(c) + '</section>' +
        '<div class="pn-actions">' + htmlActions(c) + '</div>';
    }

    /* la page Commander */
    var page = document.querySelector('[data-panier-page]');
    if (page) {
      var el = function (s) { return page.querySelector(s); };
      if (el('[data-pn-choix]'))  el('[data-pn-choix]').innerHTML = htmlChoix(c);
      if (el('[data-pn-eng]'))    el('[data-pn-eng]').innerHTML = htmlEngagement();
      if (el('[data-pn-total]'))  el('[data-pn-total]').innerHTML = htmlTotal(c);
      if (el('[data-pn-act]'))    el('[data-pn-act]').innerHTML = htmlActions(c);
    }
  }

  /* ── un seul écouteur pour toute la page ────────────────────────────── */
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-bascule],[data-eng],[data-vider],[data-panier]') : null;
    if (!b) return;
    if (b.hasAttribute('data-bascule')) { e.preventDefault(); basculer(b.getAttribute('data-bascule')); return; }
    if (b.hasAttribute('data-panier'))  { e.preventDefault(); basculer(b.getAttribute('data-panier'));
      /* ajouté depuis une fiche : on montre le panier, sinon rien ne dit
         que le clic a servi à quelque chose */
      if (dedans(b.getAttribute('data-panier')) && !b.hasAttribute('data-panier-discret')) ouvrir();
      return; }
    if (b.hasAttribute('data-eng'))     { e.preventDefault(); etat.eng = b.getAttribute('data-eng'); ecrire(); return; }
    if (b.hasAttribute('data-vider'))   { e.preventDefault(); vider(); }
  });

  /* talos-paiement.js s'annonce après nous : le tiroir et la page Commander
     doivent reprendre leurs libellés une fois qu'on sait à quoi s'en tenir */
  document.addEventListener('paiement:pret', function () { rendre(); });

  /* un autre onglet a changé le panier */
  window.addEventListener('storage', function (e) {
    if (e.key === CLE) { lire(); rendre(); }
  });

  function demarrer() {
    lire();
    poserBouton();
    rendre();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', demarrer);
  } else {
    demarrer();
  }

  /* on expose le minimum : la page Commander n'a besoin de rien d'autre */
  window.TalosPanier = { ouvrir: ouvrir, etat: function () { return calcul(); }, AGENTS: AGENTS };
})();
