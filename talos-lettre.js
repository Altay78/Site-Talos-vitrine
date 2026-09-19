/* ═══════════════════════════════════════════════════════════════════════════
   TALOS · LA LETTRE D'INFORMATION

   ►►► UNE SEULE LIGNE À REMPLIR : ENDPOINT, juste en dessous. ◄◄◄

   Deux formulaires d'inscription vivent sur le site : celui du pied de page,
   présent sur toutes les pages, et celui du blog. Aucun des deux n'envoyait
   quoi que ce soit. Le premier ne faisait rien du tout au clic ; le second
   affichait « C'est noté — vous recevrez la prochaine édition » alors que
   l'adresse n'allait nulle part. Une inscription qu'on promet sans la tenir
   coûte plus cher qu'un formulaire absent.

   Tant qu'ENDPOINT est vide, les deux formulaires disent la vérité : ils
   renvoient vers l'adresse de contact, qui, elle, fonctionne. Dès qu'il est
   rempli, ils envoient pour de bon et confirment.

   Pour l'activer : collez l'adresse du formulaire de votre outil d'emailing
   (Brevo, Mailchimp, Buttondown…). Elle attend un POST avec le champ
   « email ». La plupart des outils la donnent sous « formulaire embarqué »
   ou « endpoint ».
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── 1 · VOTRE ADRESSE D'ENVOI ──────────────────────────────────────── */
  var ENDPOINT = '';

  /* ── 2 · OÙ L'ON RENVOIE TANT QUE CE N'EST PAS BRANCHÉ ──────────────── */
  var CONTACT = 'contact@talos-ai.tech';

  /* ── 3 · RIEN À TOUCHER EN DESSOUS ──────────────────────────────────── */

  var pret = /^https?:\/\/\S+$/.test(ENDPOINT.trim());

  function message(form, texte, ok) {
    var p = form.parentNode.querySelector('.lettre-dit');
    if (!p) {
      p = document.createElement('p');
      p.className = 'lettre-dit';
      p.setAttribute('role', 'status');
      form.parentNode.insertBefore(p, form.nextSibling);
    }
    p.classList.toggle('est-ok', !!ok);
    p.innerHTML = texte;
  }

  function brancher(form) {
    if (form.dataset.lettre) return;
    form.dataset.lettre = '1';
    /* le pied de page bloquait l'envoi en dur dans le markup */
    form.removeAttribute('onsubmit');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var champ = form.querySelector('input[type="email"]');
      var mail = champ ? champ.value.trim() : '';
      if (!mail || !champ.checkValidity()) {
        if (champ) champ.reportValidity();
        return;
      }

      if (!pret) {
        /* pas d'outil d'emailing branché : on ne fait pas semblant.
           On donne le seul chemin qui marche, pré-rempli. */
        var sujet = encodeURIComponent('Inscription à la lettre Talos');
        var corps = encodeURIComponent('Bonjour,\n\nMerci de m’inscrire à votre '
                    + 'lettre d’information avec cette adresse : ' + mail + '.\n');
        message(form,
          'Notre outil d’envoi n’est pas encore branché. '
          + '<a href="mailto:' + CONTACT + '?subject=' + sujet + '&body=' + corps + '">'
          + 'Envoyez-nous un mot</a> et on vous inscrit à la main.');
        return;
      }

      var bouton = form.querySelector('button[type="submit"], button:not([type])');
      if (bouton) { bouton.disabled = true; }
      var data = new FormData();
      data.append('email', mail);

      fetch(ENDPOINT, { method: 'POST', body: data, mode: 'cors' })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          /* le blog a déjà sa confirmation dessinée : on la réveille */
          var boite = form.closest('.letter');
          if (boite) boite.classList.add('sent');
          else message(form, 'C’est noté — vous recevrez la prochaine édition.', true);
        })
        .catch(function () {
          message(form, 'L’envoi n’a pas abouti. Écrivez-nous à '
            + '<a href="mailto:' + CONTACT + '">' + CONTACT + '</a>.');
        })
        .then(function () { if (bouton) bouton.disabled = false; });
    });
  }

  function init() {
    [].forEach.call(document.querySelectorAll('form.nform, #letter-form'), brancher);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
