# -*- coding: utf-8 -*-
"""La barre passe aux menus volants : « Espace client » et « Réserver une
démo » deviennent deux boutons-icônes, chacun ouvre un panneau.

    python3 _build/flyout_nav.py

Remplace le lien texte de l'espace client et le bouton de démo dans toutes
les pages qui les portent, pose talos-ui.css / talos-ui.js, et recale les
empreintes de cache. Idempotent : un second passage ne change rien.

⚠️  nav_sync.py est en retard sur les pages en ligne — ne pas le relancer
    derrière (voir outils.py).
"""
import glob, hashlib, io, os, re

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def svg(d, w=1.7):
    return (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, d))


# jeu d'icônes ligne, tracé 1,7 px sur grille 24 — celui des panneaux de la barre
IC = {
    'user':  u'<path d="M12 15.4c-3.9 0-7.2.6-7.2 2.9s3.3 2.9 7.2 2.9 7.2-.6 7.2-2.9-3.3-2.9-7.2-2.9z"/>'
             u'<circle cx="12" cy="7.4" r="4.6"/>',
    'cal':   u'<rect x="3.5" y="5" width="17" height="15.5" rx="3.2"/><path d="M3.5 9.8h17M8.2 3v4M15.8 3v4"/>'
             u'<path d="M9.2 14.8l1.9 1.9 3.8-3.8"/>',
    'login': u'<path d="M14 4h3.2A2.8 2.8 0 0 1 20 6.8v10.4a2.8 2.8 0 0 1-2.8 2.8H14"/>'
             u'<path d="M4 12h10.5M10.8 8.2l3.8 3.8-3.8 3.8"/>',
    'plus':  u'<circle cx="10" cy="7.8" r="3.8"/><path d="M3.4 20.2a6.6 6.6 0 0 1 11.4-4.5"/>'
             u'<path d="M18.5 14.4v6.2M15.4 17.5h6.2"/>',
    'mail':  u'<rect x="3" y="5" width="18" height="14" rx="2.8"/><path d="M3.8 7.4l7 5a2 2 0 0 0 2.4 0l7-5"/>',
    'bag':   u'<path d="M5.4 8h13.2l-1 11.1a2 2 0 0 1-2 1.9H8.4a2 2 0 0 1-2-1.9z"/><path d="M9 10.4V7a3 3 0 0 1 6 0v3.4"/>',
    'tag':   u'<path d="M20.6 13.3l-7.3 7.3a1.9 1.9 0 0 1-2.7 0l-7.2-7.2a1.9 1.9 0 0 1-.5-1.3V4.6'
             u'a1.6 1.6 0 0 1 1.6-1.6h7.5c.5 0 1 .2 1.3.5l7.3 7.3a1.9 1.9 0 0 1 0 2.5z"/><circle cx="8.1" cy="8.1" r="1.3"/>',
    'video': u'<rect x="2.8" y="6" width="13" height="12" rx="2.8"/><path d="M15.8 10.4l4.6-2.7v8.6l-4.6-2.7z"/>',
    'calc':  u'<rect x="4.5" y="2.5" width="15" height="19" rx="2.8"/><path d="M8.2 6.8h7.6"/>'
             u'<path d="M8.4 11.4h.02M12 11.4h.02M15.6 11.4h.02M8.4 14.8h.02M12 14.8h.02M15.6 14.8h.02'
             u'M8.4 18.2h.02M12 18.2h.02M15.6 18.2h.02"/>',
    'play':  u'<circle cx="12" cy="12" r="9"/><path d="M10.3 8.9v6.2l4.9-3.1z"/>',
    'go':    u'<path d="M9 6l6 6-6 6"/>',
    'back':  u'<path d="M15 6l-6 6 6 6"/>',
    'key':   u'<rect x="5" y="10.5" width="14" height="10" rx="2.6"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    'check': u'<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6z"/><path d="M9 12l2.2 2.2 4.3-4.2"/>',
}


def item(href, ic, titre, sous, main=False, sub=None):
    cls = u'tfly-it is-main' if main else u'tfly-it'
    corps = (u'<span class="tfly-ic">%s</span><span class="tfly-tx"><b>%s</b><small>%s</small></span>'
             u'<svg class="tfly-go" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
             % (svg(IC[ic]), titre, sous, IC['go']))
    if sub is not None:
        return u'<li><button type="button" class="%s" data-tfly-sub="%d">%s</button></li>' % (cls, sub, corps)
    return u'<li><a class="%s" href="%s">%s</a></li>' % (cls, href, corps)


def vue(contenu, retour=None):
    tete = u''
    if retour:
        tete = (u'<button type="button" class="tfly-back">%s%s</button>'
                % (svg(IC['back'], 2), retour))
    return u'<div class="tfly-view">%s%s</div>' % (tete, contenu)


def entete(titre, sous):
    return u'<p class="tfly-hd"><b>%s</b><span>%s</span></p>' % (titre, sous)


def pied(ic, html):
    return u'<p class="tfly-ft">%s<span>%s</span></p>' % (svg(IC[ic]), html)


ESP = (
    u'<div class="tfly is-esp">'
    u'<button type="button" class="tfly-t" aria-label="Espace client" aria-expanded="false" '
    u'aria-controls="tfly-esp">%s</button>'
    u'<div class="tfly-pan" id="tfly-esp" hidden data-state="closed"><div class="tfly-track">'
    % svg(IC['user'], 1.8)
    + vue(entete(u'Espace client', u'Suivez ce que fait votre équipe Talos.')
          + u'<ul class="tfly-list">'
          + item('https://app.talos-ai.tech/', 'login', u'Se connecter',
                 u'Devis, factures et relances en cours', main=True)
          + item(None, 'plus', u'Pas encore client ?', u'Ouvrir un compte en ligne', sub=1)
          + item('mailto:contact@talos-ai.tech', 'mail', u'Besoin d’aide',
                 u'contact@talos-ai.tech')
          + u'</ul>'
          + pied('key', u'Votre accès arrive par e-mail après la commande.'))
    + vue(entete(u'Ouvrir un compte',
                 u'Le compte s’ouvre après le paiement : le lien d’accès part par e-mail.')
          + u'<ul class="tfly-list">'
          + item('commander.html', 'bag', u'Composer mon équipe',
                 u'Choisir ses assistants et commander', main=True)
          + item('tarifs.html', 'tag', u'Voir les tarifs', u'Dès 99 € TTC par mois')
          + item('reserver.html', 'video', u'Voir une démo d’abord',
                 u'30 minutes en visio, sans engagement')
          + u'</ul>', retour=u'Espace client')
    + u'</div></div></div>')

DEMO = (
    u'<div class="tfly tfly-demo">'
    u'<button type="button" class="tfly-t is-cta" aria-label="Réserver une démo" aria-expanded="false" '
    u'aria-controls="tfly-demo">%s</button>'
    u'<div class="tfly-pan" id="tfly-demo" hidden data-state="closed"><div class="tfly-track">'
    % svg(IC['cal'], 1.8)
    + vue(entete(u'Réserver une démo', u'30 minutes en visio, sur vos vrais devis.')
          + u'<ul class="tfly-list">'
          + item('reserver.html', 'cal', u'Choisir un créneau', u'En visio, à l\u2019heure qui vous va', main=True)
          + item('simulateur.html', 'calc', u'Estimer mon gain', u'Votre gain en 30 secondes')
          + item('comment-ca-marche.html', 'play', u'Voir comment ça marche',
                 u'Du premier mail à l’encaissement')
          + u'</ul>'
          + pied('check', u'Sans carte bancaire, sans engagement.'))
    + u'</div></div></div>')

BLOC = u'<!--tfly-->' + ESP + DEMO + u'<!--/tfly-->'
ANCIEN = re.compile(r'<a class="tnav-esp".*?</a>\s*<a class="tnav-cta"[^>]*>[^<]*</a>', re.S)
DEJA = re.compile(r'<!--tfly-->.*?<!--/tfly-->', re.S)


def empreinte(nom):
    return hashlib.md5(io.open(WEB + nom, 'rb').read()).hexdigest()[:8]


def ordonner_liens(s):
    """Barre du PC : Agents IA, Tarifs, Comment ça marche, puis Pourquoi
    Talos. Échange dans le balisage, pas en CSS (order) : l'ordre au clavier
    et celui des lecteurs d'écran suivent ainsi l'ordre affiché."""
    m = re.search(r'(<div class="tnav-links">)(.*?)(</div>)', s, re.S)
    if not m:
        return s
    inner = m.group(2)
    c = re.search(r'<a href="comment-ca-marche\.html"[^>]*>Comment ça marche</a>', inner)
    t = inner.find('<span class="tnav-drop"><a class="tnav-drop-t')
    t = inner.find('<span class="tnav-drop"><a class="tnav-drop-t', t + 1) if t >= 0 else -1
    while t >= 0 and 'href="tarifs.html"' not in inner[t:t + 120]:
        t = inner.find('<span class="tnav-drop"><a class="tnav-drop-t', t + 1)
    p = inner.find('<span class="tnav-drop"><a class="tnav-drop-t', t + 1) if t >= 0 else -1
    if not c or t < 0 or p < 0 or not (c.start() < t < p) or c.end() != t:
        return s     # déjà dans le bon ordre, ou barre inattendue : on n'y touche pas
    inner = inner[:c.start()] + inner[t:p] + inner[c.start():c.end()] + inner[p:]
    return s[:m.start(2)] + inner + s[m.end(2):]


def traiter(f):
    s = io.open(WEB + f, encoding='utf-8').read()
    avant = s
    s = ordonner_liens(s)
    s, n = ANCIEN.subn(lambda m: BLOC, s, count=1)
    if not n:
        s = DEJA.sub(lambda m: BLOC, s, count=1)

    # les deux fichiers du composant, posés à côté de talos-more
    if 'talos-ui.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="talos-more\.css[^"]*">)',
                   r'\1<link rel="stylesheet" href="talos-ui.css">', s, count=1)
    if 'talos-ui.js' not in s:
        s = re.sub(r'(<script src="talos-more\.js[^"]*" defer></script>)',
                   r'\1<script src="talos-ui.js" defer></script>', s, count=1)
    for nom in ('talos-ui.css', 'talos-ui.js', 'panier.js', 'panier.css'):
        s = re.sub(r'((?:href|src)="%s)(\?v=\w+)?"' % re.escape(nom),
                   r'\1?v=%s"' % empreinte(nom), s)

    if s != avant:
        io.open(WEB + f, 'w', encoding='utf-8').write(s)
        return u'mis à jour' + (u'' if 'tfly-demo' in s else u' (sans barre)')
    return u'déjà à jour'


if __name__ == '__main__':
    for p in sorted(glob.glob(WEB + '*.html')):
        f = os.path.basename(p)
        if 'talos-more.css' not in io.open(p, encoding='utf-8').read():
            continue
        print(u'%-28s %s' % (f, traiter(f)))
