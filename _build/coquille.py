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


def head(title, desc, og_title=None, og_desc=None, css='', noindex=False):
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
<meta name="twitter:card" content="summary_large_image">%s
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>
%s
%s
</style>
</head>
""" % (title, desc, og_title or title, og_desc or desc,
       u'\n<meta name="robots" content="noindex">' if noindex else u'',
       SHELL_CSS, css)


def page(fname, title, desc, css, body, js, og_title=None, og_desc=None,
         nav=True, footer=True, noindex=False):
    out = head(title, desc, og_title, og_desc, css, noindex)
    out += u'<body>\n<main>\n\n'
    if nav:
        out += NAV + u'\n\n'
    out += body
    if footer:
        out += u'\n\n' + FOOTER
    out += u'\n</main>\n\n<script>\n' + SHELL_JS + u'\n' + js + u'\n</script>\n</body>\n</html>\n'
    io.open(WEB + fname, 'w', encoding='utf-8').write(out)
    print(u'écrit : %s (%d octets)' % (fname, len(out)))
