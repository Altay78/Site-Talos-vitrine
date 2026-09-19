# -*- coding: utf-8 -*-
"""Le gabarit v2 des fiches assistant — huit blocs.

Il remplace le gabarit à quatre blocs de assistants.py. Ici on ne décrit que
la mise en forme : les contenus vivent dans fiches.py, un dictionnaire par
assistant. La feuille commune est parts/fiche.css, le script parts/fiche.js.

Rien de ce fichier ne doit contenir de texte visible par le visiteur — si une
phrase apparaît ici, c'est qu'elle a sa place dans fiches.py.
"""

# ═══════════════════════════════════════════════════════════════════════════
#  LES ICÔNES — Iconly Light, le jeu posé sur tout le site
# ═══════════════════════════════════════════════════════════════════════════

ICO = {
 'msg':    u'<path d="M 17.9 8.85L 13.46 12.46C 12.62 13.13 11.44 13.13 10.6 12.46L 6.12 8.85"/>'
           u'<path d="M 16.91 21C 19.95 21.01 22 18.51 22 15.44L 22 8.57C 22 5.5 19.95 3 16.91 3L 7.09 3C 4.05 3 2 5.5 2 8.57L 2 15.44C 2 18.51 4.05 21.01 7.09 21L 16.91 21Z"/>',
 'chat':   u'<path d="M 19.07 19.07C 16.02 22.13 11.49 22.79 7.79 21.07C 7.24 20.85 6.79 20.68 6.37 20.68C 5.18 20.68 3.7 21.83 2.93 21.07C 2.17 20.3 3.32 18.82 3.32 17.63C 3.32 17.2 3.15 16.76 2.93 16.21C 1.21 12.51 1.87 7.98 4.93 4.93C 8.83 1.02 15.17 1.02 19.07 4.93C 22.98 8.84 22.97 15.17 19.07 19.07Z"/>'
           u'<path d="M15.94 12.41L15.95 12.41"/><path d="M11.93 12.41L11.94 12.41"/><path d="M7.92 12.41L7.93 12.41"/>',
 'doc':    u'<path d="M15.72 16.22L8.5 16.22"/><path d="M15.72 12.04L8.5 12.04"/><path d="M11.25 7.86L8.5 7.86"/>'
           u'<path d="M 15.91 2.75C 15.91 2.75 8.23 2.75 8.22 2.75C 5.46 2.77 3.75 4.59 3.75 7.36L 3.75 16.55C 3.75 19.34 5.47 21.16 8.26 21.16C 8.26 21.16 15.93 21.16 15.95 21.16C 18.71 21.14 20.42 19.32 20.42 16.55L 20.42 7.36C 20.42 4.57 18.69 2.75 15.91 2.75Z"/>',
 'loop':   u'<path d="M 19.69 14.29C 20.51 13.32 21 12.06 21 10.69C 21 7.59 18.49 5.07 15.38 5.07H 8.61C 5.51 5.07 3 7.59 3 10.69C 3 13.79 5.51 16.3 8.61 16.3H 15.38"/>'
           u'<path d="M 12.77 13.68L 15.39 16.3L 12.77 18.93"/>',
 'clock':  u'<path d="M 21.25 12C 21.25 17.11 17.11 21.25 12 21.25C 6.89 21.25 2.75 17.11 2.75 12C 2.75 6.89 6.89 2.75 12 2.75C 17.11 2.75 21.25 6.89 21.25 12Z"/>'
           u'<path d="M15.43 14.94L11.66 12.69L11.66 7.85"/>',
 'edit':   u'<path d="M13.75 20.44L21 20.44"/>'
           u'<path d="M 12.78 3.79C 13.56 2.87 14.95 2.73 15.9 3.49C 15.95 3.53 17.63 4.84 17.63 4.84C 18.67 5.47 18.99 6.8 18.35 7.82C 18.32 7.88 8.81 19.76 8.81 19.76C 8.5 20.16 8.02 20.39 7.5 20.4L 3.86 20.44L 3.04 16.97C 2.93 16.48 3.04 15.97 3.36 15.58L 12.78 3.79Z"/>'
           u'<path d="M11.02 6L16.47 10.19"/>',
 'send':   u'<path d="M 15.83 8.17L 10.11 13.96L 3.6 9.89C 2.67 9.3 2.86 7.89 3.92 7.58L 19.37 3.05C 20.34 2.77 21.23 3.67 20.95 4.64L 16.37 20.09C 16.06 21.14 14.65 21.33 14.07 20.4L 10.11 13.96"/>',
 'shield': u'<path d="M 11.98 21.61C 11.98 21.61 19.66 19.28 19.66 12.88C 19.66 6.47 19.93 5.97 19.32 5.36C 18.7 4.74 12.99 2.75 11.98 2.75C 10.98 2.75 5.27 4.74 4.65 5.36C 4.03 5.97 4.31 6.47 4.31 12.88C 4.31 19.28 11.98 21.61 11.98 21.61Z"/>'
           u'<path d="M9.39 11.87L11.28 13.77L15.18 9.87"/>',
 'cal':    u'<path d="M3.09 9.4L20.92 9.4"/><path d="M16.44 13.31L16.45 13.31"/><path d="M12 13.31L12.01 13.31"/>'
           u'<path d="M7.56 13.31L7.57 13.31"/><path d="M16.44 17.2L16.45 17.2"/><path d="M12 17.2L12.01 17.2"/>'
           u'<path d="M7.56 17.2L7.57 17.2"/><path d="M16.04 2L16.04 5.29"/><path d="M7.97 2L7.97 5.29"/>'
           u'<path d="M 16.24 3.58L 7.77 3.58C 4.83 3.58 3 5.22 3 8.22L 3 17.27C 3 20.33 4.83 22 7.77 22L 16.23 22C 19.17 22 21 20.35 21 17.35L 21 8.22C 21.01 5.22 19.18 3.58 16.24 3.58Z"/>',
 'bell':   u'<path d="M 12 17.85C 17.64 17.85 20.25 17.12 20.5 14.22C 20.5 11.32 18.68 11.51 18.68 7.95C 18.68 5.16 16.05 2 12 2C 7.95 2 5.32 5.16 5.32 7.95C 5.32 11.51 3.5 11.32 3.5 14.22C 3.75 17.14 6.36 17.85 12 17.85Z"/>'
           u'<path d="M 14.39 20.86C 13.02 22.37 10.9 22.39 9.52 20.86"/>',
 'pin':    u'<path d="M 14.5 10.5C 14.5 9.12 13.38 8 12 8C 10.62 8 9.5 9.12 9.5 10.5C 9.5 11.88 10.62 13 12 13C 13.38 13 14.5 11.88 14.5 10.5Z"/>'
           u'<path d="M 12 21C 10.8 21 4.5 15.9 4.5 10.56C 4.5 6.39 7.86 3 12 3C 16.14 3 19.5 6.39 19.5 10.56C 19.5 15.9 13.2 21 12 21Z"/>',
 'cam':    u'<path d="M 15.04 4.05C 16.05 4.45 16.36 5.85 16.77 6.3C 17.19 6.75 17.78 6.91 18.1 6.91C 19.84 6.91 21.25 8.32 21.25 10.05L 21.25 15.85C 21.25 18.18 19.36 20.07 17.03 20.07L 6.97 20.07C 4.64 20.07 2.75 18.18 2.75 15.85L 2.75 10.05C 2.75 8.32 4.16 6.91 5.9 6.91C 6.22 6.91 6.81 6.75 7.23 6.3C 7.64 5.85 7.95 4.45 8.96 4.05C 9.97 3.65 14.03 3.65 15.04 4.05Z"/>'
           u'<path d="M17.5 9.5L17.5 9.5"/>'
           u'<path d="M 15.18 13.13C 15.18 11.37 13.76 9.95 12 9.95C 10.24 9.95 8.82 11.37 8.82 13.13C 8.82 14.88 10.24 16.31 12 16.31C 13.76 16.31 15.18 14.88 15.18 13.13Z"/>',
 'voice':  u'<path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3z"/>'
           u'<path d="M18.5 11.5a6.5 6.5 0 0 1-13 0M12 18.5V22"/>',
 'search': u'<path d="M2.78 11.77a8.99 8.99 0 1 0 17.98 0a8.99 8.99 0 1 0 -17.98 0"/><path d="M18.02 18.49L21.54 22"/>',
 'star':   u'<path d="M 13.1 4.18L 14.93 7.83C 15.11 8.19 15.46 8.43 15.86 8.49L 19.95 9.08C 20.96 9.23 21.36 10.45 20.63 11.15L 17.67 13.99C 17.38 14.27 17.25 14.67 17.32 15.07L 18.01 19.08C 18.19 20.07 17.13 20.83 16.23 20.36L 12.57 18.46C 12.22 18.28 11.79 18.28 11.43 18.46L 7.77 20.36C 6.87 20.83 5.81 20.07 5.99 19.08L 6.68 15.07C 6.75 14.67 6.62 14.27 6.33 13.99L 3.37 11.15C 2.64 10.45 3.04 9.23 4.05 9.08L 8.14 8.49C 8.54 8.43 8.89 8.19 9.07 7.83L 10.9 4.18C 11.35 3.27 12.65 3.27 13.1 4.18Z"/>',
 'bag':    u'<path d="M 6.69 11.38C 7.38 10.23 8.12 9.1 8.85 7.97L 6.87 4.28C 6.87 4.28 7.02 4.15 7.4 3.85C 8.53 2.98 9.76 2.76 11.09 3.27C 12.36 3.77 13.65 4.14 15.02 4.06C 15.42 4.04 16.96 3.84 16.96 3.84L 15.16 7.96C 15.88 9.09 16.62 10.23 17.31 11.38C 18.44 13.26 19.53 15.37 18.65 17.56C 17.63 20.11 14.64 20.96 12 21C 9.35 20.96 6.37 20.11 5.35 17.56C 4.47 15.37 5.56 13.26 6.69 11.38Z"/>'
           u'<path d="M 8.85 7.98C 10.95 8.46 13.05 8.46 15.16 7.98"/>',
 'filter': u'<path d="M10.33 16.59L4.03 16.59"/><path d="M13.14 6.9L19.44 6.9"/>'
           u'<path d="M 8.73 6.85C 8.73 5.55 7.67 4.5 6.36 4.5C 5.06 4.5 4 5.55 4 6.85C 4 8.14 5.06 9.19 6.36 9.19C 7.67 9.19 8.73 8.14 8.73 6.85Z"/>'
           u'<path d="M 20 16.55C 20 15.26 18.94 14.21 17.64 14.21C 16.33 14.21 15.27 15.26 15.27 16.55C 15.27 17.85 16.33 18.9 17.64 18.9C 18.94 18.9 20 17.85 20 16.55Z"/>',
 'chart':  u'<path d="M7.37 10.2L7.37 17.06"/><path d="M12.04 6.92L12.04 17.06"/><path d="M16.63 13.83L16.63 17.06"/>'
           u'<path d="M 16.69 2L 7.31 2C 4.05 2 2 4.31 2 7.59L 2 16.41C 2 19.69 4.04 22 7.31 22L 16.69 22C 19.96 22 22 19.69 22 16.41L 22 7.59C 22 4.31 19.96 2 16.69 2Z"/>',
 'grid':   u'<rect x="3" y="3" width="7.4" height="7.4" rx="2"/><rect x="13.6" y="3" width="7.4" height="7.4" rx="2"/>'
           u'<rect x="3" y="13.6" width="7.4" height="7.4" rx="2"/><path d="M17.3 13.6v7.4M13.6 17.3h7.4"/>',
 'lock':   u'<path d="M 16.42 9.45L 16.42 7.3C 16.42 4.79 14.39 2.75 11.87 2.75C 9.36 2.74 7.31 4.77 7.3 7.28L 7.3 7.3L 7.3 9.45"/>'
           u'<path d="M 15.68 21.25L 8.04 21.25C 5.95 21.25 4.25 19.55 4.25 17.46L 4.25 13.17C 4.25 11.07 5.95 9.38 8.04 9.38L 15.68 9.38C 17.78 9.38 19.48 11.07 19.48 13.17L 19.48 17.46C 19.48 19.55 17.78 21.25 15.68 21.25Z"/>'
           u'<path d="M11.86 14.2L11.86 16.42"/>',
 'info':   u'<path d="M 16.33 2.75L 7.67 2.75C 4.64 2.75 2.75 4.89 2.75 7.92L 2.75 16.08C 2.75 19.11 4.64 21.25 7.67 21.25L 16.33 21.25C 19.36 21.25 21.25 19.11 21.25 16.08L 21.25 7.92C 21.25 4.89 19.36 2.75 16.33 2.75Z"/>'
           u'<path d="M11.99 16L11.99 12"/><path d="M11.99 8.2L12 8.2"/>',
 'grille': u'<path d="M 12 8.72V 8.72"/>'
           u'<path d="M 14.45 5.05H 16.21C 18.85 5.05 21 7.2 21 9.86V 15.93C 21 18.58 18.85 20.74 16.21 20.74H 7.8C 5.15 20.74 3 18.58 3 15.93V 9.86C 3 7.2 5.15 5.05 7.8 5.05H 9.53"/>'
           u'<path d="M 14.46 5.17V 9.42C 14.46 10.47 13.61 11.32 12.56 11.32H 11.44C 10.39 11.32 9.54 10.47 9.54 9.42V 5.17C 9.54 4.12 10.39 3.27 11.44 3.27H 12.56C 13.61 3.27 14.46 4.12 14.46 5.17Z"/>',
 'user':   u'<path d="M 11.98 15.35C 8.12 15.35 4.81 15.93 4.81 18.27C 4.81 20.61 8.1 21.22 11.98 21.22C 15.85 21.22 19.15 20.63 19.15 18.29C 19.15 15.95 15.87 15.35 11.98 15.35Z"/>'
           u'<path d="M 11.98 12.01C 14.52 12.01 16.58 9.95 16.58 7.41C 16.58 4.87 14.52 2.81 11.98 2.81C 9.45 2.81 7.39 4.87 7.39 7.41C 7.38 9.94 9.42 12 11.95 12.01L 11.98 12.01Z"/>',
 'tick':   u'<path d="M20 6 9 17l-5-5"/>',
 'plus':   u'<path d="M12 5v14M5 12h14"/>',
 'chev':   u'<path d="M9 6l6 6-6 6"/>',
 'fleche': u'<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def svg(cle, trait='1.7', classe=None):
    return (u'<svg %sviewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (u'class="%s" ' % classe if classe else u'', trait, ICO[cle]))


CHEV = svg('chev', '2.4')


def ajouter(slug, texte=u"Ajouter à mon équipe"):
    """Le bouton d'ajout au panier. panier.js s'occupe du reste — libellé,
    icône et état suivent le contenu du panier."""
    return (u'<button type="button" data-panier="%s" data-panier-texte="%s">'
            u'<span data-panier-label>%s</span>'
            u'<span data-panier-ico aria-hidden="true"></span></button>'
            % (slug, texte, texte))
FLECHE = svg('fleche', '2.4')
TICK = svg('tick', '2.4')


# ═══════════════════════════════════════════════════════════════════════════
#  1 · HERO
# ═══════════════════════════════════════════════════════════════════════════

def _b1(f):
    # une ligne par mission, autant qu'il y en a — la grille les aligne
    atouts = u'\n'.join(
        u'        <li><i aria-hidden="true">%s</i>%s</li>' % (svg(ico, '1.8'), t)
        for ico, t in f['atouts'])
    return u'''<!-- ═══ 1 · HERO ══════════════════════════════════════════════════════════ -->
<section class="t-asst ac-hero">
  <div class="shell ac-hero-grid">

    <div class="ac-hero-media">
      <picture>
        <source srcset="perso/assistant-%(slug)s.webp" type="image/webp">
        <img class="perso" src="perso/assistant-%(slug)s.png" width="%(pw)d" height="%(ph)d"
             decoding="async" fetchpriority="high" alt="%(alt)s">
      </picture>
    </div>

    <div class="ac-hero-txt">
      <p class="ac-eyebrow">
        <img src="perso/avatar-%(slug)s.webp" width="26" height="26" alt="" decoding="async">
        %(role)s
      </p>

      <h1>%(h1)s</h1>

      <p class="ac-proof">
        <span class="ac-proof-i">%(bouclier)s<b>+75 intégrations</b> comprises</span>
        <span class="ac-proof-sep" aria-hidden="true"></span>
        <span class="ac-proof-i">%(coche)s Mise en place <b>personnalisée</b></span>
      </p>

      <p class="ac-lede">%(lede)s</p>

      <ul class="ac-atouts">
%(atouts)s
      </ul>

      <div class="actions">
        %(ajout)s
        <a class="btn btn-2" href="reserver.html">Voir une démonstration</a>
      </div>
    </div>

  </div>
</section>
''' % dict(f, atouts=atouts, fleche=CHEV, ajout=ajouter(f['slug']),
           bouclier=svg('shield', '1.9'), coche=svg('tick', '2'))


# ═══════════════════════════════════════════════════════════════════════════
#  2 · LES TROIS MISSIONS — le téléphone suit celle qu'on choisit
# ═══════════════════════════════════════════════════════════════════════════

def _b2(f):
    ecrans, onglets = [], []
    for i, (num, titre, texte, ico, shot, alt) in enumerate(f['missions'], 1):
        ecrans.append(
            u'              <img%s data-m="m%d" src="shots/%s.webp" width="780" height="1688" '
            u'loading="lazy" decoding="async" alt="%s">'
            % (u' class="on"' if i == 1 else u'', i, shot, alt))
        onglets.append(u'''        <button class="ac-mission" type="button" role="tab" id="acT%(i)d" data-m="m%(i)d"
                aria-selected="%(sel)s" aria-controls="acScreen">
          <span class="ac-mission-h">
            <span class="ac-mission-ic" aria-hidden="true">%(ico)s</span>
            <span class="ac-mission-n">%(num)s</span>
          </span>
          <h3>%(titre)s</h3>
          <p>%(texte)s</p>
        </button>''' % dict(i=i, sel=u'true' if i == 1 else u'false',
                            ico=svg(ico), num=num, titre=titre, texte=texte))

    return u'''

<!-- ═══ 2 · LES TROIS MISSIONS ════════════════════════════════════════════ -->
<section class="t-asst ac-miss" id="missions">
  <div class="shell">

    <div class="ac-miss-head">
      <h2 class="ac-h2">%(b2_h2)s</h2>
    </div>

    <div class="ac-miss-grid">

      <div class="ac-scene">
        <div class="ac-phone">
          <span class="ac-phone-k act"></span><span class="ac-phone-k vu"></span><span class="ac-phone-k vd"></span><span class="ac-phone-k pw"></span>
          <div class="ac-phone-bezel">
            <div class="ac-screen" id="acScreen" role="tabpanel" tabindex="0"
                 aria-labelledby="acT1">
%(ecrans)s
            </div>
          </div>
          <div class="ac-phone-glare"></div>
        </div>
      </div>

      <div class="ac-miss-list" role="tablist" aria-label="Les missions de %(role_bas)s">

%(onglets)s

      </div>
    </div>
  </div>
</section>
''' % dict(f, ecrans=u'\n'.join(ecrans), onglets=u'\n\n'.join(onglets))


# ═══════════════════════════════════════════════════════════════════════════
#  3 · LE SCÉNARIO — sept fiches qui se recouvrent au défilement
# ═══════════════════════════════════════════════════════════════════════════

def chips(*items):
    return (u'<ul class="ac-chips">'
            + u''.join(u'<li>%s</li>' % i for i in items) + u'</ul>')


def prix(*trios):
    """(libellé, montant, à la une) — la carte mise en avant porte .hot"""
    return (u'<ul class="ac-prices">'
            + u''.join(u'<li%s><small>%s</small><b>%s</b></li>'
                       % (u' class="hot"' if hot else u'', lib, val)
                       for lib, val, hot in trios) + u'</ul>')


def cite(texte):
    return u'<p class="ac-step-q">« %s »</p>' % texte


def dire(texte):
    return u'<p class="ac-step-p">%s</p>' % texte


def gain(montant, texte):
    return (u'<div class="ac-step-win"><b>%s</b><span>%s</span></div>'
            % (montant, texte))


def _b3(f):
    etapes = []
    for i, (jour, heure, horodate, ico, titre, corps) in enumerate(f['etapes']):
        jour_html = u'<span class="d">%s</span>' % jour if jour else u''
        etapes.append(u'''      <li class="ac-step" style="--i:%(i)d">
        <span class="ac-step-tab" aria-hidden="true">%(jour)s%(heure)s</span>
        <div class="ac-step-card">
          <div class="ac-step-h">
            <span class="ac-step-ic" aria-hidden="true">%(ico)s</span>
            <b>%(titre)s</b>
            <span class="ac-step-when">%(horodate)s</span>
          </div>
          <div class="ac-step-body">%(corps)s</div>
        </div>
      </li>''' % dict(i=i, jour=jour_html, heure=heure, ico=svg(ico),
                      titre=titre, horodate=horodate, corps=corps))

    return u'''

<!-- ═══ 3 · LE SCÉNARIO ═══════════════════════════════════════════════════ -->
<section class="t-asst ac-story" id="scenario">
  <div class="shell ac-story-grid">

    <div class="ac-story-txt">
      <p class="ac-tag">Cas pratique</p>
      <h2 class="ac-h2">%(b3_h2)s</h2>
      <p class="ac-sub">%(b3_sub)s</p>

      <div class="ac-story-note">
        <b>%(b3_note_t)s</b>
        %(b3_note_p)s
      </div>

      <div class="actions">
        <a class="btn btn-1" href="reserver.html">Je veux mon assistant%(e)s %(fleche)s</a>
      </div>
    </div>

    <ol class="ac-steps" id="acSteps" tabindex="0" role="group"
        aria-label="Le scénario étape par étape, à faire défiler horizontalement sur téléphone">

%(etapes)s

    </ol>
  </div>
</section>
''' % dict(f, etapes=u'\n\n'.join(etapes), fleche=CHEV)


# ═══════════════════════════════════════════════════════════════════════════
#  4 · LE DÉTAIL — quatre grandes cartes denses
# ═══════════════════════════════════════════════════════════════════════════

def _b4(f):
    cartes = []
    for c in f['cartes']:
        puces = u'\n'.join(
            u'          <li><i aria-hidden="true">%s</i>%s</li>' % (svg(ico, '1.8'), txt)
            for ico, txt in c['puces'])
        cartes.append(u'''      <article class="ac-card">
        <div class="ac-card-top">
          <img class="ac-card-av" src="perso/avatar-%(slug)s.webp" width="42" height="42" alt="" loading="lazy" decoding="async">
          <span class="ac-card-role">%(role)s</span>
          <span class="ac-card-n">%(n)02d fonctionnalités</span>
        </div>
        <p class="ac-card-lab">%(lab)s</p>
        <h3>%(titre)s</h3>
        <p class="ac-card-acc">%(acc)s <span>· %(acc2)s</span></p>
        <hr class="ac-card-sep">
        <p class="ac-card-cap">Ce qu'%(pronom)s fait :</p>
        <ul>
%(puces)s
        </ul>
        <a class="ac-card-go" href="%(href)s">%(cta)s %(chev)s</a>
      </article>''' % dict(c, slug=f['slug'], pronom=f['pronom'],
                           n=len(c['puces']), puces=puces, chev=CHEV))

    return u'''

<!-- ═══ 4 · LE DÉTAIL DES FONCTIONNALITÉS ═════════════════════════════════ -->
<section class="t-asst ac-feat" id="fonctionnalites">
  <div class="shell">

    <div class="ac-feat-head">
      <p class="ac-tag">Ce qu'%(pronom)s prend en charge</p>
      <h2 class="ac-h2">%(b4_h2)s</h2>
      <p class="ac-sub">%(b4_sub)s</p>
    </div>

    <div class="ac-feat-rail" tabindex="0" role="group"
         aria-label="Les fonctionnalités, à faire défiler horizontalement">

%(cartes)s

    </div>
  </div>
</section>
''' % dict(f, cartes=u'\n\n'.join(cartes))


# ═══════════════════════════════════════════════════════════════════════════
#  5 · LES OUTILS — deux bandeaux qui défilent en sens inverse
# ═══════════════════════════════════════════════════════════════════════════

OUTILS_1 = [
 ('whatsapp-icon', u'WhatsApp'), ('gmail', u'Gmail'), ('google-calendar', u'Google Agenda'),
 ('microsoft-outlook', u'Outlook'), ('microsoft-teams', u'Microsoft Teams'),
 ('telegram', u'Telegram'), ('messenger', u'Messenger'), ('instagram-icon', u'Instagram'),
 ('facebook-icon', u'Facebook'), ('linkedin', u'LinkedIn'), ('drive', u'Google Drive'),
]
OUTILS_2 = [
 ('stripe', u'Stripe'), ('calendly', u'Calendly'), ('google-sheets', u'Google Sheets'),
 ('microsoft-excel', u'Excel'), ('microsoft-onedrive', u'OneDrive'), ('dropbox', u'Dropbox'),
 ('slack', u'Slack'), ('notion', u'Notion'), ('trello', u'Trello'), ('asana-logo', u'Asana'),
 ('salesforce', u'Salesforce'),
]


def _bande(outils, rev=False):
    """Le contenu est écrit deux fois : la boucle du défilement est un
    translate de -50 %, il faut donc deux exemplaires identiques."""
    chip = (u'<span class="ac-chip"><img src="logos/%s.svg" alt="" loading="lazy" '
            u'width="22" height="22"><span>%s</span></span>')
    puces = u'\n        '.join(chip % o for o in outils * 2)
    return (u'    <div class="ac-belt-row%s">\n      <div class="ac-belt-track">\n        %s\n'
            u'      </div>\n    </div>' % (u' rev' if rev else u'', puces))


def _b5(f):
    return u'''

<!-- ═══ 5 · VOS OUTILS ════════════════════════════════════════════════════ -->
<section class="t-asst ac-tools" id="outils">
  <div class="shell ac-tools-head">
    <h2 class="ac-h2">%(b5_h2)s</h2>
    <p class="ac-sub">%(b5_sub)s</p>
    <p class="ac-tools-count">%(ico)s +75 intégrations disponibles</p>
  </div>

  <div class="ac-belt" aria-hidden="true">
%(r1)s
%(r2)s
  </div>

  <div class="shell">
    <p class="ac-tools-foot"><b>Et si votre outil n'est pas dans la liste ?</b>
      On le branche pendant la mise en place. C'est compris dans l'installation.</p>
  </div>
</section>
''' % dict(f, ico=svg('grid', '1.9'),
           r1=_bande(OUTILS_1), r2=_bande(OUTILS_2, rev=True))


# ═══════════════════════════════════════════════════════════════════════════
#  6 · LE DUO — l'assistant qui complète celui-ci
# ═══════════════════════════════════════════════════════════════════════════

def _b6(f):
    return u'''

<!-- ═══ 6 · LE DUO ════════════════════════════════════════════════════════ -->
<section class="t-asst ac-duo">
  <div class="shell">

    <div class="ac-duo-head">
      <p class="ac-tag">Encore plus fort à deux</p>
      <h2 class="ac-h2">%(b6_h2)s</h2>
    </div>

    <div class="ac-duo-card">
      <div class="ac-duo-pair">
        <img src="perso/avatar-%(slug)s.webp" width="82" height="82" alt="%(role)s" loading="lazy" decoding="async">
        <span class="ac-duo-plus" aria-hidden="true">%(plus)s</span>
        <img src="perso/avatar-%(duo_slug)s.webp" width="82" height="82" alt="%(duo_role)s" loading="lazy" decoding="async">
      </div>

      <div class="ac-duo-txt">
        <span class="ac-card-role">%(duo_role)s</span>
        <h3>%(duo_titre)s</h3>
        <p>%(duo_texte)s</p>
      </div>

      <div class="ac-duo-act">
        %(ajout_duo)s
        <a class="ac-duo-all" href="assistant-%(duo_slug)s.html">Voir sa fiche %(fleche)s</a>
      </div>
    </div>

  </div>
</section>
''' % dict(f, plus=svg('plus', '3'), chev=CHEV, fleche=FLECHE,
           ajout_duo=ajouter(f['duo_slug']))


# ═══════════════════════════════════════════════════════════════════════════
#  7 · AVANT / AVEC TALOS
#      Le tableau est dessiné en SVG sur ordinateur ; sous 760 px il cède la
#      place aux cartes empilées, qui portent aussi la sémantique.
# ═══════════════════════════════════════════════════════════════════════════

_CROIX = (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
          u'stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')
_COCHE = (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
          u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          u'<path d="M20 6 9 17l-5-5"/></svg>')


def _tableau_svg(lignes):
    """Six lignes de 66 px sous un bandeau d'en-tête de 68 px."""
    n = len(lignes)
    h = 68 + 66 * n
    bandes = u''.join(u'<rect x="1" y="%d" width="1038" height="66"/>' % (68 + 66 * i)
                      for i in range(1, n, 2))
    filets = u''.join(u'<path d="M1 %d.5h1038"/>' % (68 + 66 * i) for i in range(n))
    gauche = u''.join(u'<text x="92" y="%d">%s</text>' % (68 + 66 * i + 39, a)
                      for i, (a, _) in enumerate(lignes))
    droite = u''.join(u'<text x="612" y="%d">%s</text>' % (68 + 66 * i + 39, b)
                      for i, (_, b) in enumerate(lignes))
    ronds_g = u''.join(u'<circle cx="62" cy="%d" r="13"/>' % (68 + 66 * i + 33)
                       for i in range(n))
    croix = u''.join(u'<path d="M57.5 %.1fl9 9M66.5 %.1fl-9 9"/>'
                     % (68 + 66 * i + 28.5, 68 + 66 * i + 28.5) for i in range(n))
    ronds_d = u''.join(u'<circle cx="582" cy="%d" r="13"/>' % (68 + 66 * i + 33)
                       for i in range(n))
    coches = u''.join(u'<path d="M577 %.1fl3.4 3.6 6.8-7.2"/>' % (68 + 66 * i + 33.5)
                      for i in range(n))
    return u'''<svg viewBox="0 0 1040 %(h2)d" xmlns="http://www.w3.org/2000/svg"
           font-family="Helvetica Neue,Helvetica,Arial,sans-serif">
        <rect x=".5" y=".5" width="1039" height="%(h1)d" rx="24"
              fill="var(--ink-2)" stroke="var(--line-2)"/>
        <g fill="currentColor" color="var(--parch)" opacity=".035">%(bandes)s</g>
        <g stroke="var(--line)" stroke-width="1">%(filets)s<path d="M520.5 1v%(h)d"/></g>
        <text x="40" y="42" font-size="13" font-weight="700" letter-spacing="2.4"
              fill="var(--lin)">AVANT</text>
        <text x="560" y="42" font-size="13" font-weight="700" letter-spacing="2.4"
              fill="var(--bronze)">AVEC TALOS</text>
        <g font-size="16.5" fill="var(--lin)">%(gauche)s</g>
        <g font-size="16.5" font-weight="600" fill="var(--parch)">%(droite)s</g>
        <g fill="currentColor" color="var(--lin)">
          <g opacity=".14">%(ronds_g)s</g>
          <g stroke="var(--lin)" stroke-width="1.8" stroke-linecap="round" fill="none">%(croix)s</g>
        </g>
        <g>
          <g fill="var(--bronze)" opacity=".16">%(ronds_d)s</g>
          <g stroke="var(--bronze)" stroke-width="2.1" stroke-linecap="round"
             stroke-linejoin="round" fill="none">%(coches)s</g>
        </g>
      </svg>''' % dict(h=h, h1=h - 2, h2=h, bandes=bandes, filets=filets,
                       gauche=gauche, droite=droite, ronds_g=ronds_g, croix=croix,
                       ronds_d=ronds_d, coches=coches)


def _b7(f):
    cartes = u'\n'.join(
        u'        <tr><td class="av">%s</td><td class="ap">%s</td></tr>' % (a, b)
        for a, b in f['avant_apres'])

    return u'''

<!-- ═══ 7 · AVANT / AVEC TALOS ════════════════════════════════════════════ -->
<section class="t-asst ac-ba">
  <div class="shell">

    <div class="ac-ba-head">
      <p class="ac-tag">Le changement</p>
      <h2 class="ac-h2">%(b7_h2)s</h2>
    </div>

    <div class="ac-ba-svg" aria-hidden="true">
      %(tableau)s
    </div>

    <table class="ac-ba-table">
      <thead>
        <tr><th scope="col">Avant</th><th scope="col">Avec Talos</th></tr>
      </thead>
      <tbody>
%(cartes)s
      </tbody>
    </table>

  </div>
</section>
''' % dict(f, tableau=_tableau_svg(f['avant_apres']), cartes=cartes)


# ═══════════════════════════════════════════════════════════════════════════
#  8 · L'APPEL FINAL
# ═══════════════════════════════════════════════════════════════════════════

def _b8(f):
    reassure = u'\n'.join(
        u'      <li><i aria-hidden="true">%s</i>%s</li>' % (TICK, t)
        for t in f['b8_reassure'])
    return u'''

<!-- ═══ 8 · L'APPEL FINAL ═════════════════════════════════════════════════ -->
<section class="t-asst ac-cta">
  <div class="shell ac-cta-in">
    <img class="ac-cta-av" src="perso/avatar-%(slug)s.webp" width="84" height="84" alt="" loading="lazy" decoding="async">
    <h2>%(b8_h2)s</h2>
    <p>%(b8_sub)s</p>
    <div class="actions">
      %(ajout)s
      <a class="btn btn-2" href="reserver.html">Voir une démonstration</a>
    </div>
    <!-- deux formulations pour la même porte : talos-paiement.js montre la
         première le jour où la caisse est ouverte, la seconde d'ici là.
         On ne promet « commander » que quand on sait encaisser. -->
    <p class="ac-direct" data-achat hidden>Vous savez déjà ce qu'il vous faut ?
      <a href="commander.html">Commander en ligne, sans rendez-vous %(fleche)s</a></p>
    <p class="ac-direct" data-achat-sinon>Vous savez déjà ce qu'il vous faut ?
      <a href="commander.html">Composer mon équipe %(fleche)s</a></p>
    <ul class="ac-reassure">
%(reassure)s
    </ul>
  </div>
</section>
''' % dict(f, reassure=reassure, chev=CHEV, fleche=FLECHE,
           ajout=ajouter(f['slug']))


def corps(f):
    return (_b1(f) + _b2(f) + _b3(f) + _b4(f) + _b5(f) + _b6(f) + _b7(f) + _b8(f))
