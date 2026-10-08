# -*- coding: utf-8 -*-
"""Les outils gratuits du site : une page autonome par outil.

    python3 _build/outils.py        # écrit les pages outils + lien en pied de page
    python3 _build/seo.py           # titres, JSON-LD, sitemap, llms.txt

Ne régénère QUE les pages outils, et n'ajoute qu'une ligne au pied de
page des autres. Idempotent.

⚠️  Ne PAS passer nav_sync.py derrière : il est en retard sur les pages
    en ligne (anciennes icônes, « Solo, Pro, Business », lien espace
    client). C'est pourquoi la barre et le pied de page des outils sont
    recopiés depuis une page en ligne (REF) plutôt que tirés des parts.
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coquille import page, part, WEB

REF = 'simulateur.html'   # page de référence pour la barre et le pied
OUTILS = [
    (u'Calculateur TVA BTP', 'calculateur-tva-btp.html'),
]


def lire(f):
    return io.open(WEB + f, encoding='utf-8').read()


def ecrire(f, s):
    io.open(WEB + f, 'w', encoding='utf-8').write(s)


def sans_courant(s):
    s = s.replace(' aria-current="page"', '')
    return s.replace('tnav-drop-t is-here', 'tnav-drop-t')


def aligner(f):
    """Barre, menu, pied de page, feuilles de navigation et versions de
    cache : tout est repris de REF, tel qu'il est en ligne."""
    ref, s = lire(REF), lire(f)
    for pat in (r'<header class="tnav-wrap".*?</header>',
                r'<footer class="t-ft".*?</footer>',
                r'<style id="joints-css">.*?</style>',
                r'<style id="tnav-drop-css">.*?</style>'):
        bloc = sans_courant(re.search(pat, ref, re.S).group(0))
        s, n = re.subn(pat, lambda m: bloc, s, count=1, flags=re.S)
        if not n:
            # les deux feuilles de la barre ne sont pas dans la coquille
            assert pat.startswith('<style'), (f, pat)
            s = s.replace('</head>', bloc + '\n</head>', 1)
    # mêmes empreintes de cache que la page de référence
    for nom, v in re.findall(r'(?:href|src)="([\w-]+\.(?:css|js))\?v=(\w+)"', ref):
        s = re.sub(r'((?:href|src)="%s)(\?v=\w+)?"' % re.escape(nom), r'\1?v=%s"' % v, s)
    ecrire(f, s)


def lier_pied_de_page():
    """Ajoute chaque outil à la colonne « Navigation » de toutes les pages."""
    lignes = u''.join(u'\n          <li><a href="%s">%s</a></li>' % (h, t) for t, h in OUTILS)
    for f in sorted(os.listdir(WEB)):
        if not f.endswith('.html'):
            continue
        s = lire(f)
        m = re.search(r'(<h2>Navigation</h2>\s*<ul>.*?)(\s*</ul>)', s, re.S)
        if not m or OUTILS[0][1] in m.group(1):
            continue
        ecrire(f, s[:m.end(1)] + lignes + s[m.end(1):])
        print(u'pied de page : %s' % f)


page('calculateur-tva-btp.html',
     u"Calculateur TVA travaux 2026 : 5,5 %, 10 % ou 20 % | Talos",
     u"Quel taux de TVA pour vos travaux ? Répondez à 4 questions : taux, montant TTC "
     u"et mention à faire signer au client. Règles de la loi de finances 2026.",
     part('tva.css'), part('tva.html'), part('tva.js'))
aligner('calculateur-tva-btp.html')
lier_pied_de_page()
