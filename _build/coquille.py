# -*- coding: utf-8 -*-
"""La coquille commune à toutes les pages autonomes du site.

Extrait de pages.py pour qu'une page puisse être régénérée seule : lancer
pages.py réécrit une quinzaine de fichiers, ce qui est trop pour retoucher
une page. pages.py importe ce module, rien n'a changé pour lui.
"""
import os, io

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
P = WEB + '_build/parts/'


def part(name):
    return io.open(P + name, encoding='utf-8').read()


SHELL_CSS = part('shell.css')
NAV = part('nav.html')
FOOTER = part('footer.html')
SHELL_JS = part('shell.js')


#  Le site est servi sous cette adresse, avec l'extension .html
#  (vercel.json garde cleanUrls à false). C'est elle que les moteurs
#  doivent retenir, et celle que les réseaux sociaux vont chercher.
SITE = u'https://www.talos-ai.tech/'

#  Aperçu de partage : sans lui, une page envoyée sur WhatsApp ou
#  LinkedIn s'affiche en carte grise. 1200×630, le format attendu.
OG_IMAGE = SITE + u'og-talos.jpg'


def head(title, desc, og_title=None, og_desc=None, css='', noindex=False,
         fname=None):
    return u"""<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
<meta charset="utf-8">
<script>(function(){try{var t=localStorage.getItem('talos-theme')||'dark';document.documentElement.setAttribute('data-theme',t)}catch(e){}})();</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="author" content="Talos">
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Talos">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%s">%s%s
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="panier.css">
<link rel="stylesheet" href="talos-press.css">
<style>
%s
%s
</style>
<!-- chargées en dernier : à spécificité égale, ce sont elles qui gagnent -->
<link rel="stylesheet" href="talos-mobile.css">
<link rel="stylesheet" href="talos-more.css">
</head>
""" % (title, desc, og_title or title, og_desc or desc,
       OG_IMAGE, OG_IMAGE,
       (u'\n<link rel="canonical" href="%s%s">\n<meta property="og:url" content="%s%s">'
        % (SITE, fname, SITE, fname)) if (fname and not noindex) else u'',
       u'\n<meta name="robots" content="noindex">' if noindex else u'',
       SHELL_CSS, css)


def page(fname, title, desc, css, body, js, og_title=None, og_desc=None,
         nav=True, footer=True, noindex=False):
    out = head(title, desc, og_title, og_desc, css, noindex, fname)
    out += u'<body>\n<main>\n\n'
    if nav:
        out += NAV + u'\n\n'
    out += body
    if footer:
        out += u'\n\n' + FOOTER
    out += u'\n</main>\n\n<script>\n' + SHELL_JS + u'\n' + js + u'\n</script>\n'
    # le panier s'installe tout seul : bouton de barre, tiroir, boutons
    # « ajouter ». Chargé en dernier, il ne retarde rien.
    # talos-paiement.js doit passer AVANT panier.js : c'est lui qui dit
    # si l'achat en ligne est ouvert. defer conserve l'ordre de déclaration.
    out += u'<script src="talos-paiement.js" defer></script>\n'
    out += u'<script src="panier.js" defer></script>\n'
    # les paragraphes gris se replient derrière « En savoir plus » sur
    # téléphone : le script se pose tout seul, page par page
    out += u'<script src="talos-more.js" defer></script>\n'
    # l'inscription à la lettre : un seul comportement pour les deux
    # formulaires du site, celui du pied de page et celui du blog
    out += u'<script src="talos-lettre.js" defer></script>\n</body>\n</html>\n'
    io.open(WEB + fname, 'w', encoding='utf-8').write(out)
    print(u'écrit : %s (%d octets)' % (fname, len(out)))
