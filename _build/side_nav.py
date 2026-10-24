# -*- coding: utf-8 -*-
"""Le menu du téléphone devient un panneau latéral : l'équipe en tête,
visage par visage, puis la navigation à icônes, une carte de démo et
l'espace client avec l'interrupteur de thème.

    python3 _build/side_nav.py

Remplace <div class="tnav-menu"> dans toutes les pages qui le portent,
marque la page ouverte (aria-current) et recale les empreintes de cache
de talos-ui.css, talos-ui.js et panier.js. Idempotent : un second passage
ne change rien.

Habillage dans talos-ui.css (.tside), fermeture dans talos-ui.js.

⚠️  nav_sync.py est en retard sur les pages en ligne — ne pas le relancer
    derrière : il remettrait l'ancienne liste à plat.
"""
import glob, hashlib, io, os, re

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def svg(d, w=1.7):
    return (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, d))


# même tracé que les menus volants de la barre : 1,7 px sur grille 24
IC = {
    'how':   u'<circle cx="12" cy="12" r="9"/><path d="M10.3 8.9v6.2l4.9-3.1z"/>',
    'tag':   u'<path d="M20.6 13.3l-7.3 7.3a1.9 1.9 0 0 1-2.7 0l-7.2-7.2a1.9 1.9 0 0 1-.5-1.3V4.6'
             u'a1.6 1.6 0 0 1 1.6-1.6h7.5c.5 0 1 .2 1.3.5l7.3 7.3a1.9 1.9 0 0 1 0 2.5z"/><circle cx="8.1" cy="8.1" r="1.3"/>',
    'flame': u'<path d="M12 2.8c.6 3.1 2.4 4.6 4 6.2 1.6 1.6 2.6 3.3 2.6 5.5a6.6 6.6 0 0 1-13.2 0'
             u'c0-2.5 1.2-4 2.6-5.3"/><path d="M12 21a3.2 3.2 0 0 1-3.2-3.2c0-1.8 1.4-2.7 2.1-4'
             u'.4.8 1.7 2.1 2.6 2.1 4.4A3.2 3.2 0 0 1 12 21z"/>',
    'user':  u'<path d="M12 15.4c-3.9 0-7.2.6-7.2 2.9s3.3 2.9 7.2 2.9 7.2-.6 7.2-2.9-3.3-2.9-7.2-2.9z"/>'
             u'<circle cx="12" cy="7.4" r="4.6"/>',
    'cal':   u'<rect x="3.5" y="5" width="17" height="15.5" rx="3.2"/><path d="M3.5 9.8h17M8.2 3v4M15.8 3v4"/>'
             u'<path d="M9.2 14.8l1.9 1.9 3.8-3.8"/>',
    'go':    u'<path d="M9 6l6 6-6 6"/>',
    'down':  u'<path d="M6 9.5l6 6 6-6"/>',
    'arrow': u'<path d="M5 12h14M13 6l6 6-6 6"/>',
    'moon':  u'<path d="M21 12.7A8.6 8.6 0 1 1 11.3 3a6.7 6.7 0 0 0 9.7 9.7z"/>',
    'sun':   u'<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v1.8M12 19.6v1.8M4.4 4.4l1.3 1.3'
             u'M18.3 18.3l1.3 1.3M2.6 12h1.8M19.6 12h1.8M4.4 19.6l1.3-1.3M18.3 5.7l1.3-1.3"/>',
}

LOGO = (u'<svg viewBox="253 302 472 550" aria-hidden="true">'
        u'<mask id="tside-marteau" maskUnits="userSpaceOnUse" x="253" y="302" width="472" height="550">'
        u'<rect x="253" y="302" width="472" height="550" fill="#fff"/>'
        u'<path d="M 310 302 L 725 302 L 688 406 L 558 406 L 502 640 L 372 640 L 400 406 L 362 406 C 338 409 316 430 300 457 C 291 472 265 468 258 447 C 250 420 255 389 263 363 C 276 324 288 302 310 302 Z" fill="#000" stroke="#000" stroke-width="32" stroke-linejoin="round"/></mask>'
        u'<g mask="url(#tside-marteau)"><path d="M 494 536 L 642 536 L 399 852 L 459 684 Z" fill="#C75C24"/></g>'
        u'<path d="M 310 302 L 725 302 L 688 406 L 558 406 L 502 640 L 372 640 L 400 406 L 362 406 C 338 409 316 430 300 457 C 291 472 265 468 258 447 C 250 420 255 389 263 363 C 276 324 288 302 310 302 Z" fill="currentColor"/></svg>')

# Ceux qu'on peut commander d'abord ; les « Bientôt » ferment la liste,
# grisés et sans point vert.
EQUIPE = [
    ('commercial',    u'Assistant commercial',      u'Devis, signature, relances',    False),
    ('client',        u'Assistante client',         u'Réponses et rendez-vous',       False),
    ('facturation',   u'Assistant facturation',     u'Factures, acomptes, situations', False),
    ('administratif', u'Assistante administrative', u'Tri des mails et classement',   False),
    ('tresorerie',    u'Assistante trésorerie',     u'Impayés et relances',           True),
    ('juridique',     u'Assistante juridique',      u'Contrats et conformité',        True),
]

# (icône, libellé, href) ou (icône, libellé, [(libellé, href), …]) pour un groupe
NAV = [
    ('how',   u'Comment ça marche', 'comment-ca-marche.html'),
    ('tag',   u'Tarifs', [(u'Formules et tarifs', 'tarifs.html'),
                          (u'Simulateur', 'simulateur.html')]),
    ('flame', u'Pourquoi Talos', [(u'Notre histoire', 'pourquoi-talos.html'),
                                  (u'Blog', 'blog.html'),
                                  (u'Calculateur TVA', 'calculateur-tva-btp.html')]),
]


def cur(href, page):
    return u' aria-current="page"' if href == page else u''


def avatar(slug):
    return (u'<img src="perso/avatar-%s.webp" alt="" width="36" height="36" '
            u'loading="lazy" decoding="async">' % slug)


def side_html(page):
    i = [0]

    def li(corps):
        i[0] += 1
        return u'<li style="--i:%d">%s</li>' % (i[0] - 1, corps)

    ags = []
    for slug, nom, mission, bientot in EQUIPE:
        href = 'assistant-%s.html' % slug
        badge = u' <i class="tside-soon">Bientôt</i>' if bientot else u''
        ags.append(li(u'<a class="tside-ag%s" href="%s"%s><span class="tside-av">%s</span>'
                      u'<span class="tside-tx"><b>%s%s</b><small>%s</small></span></a>'
                      % (u' is-soon' if bientot else u'', href, cur(href, page),
                         avatar(slug), nom, badge, mission)))

    nav = []
    for ic, nom, cible in NAV:
        icone = u'<span class="tside-ic">%s</span>' % svg(IC[ic])
        if isinstance(cible, list):
            ici = any(h == page for _, h in cible)
            subs = u''.join(u'<li><a href="%s"%s>%s</a></li>' % (h, cur(h, page), t) for t, h in cible)
            nav.append(li(u'<details class="tside-grp%s"%s><summary class="tside-it">%s%s'
                          u'<svg class="tside-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                          u'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" '
                          u'aria-hidden="true">%s</svg></summary><ul class="tside-sub">%s</ul></details>'
                          % (u' is-here' if ici else u'', u' open' if ici else u'',
                             icone, nom, IC['down'], subs)))
        else:
            nav.append(li(u'<a class="tside-it" href="%s"%s>%s%s</a>'
                          % (cible, cur(cible, page), icone, nom)))

    pile = u''.join(avatar(s) for s, _, _, b in EQUIPE if not b)

    return (
        u'<!--tside--><div class="tnav-menu" id="tnav-menu">'
        u'<aside class="tside" aria-label="Menu">'
        u'<button type="button" class="tside-x" aria-label="Fermer le menu">%s</button>'
        u'<a class="tside-brand" href="index.html"><span class="tside-logo">%s</span>'
        u'<span class="tside-id"><small>Agents IA du BTP</small><b>Talos</b></span></a>'
        u'<nav class="tside-scroll" aria-label="Menu du téléphone">'
        u'<p class="tside-lb"><span>Votre équipe</span><a href="offres.html"%s>Tout voir%s</a></p>'
        u'<ul>%s</ul>'
        u'<p class="tside-lb"><span>Découvrir</span></p>'
        u'<ul>%s</ul>'
        u'</nav>'
        u'<section class="tside-card" aria-label="Démo" style="--i:%d">'
        u'<span class="tside-stack">%s</span>'
        u'<b>Voyez-les travailler</b>'
        u'<span class="tside-pitch">30 minutes en visio, sur vos vrais devis.</span>'
        u'<a class="tside-cta" href="reserver.html"%s>%sRéserver une démo</a>'
        u'</section>'
        u'<p class="tside-ft">'
        u'<a class="tside-row m-esp" href="https://app.talos-ai.tech/">%sEspace client</a>'
        u'<button type="button" class="theme-toggle tside-theme" aria-label="Changer de thème">'
        u'<span class="tside-knob">%s%s</span></button>'
        u'</p>'
        u'</aside></div><!--/tside-->'
        % (svg(IC['go'], 2.2), LOGO, cur('offres.html', page), svg(IC['arrow'], 2.2),
           u''.join(ags), u''.join(nav), i[0], pile,
           cur('reserver.html', page), svg(IC['cal'], 1.8), svg(IC['user']),
           svg(IC['moon'], 1.9).replace(u'<svg ', u'<svg class="moon" ', 1),
           svg(IC['sun'], 1.9).replace(u'<svg ', u'<svg class="sun" ', 1)))


ANCIEN = re.compile(r'<div class="tnav-menu" id="tnav-menu">.*?</div>', re.S)
DEJA = re.compile(r'<!--tside-->.*?<!--/tside-->', re.S)


def empreinte(nom):
    return hashlib.md5(io.open(WEB + nom, 'rb').read()).hexdigest()[:8]


def traiter(f):
    s = io.open(WEB + f, encoding='utf-8').read()
    avant = s
    bloc = side_html(f)
    s, n = DEJA.subn(lambda m: bloc, s, count=1)
    if not n:
        s, n = ANCIEN.subn(lambda m: bloc, s, count=1)
    for nom in ('talos-ui.css', 'talos-ui.js', 'panier.js'):
        s = re.sub(r'((?:href|src)="%s)(\?v=\w+)?"' % re.escape(nom),
                   r'\1?v=%s"' % empreinte(nom), s)
    if s != avant:
        io.open(WEB + f, 'w', encoding='utf-8').write(s)
        return u'mis à jour' + (u'' if n else u' (sans menu)')
    return u'déjà à jour'


if __name__ == '__main__':
    for p in sorted(glob.glob(WEB + '*.html')):
        f = os.path.basename(p)
        if 'talos-ui.css' not in io.open(p, encoding='utf-8').read():
            continue
        print(u'%-28s %s' % (f, traiter(f)))
