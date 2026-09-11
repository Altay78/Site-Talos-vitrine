# -*- coding: utf-8 -*-
"""Génère le markup du calculateur de coût administratif (.t-gains).

Les huit lignes du tableau sont identiques à la virgule près : on les écrit
une fois ici plutôt que huit fois à la main. Les durées moyennes viennent
des relevés faits chez les artisans accompagnés.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__)) + '/parts/gains.html'

# (id, nom, sous-titre, minutes, unité 'sem'|'jour', quantité par défaut, coché, icône)
TASKS = [
    ('devis',   u'Devis',        u'Création de devis',        30, 'sem',  15, True,  'doc'),
    ('relance', u'Relance devis', u'Relances et suivi',         5, 'sem',  12, True,  'loop'),
    ('facture', u'Facturation',  u'Création et envoi',         15, 'sem',  12, True,  'doc'),
    ('impaye',  u'Impayés',      u'Relances impayés',          10, 'sem',   8, True,  'alert'),
    ('treso',   u'Trésorerie',   u'Suivi et prévisionnel',     30, 'sem',   1, False, 'chart'),
    ('mail',    u'E-mails',      u'Tri et réponses',           45, 'jour',  5, True,  'mail'),
    ('assist',  u'Assistant 24/7', u'Réponses clients',        15, 'jour',  5, True,  'bot'),
    ('rdv',     u'Rendez-vous',  u'Planification et rappels',  15, 'sem',  10, True,  'cal'),
]

ICONS = {
    'doc':   '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/>',
    'loop':  '<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/>',
    'alert': '<path d="M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'mail':  '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
    'bot':   '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M8 3h8"/><path d="M9 14h.01M15 14h.01"/>',
    'cal':   '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
}

SVG = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg>')

rows = []
for tid, name, sub, mins, unit, qty, on, ic in TASKS:
    dur = u'%d min' % mins + (u' / jour' if unit == 'jour' else u'')
    rows.append(u"""      <tr data-min="%d" data-unit="%s"%s>
        <td class="task">
          <div class="tk">
            <label class="chk"><input type="checkbox" %sdata-role="on" aria-label="Compter : %s"><span></span></label>
            <span class="ic">%s</span>
            <span><b>%s</b><em>%s</em></span>
          </div>
        </td>
        <td class="dur">%s</td>
        <td class="qty"><input type="number" min="0" max="200" step="1" value="%d" data-role="qty" aria-label="%s — combien par semaine"></td>
        <td class="tim" data-role="time">—</td>
        <td class="cst" data-role="cost">—</td>
      </tr>""" % (mins, unit, u'' if on else u' class="off"',
                  u'checked ' if on else u'', name, SVG % ICONS[ic],
                  name, sub, dur, qty, name))

HTML = u"""<!-- ═══ CALCULATEUR DE COÛT ADMINISTRATIF ═══ -->
<section class="t-gains" id="cout-administratif">
<div class="g-orb a"></div>
<div class="g-orb b"></div>

<div class="wrap">

  <div class="g-head">
    <span class="eyebrow"><i></i>Calculez vos gains</span>
    <h2>Découvrez ce que votre administratif <em>vous coûte</em> chaque mois.</h2>
    <p>Cochez les tâches que vous réalisez vraiment, ajustez les fréquences, et lisez le temps
       et l'argent que Talos peut vous rendre. Tout se calcule dans votre navigateur.</p>
  </div>

  <div class="g-grid">

    <!-- ── colonne saisie ── -->
    <div>
      <div class="g-rate">
        <div class="panel rate-in">
          <span class="lb">Combien vaut votre heure de travail&nbsp;?</span>
          <span class="fld">
            <input type="number" id="gRate" min="10" max="500" step="5" value="60" aria-label="Taux horaire en euros">
            <span class="cur">€</span>
          </span>
        </div>
        <p class="panel note">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M 21.25 12C 21.25 17.11 17.11 21.25 12 21.25C 6.89 21.25 2.75 17.11 2.75 12C 2.75 6.89 6.89 2.75 12 2.75C 17.11 2.75 21.25 6.89 21.25 12Z"/><path d="M15.43 14.94L11.66 12.69L11.66 7.85"/></svg>
          Durées moyennes constatées chez nos clients artisans du bâtiment.
        </p>
      </div>

      <div class="panel g-table">
        <table id="gTable">
          <thead>
            <tr>
              <th scope="col">Fonctionnalité</th>
              <th scope="col">Durée moyenne</th>
              <th scope="col">Combien par semaine</th>
              <th scope="col">Temps / semaine</th>
              <th scope="col">Coût / semaine</th>
            </tr>
          </thead>
          <tbody>
%s
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── colonne verdict ── -->
    <aside class="panel g-out">
      <div class="lgd">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M 21.25 12C 21.25 17.11 17.11 21.25 12 21.25C 6.89 21.25 2.75 17.11 2.75 12C 2.75 6.89 6.89 2.75 12 2.75C 17.11 2.75 21.25 6.89 21.25 12Z"/><path d="M15.43 14.94L11.66 12.69L11.66 7.85"/></svg>
        Votre estimation
      </div>
      <div class="tiles">
        <div class="tile"><b id="gHw">—</b><em>par semaine</em></div>
        <div class="tile"><b id="gHm">—</b><em>par mois</em></div>
        <div class="tile"><b id="gHy">—</b><em>par an</em></div>
        <div class="tile"><b id="gDy">—</b><em>jours / an</em></div>
      </div>

      <div class="lgd">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M 6.69 11.38C 7.38 10.23 8.12 9.1 8.85 7.97L 6.87 4.28C 6.87 4.28 7.02 4.15 7.4 3.85C 8.53 2.98 9.76 2.76 11.09 3.27C 12.36 3.77 13.65 4.14 15.02 4.06C 15.42 4.04 16.96 3.84 16.96 3.84L 15.16 7.96C 15.88 9.09 16.62 10.23 17.31 11.38C 18.44 13.26 19.53 15.37 18.65 17.56C 17.63 20.11 14.64 20.96 12 21C 9.35 20.96 6.37 20.11 5.35 17.56C 4.47 15.37 5.56 13.26 6.69 11.38Z"/><path d="M 8.85 7.98C 10.95 8.46 13.05 8.46 15.16 7.98"/></svg>
        Coût de votre administratif
      </div>
      <div class="tiles">
        <div class="tile"><b id="gCw">—</b><em>par semaine</em></div>
        <div class="tile"><b id="gCm">—</b><em>par mois</em></div>
        <div class="tile"><b id="gCy">—</b><em>par an</em></div>
        <div class="tile hot"><b id="gCy2">—</b><em>coût annuel</em></div>
      </div>

      <div class="lgd">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7.24 14.78L10.24 10.89L13.65 13.57L16.58 9.79"/><path d="M18.07 4.2a1.92 1.92 0 1 0 3.84 0a1.92 1.92 0 1 0 -3.84 0"/><path d="M 14.92 3.12L 7.66 3.12C 4.65 3.12 2.78 5.25 2.78 8.26L 2.78 16.35C 2.78 19.36 4.61 21.48 7.66 21.48L 16.26 21.48C 19.27 21.48 21.14 19.36 21.14 16.35L 21.14 9.31"/></svg>
        Votre comparaison
      </div>
      <div class="vs">
        <div class="side bad">
          <div class="k">Sans Talos</div>
          <div class="v" id="gNoTalos">—</div>
          <div class="s">Coût de votre administratif</div>
        </div>
        <div class="mid">VS</div>
        <div class="side good">
          <div class="k">Avec Talos</div>
          <div class="v">199&nbsp;€ <span style="font-size:.55em;font-weight:600">/ mois</span></div>
          <div class="s">Abonnement Pro, 3 tâches prises en charge</div>
        </div>
      </div>

      <div class="save">
        <div class="txt">
          <div class="k">Vous économiseriez</div>
          <div class="v" id="gSave">—</div>
        </div>
        <div class="pct"><b id="gPct">—</b><em>d'économies</em></div>
      </div>

      <p class="fine">Estimation basée sur les durées que vous avez saisies et sur nos relevés terrain.
         Nous comptons 4&nbsp;semaines par mois et 48&nbsp;semaines travaillées par an. Les gains réels
         dépendent de votre activité et de vos processus.</p>
    </aside>

  </div>

  <!-- ── réinvestissement ── -->
  <div class="panel g-reinv">
    <div class="lead">
      <span class="bolt"><svg width="21" height="21" viewBox="0 0 24 24" fill="currentColor"><path d="M 11.99 15.9L 14.11 12H 9.89L 12.01 8.1"/><path d="M 12 3C 16.97 3 21 7.03 21 12C 21 16.97 16.97 21 12 21C 7.03 21 3 16.97 3 12C 3 7.03 7.03 3 12 3Z"/></svg></span>
      <div>
        <h3>Réinvestissez votre temps là où ça compte vraiment.</h3>
        <p>Ce temps peut aller à vos chantiers, à votre développement commercial, ou tout simplement à votre vie personnelle.</p>
      </div>
    </div>

    <p class="verdict">
      Avec votre activité actuelle, vous pourriez récupérer jusqu'à
      <b id="gJobs">—</b> chantiers&nbsp;/&nbsp;mois, soit <b id="gCa">—</b>,
      tout en regagnant <b id="gHours">—</b> de votre temps&nbsp;!
    </p>

    <a class="cta" href="reserver.html">
      <span class="t">Essayez Talos <span class="arw"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></span>
      <span class="s">Démo de 15 minutes, sur vos vrais chiffres</span>
      <ul>
        <li>✓ Setup géré par nous</li>
        <li>✓ Sans engagement</li>
        <li>✓ Résiliable en 1 clic</li>
      </ul>
    </a>
  </div>

</div>
</section>
""" % u'\n'.join(rows)

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print(u'écrit : %s (%d octets)' % (OUT, len(HTML)))
