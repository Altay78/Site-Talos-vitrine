/* ═══════════════════════════════════════════════════════════════════════════
   TALOS · LE PAIEMENT

   ►►► C'EST LE SEUL FICHIER À REMPLIR. ◄◄◄

   Collez vos neuf liens de paiement Stripe dans le tableau LIENS ci-dessous,
   enregistrez, et l'achat en ligne s'allume tout seul sur tout le site :
   les boutons « Commander » apparaissent, le panier envoie vers Stripe.

   Tant qu'un seul lien manque, rien ne s'allume : le site continue de
   proposer la démo, comme aujourd'hui. On ne montre jamais un bouton
   d'achat qui ne mène nulle part.

   ── Comment lire une clé ──────────────────────────────────────────
     'business-n'  =  formule Business, engagement 6 mois
        starter   1 assistant        m  mensuel   · mise en place à régler
        business  2 ou 3 assistants  n  6 mois    · mise en place à régler
        evolution 4 ou 5 assistants  y  12 mois   · mise en place OFFERTE

   ── Ce que chaque lien Stripe doit contenir ──────────────────────────
     • l'abonnement mensuel de la formule, au tarif de la durée choisie ;
     • pour m et n seulement, les frais de mise en place en ligne séparée
       (produit à paiement unique) — sur y ils sont offerts, donc rien ;
     • aucune taxe à ajouter : laissez Stripe Tax éteint. Talos relève de la
       franchise en base, le prix affiché sur le site est le prix encaissé ;
     • dans les réglages du lien : « Ne pas afficher » la quantité, et
       page de confirmation → « Rediriger vers » l'adresse de MERCI ci-dessous.

   ── Le barème, pour vérification ──────────────────────────────────
                    mensuel         6 mois          12 mois
     Starter        99 € + 149 €   89 € + 149 €    82 €
     Business      299 € + 449 €  269 € + 449 €   249 €
     Évolution     449 € + 690 €  399 € + 690 €   369 €
     (TVA non applicable, article 293 B du CGI)
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── 1 · VOS LIENS STRIPE ───────────────────────────────────────────────
     Collez l'adresse complète, du style https://buy.stripe.com/xxxxxxxx   */
  var LIENS = {
    'starter-m':   '',
    'starter-n':   '',
    'starter-y':   '',

    'business-m':  '',
    'business-n':  '',
    'business-y':  '',

    'evolution-m': '',
    'evolution-n': '',
    'evolution-y': ''
  };

  /* ── 2 · LA PAGE DE REMERCIEMENT ────────────────────────────────────────
     Celle vers laquelle Stripe renvoie après un paiement réussi. À reporter
     à l'identique dans chacun des neuf liens, côté Stripe.               */
  var MERCI = 'merci.html';

  /* ── 3 · RIEN À TOUCHER EN DESSOUS ──────────────────────────────────────
     ═══════════════════════════════════════════════════════════════════════ */

  function propre(v) {
    v = (v || '').trim();
    /* un lien vide, un « à remplir » oublié ou une adresse qui n'est pas une
       adresse : on traite tout pareil, comme absent */
    return /^https?:\/\/\S+$/.test(v) ? v : '';
  }

  /* la grille est-elle complète ? c'est ce qui décide de tout allumer */
  function pret() {
    for (var k in LIENS) {
      if (Object.prototype.hasOwnProperty.call(LIENS, k) && !propre(LIENS[k])) return false;
    }
    return true;
  }

  /* le lien d'une combinaison précise, ou '' s'il manque
     ref : la sélection d'assistants, qu'on fait voyager avec le paiement
           pour la retrouver dans Stripe en face de la commande */
  function lien(formule, eng, ref) {
    var url = propre(LIENS[formule + '-' + eng]);
    if (!url) return '';
    if (ref) {
      /* Stripe n'accepte que lettres, chiffres, tiret et souligné */
      ref = String(ref).replace(/[^A-Za-z0-9_-]+/g, '-').slice(0, 190);
      url += (url.indexOf('?') >= 0 ? '&' : '?') + 'client_reference_id=' + ref;
    }
    return url;
  }

  /* ── l'allumage ─────────────────────────────────────────────────────────
     Les boutons d'achat sont écrits dans les pages avec l'attribut hidden
     et data-achat. Ils n'apparaissent que le jour où la grille est complète
     — donc jamais par accident, et sans clignotement au chargement.
     data-achat-sinon fait l'inverse : c'est le repli vers la démo, visible
     tant que l'achat n'est pas prêt.                                      */
  function allumer() {
    var ok = pret();
    [].forEach.call(document.querySelectorAll('[data-achat]'), function (el) {
      el.hidden = !ok;
    });
    [].forEach.call(document.querySelectorAll('[data-achat-sinon]'), function (el) {
      el.hidden = ok;
    });
    document.documentElement.classList.toggle('achat-pret', ok);
    /* le panier et la page Tarifs se redessinent d'eux-mêmes à ce signal */
    document.dispatchEvent(new CustomEvent('paiement:pret', { detail: { pret: ok } }));
  }

  /* On se présente AVANT d'allumer : allumer() prévient les autres scripts,
     et le premier réflexe de chacun est de nous interroger. Dans l'autre
     ordre, ils nous trouveraient absents et retomberaient sur la démo. */
  window.TalosPaiement = {
    pret: pret,
    lien: lien,
    merci: MERCI,
    /* pratique en console pour savoir ce qu'il reste à coller :
       TalosPaiement.manquants()  →  ['starter-m', 'business-n', …]        */
    manquants: function () {
      var out = [];
      for (var k in LIENS) {
        if (Object.prototype.hasOwnProperty.call(LIENS, k) && !propre(LIENS[k])) out.push(k);
      }
      return out;
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', allumer);
  } else {
    allumer();
  }
})();
