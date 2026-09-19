/* ═══════════════════════════════════════════════════════════════
   MERCI — on relit le panier une dernière fois pour montrer au
   client ce qu'il vient de commander, puis on le vide : revenir
   sur le site ne doit pas laisser croire qu'une commande traîne.
   Si le panier est vide (lien partagé, page rouverte plus tard),
   le récapitulatif reste masqué et le reste de la page suffit.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var NOMS = {
    commercial:    'Assistant commercial',
    tresorerie:    'Assistante trésorerie',
    client:        'Assistante client',
    facturation:   'Assistant facturation',
    administratif: 'Assistante administrative'
  };
  var ENG = {
    1:  'Sans engagement, résiliable à tout moment.',
    3:  'Engagement 3 mois · −10 % sur l’abonnement.',
    6:  'Engagement 6 mois · −20 % et mise en place offerte.',
    12: 'Engagement 12 mois · −30 % et mise en place offerte.'
  };
  var MOIS = { m: 1, q: 3, n: 6, y: 12 };

  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" ' +
    'aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

  try {
    var brut = JSON.parse(localStorage.getItem('talos-panier') || 'null');
    if (!brut || !Array.isArray(brut.agents) || !brut.agents.length) return;

    var liste = document.getElementById('mrListe');
    var eng = document.getElementById('mrEng');
    var bloc = document.getElementById('mrRecap');
    if (!liste || !bloc) return;

    liste.innerHTML = brut.agents.map(function (id) {
      return '<li>' + CHECK + (NOMS[id] || id) + '</li>';
    }).join('');
    if (eng) eng.textContent = ENG[MOIS[brut.eng]] || '';
    bloc.hidden = false;

    /* la commande est passée : le panier n'a plus lieu d'être */
    localStorage.removeItem('talos-panier');
  } catch (e) { /* stockage refusé : la page reste juste sans récapitulatif */ }
})();
