/* ═══ CALCULATEUR TVA BTP ═══════════════════════════════════════════
   Le moteur (tvaDecide) est une fonction pure : mêmes réponses, même
   taux. Il est testé à part (_build/test_tva.mjs) — toute règle ajoutée
   ici doit y recevoir son cas.
   Sources : CGI art. 278-0 bis A, 279-0 bis, 257 ter, 283-2 nonies ;
   BOFiP BOI-TVA-LIQ-30-20-90 et -95 du 09/09/2026 ; BOI-LETTRE-000280.
   ═════════════════════════════════════════════════════════════════ */
var TVA_MENTIONS = {
  '279': {
    devis: "Je soussigné(e) ............................ certifie, que les travaux réalisés concernent des locaux à usage d'habitation achevés depuis plus de deux ans et qu'ils n'auront pas pour effet, sur une période de deux ans au plus, de concourir à la production d'un immeuble neuf au sens du 2° du 2 du I de l'article 257 du CGI, ni d'entraîner une augmentation de la surface de plancher des locaux existants supérieure à 10 %.",
    facture: "Par le règlement de la présente facture, le client certifie, en qualité de preneur de la prestation, que les travaux réalisés concernent des locaux à usage d'habitation achevés depuis plus de deux ans, qu'ils n'ont pas eu pour effet, sur une période de deux ans au plus, de concourir à la production d'un immeuble neuf au sens du 2° du 2 du I de l'article 257 du CGI, ni d'entraîner une augmentation de la surface de plancher des locaux existants supérieure à 10 %."
  },
  '278': {
    devis: "Je soussigné(e) ............................ (Nom, prénoms) certifie, en qualité de preneur de la prestation, que les travaux réalisés concernent des locaux à usage d'habitation achevés depuis plus de deux ans, qu'ils n'auront pas pour effet, sur une période de deux ans au plus, de concourir à la production d'un immeuble neuf au sens du 2° du 2 du I de l'article 257 du CGI, ni d'entraîner une augmentation de la surface de plancher des locaux existants supérieure à 10 % et qu'ils ont la nature de travaux de rénovation énergétique.",
    facture: "Par le règlement de la présente facture, le client certifie, en qualité de preneur de la prestation, que les travaux réalisés concernent des locaux à usage d'habitation achevés depuis plus de deux ans, qu'ils n'ont pas eu pour effet, sur une période de deux ans au plus, de concourir à la production d'un immeuble neuf au sens du 2° du 2 du I de l'article 257 du CGI, ni d'entraîner une augmentation de la surface de plancher des locaux existants supérieure à 10 % et qu'ils ont la nature de travaux de rénovation énergétique."
  }
};

/*  r = { local, mixte50, age, trav, pacOk, surface, remiseNeuf,
          secondOeuvre, electro, clientAchete, soustraitance }
    → { taux (nombre ou null), libelle, dit, mention ('279'|'278'|null),
        alertes: [] , ventile: bool, autoliq: bool }                     */
function tvaDecide(r) {
  var alertes = [];
  var out = function (taux, dit, mention, extra) {
    var o = { taux: taux, libelle: taux === null ? '—' : String(taux).replace('.', ',') + ' %',
              dit: dit, mention: mention || null, alertes: alertes, ventile: false, autoliq: false };
    for (var k in extra) o[k] = extra[k];
    return o;
  };

  // 0 · sous-traitance : le sous-traitant ne facture pas la TVA
  if (r.soustraitance) {
    alertes.push("Écrivez « Autoliquidation » sur la facture et facturez hors taxes : c'est l'entreprise principale qui déclare la TVA.");
    alertes.push("C'est elle qui applique ensuite 5,5 %, 10 % ou 20 % au client final.");
    return out(0, "En sous-traitance du BTP, <b>vous ne facturez pas de TVA</b> : elle est autoliquidée par l'entreprise qui vous donne l'ordre (article 283-2 nonies du CGI).", null, { libelle: '0 %', autoliq: true });
  }

  // 1 · équipement handicap : régime propre, indépendant de l'âge du logement
  if (r.trav === 'handicap') {
    alertes.push("Seul un matériel spécialement conçu pour les personnes handicapées est concerné : un ascenseur ordinaire, même accessible en fauteuil, reste à 20 %.");
    alertes.push("Le vendeur doit certifier que l'appareil remplit les critères de l'annexe IV du CGI (article 30-0 C).");
    alertes.push("Les travaux d'adaptation courants (douche, barres d'appui) suivent la règle générale, en principe 10 %.");
    return out(5.5, "Un équipement <b>spécialement conçu pour les personnes handicapées</b>, comme un monte-escalier, est à 5,5 % : fourniture, pose, réparation et entretien.", null);
  }

  // 2 · ce qui est à 20 % quel que soit le local
  if (r.trav === 'neuf')
    return out(20, "Une construction, une extension ou une surélévation <b>crée de la surface neuve</b> : c'est le taux normal de 20 %.", null);
  if (r.trav === 'jardin')
    return out(20, "Les espaces verts et le nettoyage <b>sont exclus des taux réduits</b>, même chez un particulier : 20 %.", null);

  // 3 · le local doit être (ou devenir) un logement
  if (r.local === 'pro') {
    alertes.push("S'il devient un logement après les travaux, choisissez « Un local pro qui devient un logement ».");
    return out(20, "Un local <b>professionnel, commercial ou agricole</b>, ou un hébergement exploité commercialement comme un hôtel, n'ouvre pas droit aux taux réduits : 20 %.", null);
  }
  if (r.age === 'moins2')
    return out(20, "Le bâtiment a <b>moins de 2 ans</b> au début des travaux : les taux réduits ne s'appliquent pas, c'est 20 %.", null);

  // 4 · ce qui fait un immeuble neuf
  if (r.surface)
    return out(20, "Les travaux augmentent la surface de plancher <b>de plus de 10 %</b> : ils sont assimilés à une construction, à 20 %.", null);
  if (r.remiseNeuf || r.secondOeuvre)
    return out(20, "Les travaux <b>rendent l'immeuble à l'état neuf</b> (structure, façades ou second œuvre refait aux 2/3) : 20 % sur l'ensemble.", null);

  // 5 · équipements exclus par nature
  if (r.trav === 'chaudiere-fossile') {
    alertes.push("Les petits travaux indissociables de la pose (local chaudière, raccordements) suivent le même taux de 20 %.");
    alertes.push("L'entretien et la réparation d'une chaudière gaz ou fioul restent à 10 % : choisissez « Rénovation, aménagement, entretien ».");
    return out(20, "Depuis le 1<sup>er</sup> mars 2025, <b>toute chaudière gaz ou fioul</b> est à 20 %, y compris à condensation ou en PAC hybride.", null);
  }

  var base;
  if (r.trav === 'pac-air-air') {
    if (!r.pacOk)
      return out(20, "La climatisation et les PAC air/air sont <b>exclues du 10 %</b>. Sans les critères de 2026 (classe énergétique, fluide, pilotage à distance), c'est 20 %.", null);
    alertes.push("Le fluide frigorigène est apprécié à la date de signature du devis. Au-delà de 12 kW, d'autres seuils s'appliquent (efficacité saisonnière).");
    base = out(5.5, "Une PAC air/air réversible qui remplit les critères de 2026 entre dans la <b>rénovation énergétique</b> : 5,5 % depuis juillet 2026.", '278');
  } else if (r.trav === 'energie') {
    alertes.push("L'équipement doit figurer à l'annexe IV du CGI et respecter ses seuils de performance (fiche technique à garder).");
    alertes.push("Un appoint au gaz ou au fioul fait basculer l'installation à 20 %.");
    base = out(5.5, "Logement de plus de 2 ans et travaux de <b>rénovation énergétique</b> : 5,5 % sur la main-d'œuvre et les fournitures que vous posez.", '278');
  } else {
    base = out(10, "Logement de plus de 2 ans et travaux <b>d'amélioration, d'aménagement ou d'entretien</b> : 10 % sur la main-d'œuvre et les fournitures que vous posez.", '279');
  }

  // 6 · local mixte sous 50 % : on ventile
  if (r.local === 'mixte' && r.mixte50 === 'non') {
    base.ventile = true;
    base.dit += " Mais le local compte <b>moins de 50 % d'habitation</b> : ce taux ne vaut que pour les pièces exclusivement d'habitation (au prorata pour les parties communes), le reste est à 20 %.";
    alertes.unshift("Séparez sur le devis la part d'habitation (taux réduit) et la part professionnelle (20 %).");
  }
  if (r.local === 'pro-vers-logement')
    alertes.unshift("Le local doit devenir principalement un logement et les travaux ne doivent pas produire un immeuble neuf.");
  if (r.electro)
    alertes.push("L'électroménager et le mobilier non intégré restent à 20 %, même posés : mettez-les sur une ligne à part.");
  if (r.clientAchete)
    alertes.push("Le matériel acheté par le client lui coûte 20 % chez son fournisseur : vous ne facturez au taux réduit que la pose.");
  return base;
}

(function () {
  var form = document.getElementById('tvForm');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var eur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' });
  var dernier = null;

  function lire() {
    var f = form.elements, v = function (n) { var x = form.querySelector('input[name="' + n + '"]:checked'); return x ? x.value : null; };
    return {
      local: v('local'), mixte50: v('mixte50'), age: v('age'), trav: v('trav'),
      pacOk: f.pacOk.checked, surface: f.surface.checked, remiseNeuf: f.remiseNeuf.checked,
      secondOeuvre: f.secondOeuvre.checked, electro: f.electro.checked,
      clientAchete: f.clientAchete.checked, soustraitance: f.soustraitance.checked
    };
  }

  function montant() {
    var s = ($('tvHt').value || '').replace(/[\s  €]/g, '').replace(',', '.');
    var n = parseFloat(s);
    return isFinite(n) && n >= 0 ? n : null;
  }

  function rendre() {
    var r = lire(), d = tvaDecide(r);
    dernier = d;
    $('tvMixte').hidden = r.local !== 'mixte';
    $('tvPac').hidden = r.trav !== 'pac-air-air';
    // l'âge et les points de vigilance n'ont pas d'objet pour certains cas
    $('tvAgeCard').classList.toggle('is-off', r.trav === 'handicap' || r.local === 'pro');

    $('tvRate').innerHTML = d.ventile ? d.libelle + '<small>+ 20 %</small>' : d.libelle;
    $('tvPillRate').textContent = d.ventile ? d.libelle + ' + 20 %' : d.libelle;
    $('tvSay').innerHTML = d.dit;

    var ht = montant();
    var montre = ht !== null && !d.ventile;
    $('tvSums').hidden = !montre;
    if (montre) {
      var tva = Math.round(ht * d.taux) / 100;
      $('tvSHt').textContent = eur.format(ht);
      $('tvSTva').textContent = eur.format(tva);
      $('tvSTtc').textContent = eur.format(ht + tva);
    }

    var box = $('tvMentionBox');
    box.hidden = !d.mention;
    if (d.mention) {
      $('tvMention').textContent = TVA_MENTIONS[d.mention].devis;
      var ttc = ht !== null ? ht * (1 + d.taux / 100) : null;
      $('tvMentionWhy').textContent = (ttc !== null && ttc < 1000 && r.trav === 'amelioration')
        ? "Sous 1 000 € TTC d'entretien ou de réparation, elle n'est pas exigée : la facture doit alors indiquer le client, l'adresse, la nature des travaux et l'ancienneté du logement."
        : "Sans elle, le taux réduit tombe et c'est 20 % sur tout le chantier. Modèle officiel, à faire signer par le client.";
    }

    $('tvWarnBox').hidden = !d.alertes.length;
    $('tvWarn').innerHTML = d.alertes.map(function (a) { return '<li>' + a + '</li>'; }).join('');
  }

  form.addEventListener('change', rendre);
  $('tvHt').addEventListener('input', rendre);
  $('tvHt').addEventListener('blur', function () {
    var n = montant();
    if (n !== null) this.value = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 2 }).format(n);
  });

  $('tvCopy').addEventListener('click', function () {
    if (!dernier || !dernier.mention) return;
    var btn = this, txt = TVA_MENTIONS[dernier.mention].devis, lab = btn.querySelector('span');
    var ok = function () { lab.textContent = 'Mention copiée'; setTimeout(function () { lab.textContent = 'Copier la mention'; }, 2200); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () {});
  });

  // la pastille disparaît quand le panneau ou le guide est à l'écran
  var pill = $('tvPill');
  if (pill && 'IntersectionObserver' in window) {
    var vus = {};
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { vus[e.target.id || e.target.className] = e.isIntersecting; });
      var cache = Object.keys(vus).some(function (k) { return vus[k]; });
      pill.classList.toggle('is-gone', cache);
    });
    io.observe($('tvRes'));
    io.observe(document.querySelector('.tv-guide'));
  }

  rendre();
})();
