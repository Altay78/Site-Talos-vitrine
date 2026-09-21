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
        starter   1 assistant        m  mensuel   · mise en place OFFERTE
        business  2 ou 3 assistants  n  6 mois    · mise en place OFFERTE
        evolution 4 ou 5 assistants  y  12 mois   · mise en place OFFERTE

   ── Ce que chaque lien Stripe doit contenir ──────────────────────────
     • l'abonnement mensuel de la formule, au tarif de la durée choisie ;
     • aucune ligne de mise en place : elle est offerte sur les trois durées
       pendant le lancement, donc chaque lien ne porte que l'abonnement ;
     • aucune taxe à ajouter : laissez Stripe Tax éteint. Talos relève de la
       franchise en base, le prix affiché sur le site est le prix encaissé ;
     • dans les réglages du lien : « Ne pas afficher » la quantité, et
       page de confirmation → « Rediriger vers » l'adresse de MERCI ci-dessous.

   ── Le barème, pour vérification ──────────────────────────────────
                    mensuel         6 mois          12 mois
     Starter        99 €            89 €            82 €
     Business      299 €           269 €           249 €
     Évolution     449 €           399 €           369 €
     (TVA non applicable, article 293 B du CGI)
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── 1 · VOS LIENS STRIPE ───────────────────────────────────────────────
     Collez l'adresse complète, du style https://buy.stripe.com/xxxxxxxx   */
  var LIENS = {
    'starter-m':   'https://buy.stripe.com/6oU28scUnckY8H55h1eAg02',
    'starter-n':   'https://buy.stripe.com/5kQ28sbQj3OscXldNxeAg0c',
    'starter-y':   'https://buy.stripe.com/9B6bJ2cUndp27D15h1eAg06',

    'business-m':  'https://buy.stripe.com/dRm6oI8E7ckYbThcJteAg01',
    'business-n':  'https://buy.stripe.com/cNi14og6z1Gk7D110LeAg0a',
    'business-y':  'https://buy.stripe.com/eVqcN6aMfacQcXl10LeAg0b',

    'evolution-m': 'https://buy.stripe.com/dRm9AUbQj98MaPdcJteAg07',
    'evolution-n': 'https://buy.stripe.com/cNidRaaMffxabTh9xheAg09',
    'evolution-y': 'https://buy.stripe.com/14A3cw9Ib0Cge1pdNxeAg08'
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

  /* ── 2 bis · OÙ MÈNE LE BOUTON « COMMANDER » ───────────────────────────
     Plus directement chez Stripe : vers l'espace client, qui crée le compte
     s'il n'existe pas, puis rouvre le même lien Stripe avec l'identifiant
     du compte accroché.

     Sans ce détour, Stripe encaisse une carte et une adresse e-mail, et
     personne ne sait à quel compte ouvrir les assistants. C'est la seule
     étape qui garantit qu'un paiement aboutit toujours à un accès.

     Les liens ci-dessus restent la source : l'espace client lit la même
     grille, et un lien vide ici éteint le bouton comme avant.           */
  var SAS = 'https://app.talos-ai.tech/souscrire';

  /* le lien d'une combinaison précise, ou '' s'il manque
     ref : la sélection d'assistants, qu'on fait voyager avec la commande
           pour la retrouver en face du paiement */
  function lien(formule, eng, ref) {
    if (!propre(LIENS[formule + '-' + eng])) return '';
    var url = SAS + '?f=' + encodeURIComponent(formule) + '&e=' + encodeURIComponent(eng);
    if (ref) {
      /* même jeu de caractères que Stripe : la référence finira chez lui */
      ref = String(ref).replace(/[^A-Za-z0-9_-]+/g, '-').slice(0, 190);
      url += '&ref=' + ref;
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
