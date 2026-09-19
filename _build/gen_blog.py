# -*- coding: utf-8 -*-
"""Génère le markup de l'index du blog (.t-blog).

Le contenu vit ici, en clair : tant qu'il n'y a pas de CMS, une liste Python
se relit et se réordonne plus facilement que des blocs HTML copiés-collés.

Rendu adaptatif : une rubrique de moins de trois articles sort en grandes
cartes (deux par ligne, photo en 16/9), au-delà elle passe en deux colonnes
de brèves façon revue. Il suffit donc d'ajouter des entrées dans ARTICLES
pour que la page reprenne la mise en page longue, sans toucher au gabarit.

Photos : `img` est un chemin local. Les deux visuels actuels sont ceux déjà
utilisés sur le site (photos/), libres de droits.
"""
import io, os

OUT = os.path.dirname(os.path.abspath(__file__)) + '/parts/blog.html.part'

# rubrique -> (sous-titre, clé de couverture de repli, initiale)
RUBRIQUES = [
    (u'Facturation 2026', u'La réforme, sans le jargon : ce qui change vraiment pour une TPE.',
     'factures', 'F'),
    (u'Devis &amp; chiffrage', u'Chiffrer vite, envoyer avant les autres, relancer sans insister.',
     'devis', 'D'),
    (u'Relances &amp; trésorerie', u'Se faire payer, dans les temps, sans y passer ses soirées.',
     'treso', 'T'),
    (u'Terrain &amp; organisation', u'Ce que les artisans que nous accompagnons ont changé sur le chantier.',
     'chantier', 'C'),
    (u'Actualités Talos', u'Ce que nous construisons, et ce qui change pour vous.',
     'talos', 'T'),
]

# (rubrique, titre, chapô, auteur, date, lecture, image, texte alternatif, href)
ARTICLES = [
    (u'Facturation 2026',
     u"Facturation électronique 2026 : le calendrier réel, et les 4 réglages "
     u"à faire avant l'échéance",
     u"Réception obligatoire pour tout le monde, émission par vagues, plateforme "
     u"agréée, format Factur-X, e-reporting. On enlève le jargon et on ne garde que "
     u"ce qui change concrètement pour une entreprise du bâtiment de 1 à 20 personnes.",
     u'Altay Sakalli', u'2 août 2026', u'9 min',
     'photos/soir-ordinateur.jpg',
     u"Un artisan devant son ordinateur portable, le soir, à la lueur d'une bougie",
     '#'),

    (u'Devis &amp; chiffrage',
     u"Relancer un devis sans passer pour un vendeur",
     u"Trois messages, espacés au bon moment, qui font signer sans jamais donner "
     u"l'impression d'insister. Les textes exacts sont dans l'article.",
     u'Altay Sakalli', u'28 juillet 2026', u'6 min',
     'photos/chantier.jpg',
     u"Chantier de maison en cours : échafaudage, charpente et briques",
     '#'),
]

ARROW = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M9 6l6 6-6 6"/></svg>')


def _taille(chemin):
    """Dimensions du fichier, lues sur le disque. Sans elles le navigateur
    ne sait pas quelle place réserver et la page saute au chargement."""
    import struct
    plein = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + chemin
    try:
        with open(plein, 'rb') as f:
            d = f.read()
    except IOError:
        return None
    if d[:2] == b'\xff\xd8':                      # JPEG
        i = 2
        while i < len(d) - 9:
            if d[i] != 0xFF:
                i += 1; continue
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3):
                h, w = struct.unpack('>HH', d[i + 5:i + 9])
                return w, h
            if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                i += 2; continue
            i += 2 + struct.unpack('>H', d[i + 2:i + 4])[0]
        return None
    if d[:8] == b'\x89PNG\r\n\x1a\n':               # PNG
        w, h = struct.unpack('>II', d[16:24])
        return w, h
    return None


def cover(a, rub):
    """Photo si elle existe, sinon dégradé de rubrique avec l'initiale."""
    img = a[6]
    if img:
        t = _taille(img)
        dim = (u' width="%d" height="%d"' % t) if t else u''
        return (u'<span class="cov"><img src="%s" alt="%s"%s loading="lazy" '
                u'decoding="async"></span>' % (img, a[7], dim))
    return u'<span class="cov" data-c="%s" data-mono="%s" aria-hidden="true"></span>' % (
        rub[2], rub[3])


def _ecrit(a):
    """L'article est-il en ligne ? Tant que son adresse est '#', la carte
    ne se clique pas : un lien qui ne mène nulle part coûte plus cher que
    l'article qu'on n'a pas encore écrit."""
    return a[8] not in (None, '', '#')


def big_card(a, rub):
    pret = _ecrit(a)
    return u"""      <%s class="big%s"%s data-cat="%s">
%s
        <span class="meta"><span class="tag">%s</span><span class="dot">·</span><span>%s</span><span class="dot">·</span><span>%s</span></span>
        <h3>%s</h3>
        <p>%s</p>
        <span class="go">%s</span>
      </%s>""" % (
        'a' if pret else 'article',
        '' if pret else ' is-soon',
        (u' href="%s"' % a[8]) if pret else u'',
        a[0], '        ' + cover(a, rub), a[0], a[4], a[5], a[1], a[2],
        (u"Lire l'article " + ARROW) if pret else u'Bientôt',
        'a' if pret else 'article')


def breve(a, rub):
    pret = _ecrit(a)
    return u"""        <%s class="post%s"%s data-cat="%s">
%s
          <span class="bd">
            <span class="meta"><span>%s</span><span class="dot">·</span><span>%s</span><span class="dot">·</span><span>%s</span></span>
            <h3>%s</h3>
          </span>
        </%s>""" % (
        'a' if pret else 'article',
        '' if pret else ' is-soon',
        (u' href="%s"' % a[8]) if pret else u'',
        a[0], '          ' + cover(a, rub), a[3], a[4], a[5], a[1],
        'a' if pret else 'article')


def rub_of(name):
    for r in RUBRIQUES:
        if r[0] == name:
            return r
    return (name, u'', 'devis', name[:1].upper())


def section(name, sub, arts, tout=True):
    # moins de trois articles : la grille de brèves sonnerait creux
    if len(arts) < 3:
        body = u'    <div class="bigs">\n%s\n    </div>' % u'\n'.join(
            big_card(a, rub_of(a[0])) for a in arts)
    else:
        body = u'      <div class="posts">\n%s\n      </div>' % u'\n'.join(
            breve(a, rub_of(a[0])) for a in arts)
    lien = (u'<a class="all" href="#">Voir tous les articles %s</a>' % ARROW) if tout else u''
    return u"""    <section class="rub" data-rub="%s">
      <div class="rub-hd">
        <div>
          <h2>%s</h2>
          <div class="sub">%s</div>
        </div>
        %s
      </div>
%s
    </section>
    <div class="rub-sep"></div>""" % (name, name, sub, lien, body)


# En dessous de quatre articles, découper en rubriques laisserait une carte
# seule par ligne avec une demi-page de vide à côté : on regroupe.
if len(ARTICLES) < 4:
    sections = [section(u'Derniers articles',
                        u'Les premiers chapitres du carnet.',
                        ARTICLES, tout=False)]
else:
    sections = [section(n, sub, [a for a in ARTICLES if a[0] == n])
                for n, sub, _k, _m in RUBRIQUES
                if any(a[0] == n for a in ARTICLES)]

HTML = u"""<section class="t-blog" id="blog">

  <!-- ═══ HERO ═══ -->
  <div class="hero">
    <span class="halo"></span>
    <div class="wrap">
      <span class="eyebrow"><i></i>Le carnet de chantier</span>
      <h1>La paperasse du bâtiment, <em>démontée</em> pièce par pièce.</h1>
      <p class="lead">
        Devis, relances, facturation 2026, trésorerie. Des méthodes testées chez de vrais
        artisans, avec les chiffres, les modèles et le temps que ça fait gagner.
        Rien de théorique.
      </p>
    </div>
  </div>

  <div class="wrap">

    <!-- ═══ RUBRIQUES ═══ -->
%s

    <!-- ═══ LA SUITE ═══ -->
    <div class="soon">
      <span class="ic">%s</span>
      <div>
        <b>Le reste du carnet est en cours d'écriture.</b>
        <span>Impayés, trésorerie, organisation de chantier, cas clients : les prochains
              articles arrivent. Laissez votre adresse pour les recevoir.</span>
      </div>
    </div>

    <!-- ═══ LETTRE D'INFORMATION ═══ -->
    <div class="letter" id="letter">
      <div>
        <h2>Un e-mail par mois. <em>Rien à jeter.</em></h2>
        <p>Les échéances qui arrivent, un modèle prêt à l'emploi, et ce que les artisans
           accompagnés ont changé ce mois-ci. Désinscription en un clic.</p>
      </div>
      <div>
        <form id="letter-form">
          <input type="email" placeholder="Votre adresse e-mail" required aria-label="Votre adresse e-mail">
          <button type="submit">Je m'inscris</button>
        </form>
        <p class="ok">C'est noté — vous recevrez la prochaine édition.</p>
        <p class="fine">Pas de publicité, pas de revente d'adresse.</p>
      </div>
    </div>

  </div>
</section>
""" % (u'\n'.join(sections),
       '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1'
       'M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3.2"/></svg>')

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print(u'écrit : %s (%d octets, %d articles)' % (OUT, len(HTML), len(ARTICLES)))
