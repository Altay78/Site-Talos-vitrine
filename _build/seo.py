# -*- coding: utf-8 -*-
"""Référencement : titres, descriptions, données structurées, canonical,
sitemap.xml et llms.txt — pour tout le site, en un seul passage.

Passe APRÈS les autres scripts. pages.py, legal.py, crew.py, offres.py…
réécrivent le <head> de leurs pages : relancer l'un d'eux remet les
anciens titres et efface le JSON-LD. Il suffit alors de relancer :

    python3 _build/seo.py

Le script est idempotent : deux passages de suite ne changent rien.

Ce qu'il ne fait pas, volontairement :
  · aucune note ni aucun avis (aggregateRating) — Google sanctionne
    les avis inventés, et il n'y en a pas encore de publics ;
  · aucune promesse absente des pages : les prix viennent de panier.js,
    la FAQ est relue dans index.html, rien n'est recopié à la main.
"""
import io, json, os, re, subprocess, html

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = u'https://www.talos-ai.tech/'

# La même phrase partout : c'est elle que les moteurs et les IA doivent
# associer au nom « Talos », qui désigne aussi d'autres choses (Cisco
# Talos, des projets de recherche…).
ENTITE = (u"Talos est un assistant IA qui prépare les devis, les factures "
          u"et les relances des artisans et des entreprises du bâtiment.")

ORG_ID = SITE + u'#organisation'
SITE_ID = SITE + u'#site'
APP_ID = SITE + u'#logiciel'

# (fichier, titre ≤ 60 car., description ≤ 160 car.)
# None = garder ce que la page porte déjà.
PAGES = [
    ('index.html',
     u"Logiciel devis et facture IA pour artisans du BTP | Talos",
     u"Talos prépare vos devis, relance vos clients et prépare vos factures "
     u"pendant que vous êtes sur le chantier. +30 artisans du bâtiment accompagnés."),
    ('offres.html',
     u"Assistants IA pour artisans du BTP : les 5 offres | Talos",
     u"Cinq assistants IA qui gèrent devis, facturation, impayés, accueil "
     u"client et mails pendant que vous êtes sur le chantier. Mise en place incluse."),
    ('assistant-commercial.html',
     u"Devis automatique artisan : assistant commercial IA | Talos",
     u"Un devis préparé depuis un mail, un vocal ou une photo, signé en ligne "
     u"avec l'acompte, puis relancé jusqu'à la réponse du client."),
    ('assistant-facturation.html',
     u"Facturation automatique pour artisans du BTP | Talos",
     u"Chaque devis signé devient une facture conforme : acompte, situations "
     u"de travaux, TVA BTP, numérotation continue et archivage."),
    ('assistant-tresorerie.html',
     u"Relance automatique des impayés pour artisans | Talos",
     u"Talos repère les factures en retard, relance à J+7, J+15 et J+30, "
     u"prépare pénalités et mise en demeure, et annonce ce qui va rentrer."),
    ('assistant-client.html',
     u"Secrétariat IA 24 h/24 pour artisans du bâtiment | Talos",
     u"L'assistante client répond à vos clients jour et nuit, qualifie les "
     u"demandes, propose des créneaux compatibles avec vos trajets."),
    ('assistant-administratif.html',
     u"Tri des mails et classement automatique pour artisans | Talos",
     u"L'assistante administrative trie votre boîte mail en six catégories, "
     u"remonte les urgences et classe chaque pièce au bon chantier."),
    ('tarifs.html',
     u"Tarifs : logiciel devis et facture dès 99 €/mois | Talos",
     None),  # composée plus bas depuis panier.js
    ('comment-ca-marche.html',
     u"Comment fonctionne Talos, l'assistant IA des artisans",
     u"Rien à installer ni à apprendre : on configure Talos sur vos habitudes, "
     u"il prépare devis, relances et factures. Vous validez, c'est tout."),
    ('simulateur.html',
     u"Simulateur de gains : temps et chiffre récupérés | Talos",
     None),
    ('pourquoi-talos.html',
     u"À propos de Talos : l'IA née dans une famille d'artisans",
     u"Talos est né autour d'une table familiale d'artisans du BTP, pour leur "
     u"rendre le temps perdu dans l'administratif. Notre histoire, nos engagements."),
    ('blog.html',
     u"Blog Talos : devis, factures et relances pour le BTP",
     None),
    ('reserver.html',
     u"Démo Talos : 30 minutes sur vos vrais devis et factures",
     None),
    ('calculateur-tva-btp.html', None, None),  # titre posé par outils.py
    ('commander.html', None, None),
    ('mentions-legales.html', None, None),
    ('cgu.html', None, None),
    ('cgv.html', None, None),
    ('confidentialite.html', None, None),
]

ASSISTANTS = {
    'assistant-commercial.html': u"Assistant commercial",
    'assistant-facturation.html': u"Assistant facturation",
    'assistant-tresorerie.html': u"Assistante trésorerie",
    'assistant-client.html': u"Assistante client",
    'assistant-administratif.html': u"Assistante administrative",
}


def lire(f):
    return io.open(WEB + f, encoding='utf-8').read()


def ecrire(f, s):
    io.open(WEB + f, 'w', encoding='utf-8').write(s)


def url(f):
    return SITE if f == 'index.html' else SITE + f


def date_git(f):
    """Dernier commit du fichier : un dateModified qui ne ment pas."""
    try:
        d = subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', f],
                                    cwd=WEB, text=True).strip()
    except Exception:
        d = ''
    return d or None


def esc(s):
    return html.escape(s, quote=False).replace('"', '&quot;')


# ── la grille tarifaire, lue dans panier.js (seule source de vérité) ────
def paliers():
    js = lire('panier.js')
    out = []
    for m in re.finditer(r"\{ id: '(\w+)',\s*nom: '([^']+)',\s*max: (\d+),\s*"
                         r"setup: (\d+), p: \{ m: (\d+),\s*n: (\d+),\s*y: (\d+)\s*\} \}", js):
        out.append(dict(id=m.group(1), nom=m.group(2), max=int(m.group(3)),
                        setup=int(m.group(4)), m=int(m.group(5)), y=int(m.group(7))))
    assert len(out) == 3, u'grille introuvable dans panier.js'
    return out


# ── la FAQ, relue dans l'accordéon de l'accueil ─────────────────────────
def faq():
    s = lire('index.html')
    acc = s[s.find('<div class="acc" id="acc">'):]
    items = re.findall(r'<button class="q"[^>]*>\s*<span>(.*?)</span>.*?'
                       r'<div class="a-in">(.*?)</div>', acc, re.S)
    out = []
    for q, a in items:
        q = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', q))).strip()
        a = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', a))).strip()
        out.append((q, a))
    assert len(out) >= 5, u'FAQ introuvable dans index.html'
    return out


def faq_details(f):
    """FAQ en <details><summary> (pages outils), relue dans la page."""
    s = lire(f)
    out = []
    for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s, re.S):
        nettoie = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()
        out.append((nettoie(q), nettoie(a)))
    assert len(out) >= 3, u'FAQ introuvable dans %s' % f
    return out


def organisation():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Talos",
        "alternateName": "Talos AI",
        "url": SITE,
        "logo": {"@type": "ImageObject", "url": SITE + "apple-touch-icon.png",
                 "width": 180, "height": 180},
        "image": SITE + "og-talos.jpg",
        "description": ENTITE,
        "email": "contact@talos-ai.tech",
        "founder": {"@type": "Person", "name": "Altay Sakalli"},
        "identifier": {"@type": "PropertyValue", "propertyID": "SIREN",
                       "value": "920171774"},
        "areaServed": {"@type": "Country", "name": "France"},
        "knowsLanguage": "fr",
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                         "email": "contact@talos-ai.tech", "availableLanguage": "fr"},
        "sameAs": ["https://www.instagram.com/talos.ai.tech/"],
    }


def logiciel(grille):
    return {
        "@type": "SoftwareApplication",
        "@id": APP_ID,
        "name": "Talos",
        "description": ENTITE,
        "applicationCategory": "BusinessApplication",
        "applicationSubCategory": "Logiciel de devis et de facturation pour artisans",
        "operatingSystem": "Web",
        "url": SITE,
        "publisher": {"@id": ORG_ID},
        "audience": {"@type": "BusinessAudience",
                     "name": "Artisans et entreprises du bâtiment"},
        "featureList": ["Devis automatiques depuis un mail, un vocal ou une photo",
                        "Signature électronique et acompte",
                        "Relance des devis et des impayés",
                        "Factures conformes : acomptes, situations, TVA BTP",
                        "Prise de rendez-vous et réponses aux clients 24 h/24",
                        "Tri des mails et classement par chantier"],
        "offers": [{"@type": "Offer", "name": p['nom'], "price": str(p['m']),
                    "priceCurrency": "EUR", "url": SITE + "tarifs.html",
                    "category": "abonnement mensuel",
                    "description": "%d assistant%s, abonnement mensuel"
                                   % (p['max'], 's' if p['max'] > 1 else '')}
                   for p in grille],
    }


def fil(f, titre):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": titre, "item": url(f)}]}


def graphe(f, titre, desc, grille):
    page_type = "AboutPage" if f == 'pourquoi-talos.html' else "WebPage"
    page = {"@type": page_type, "@id": url(f) + "#page", "url": url(f),
            "name": titre, "inLanguage": "fr-FR",
            "isPartOf": {"@id": SITE_ID}, "publisher": {"@id": ORG_ID}}
    if desc:
        page["description"] = desc
    d = date_git(f)
    if d:
        page["dateModified"] = d
    if f == 'pourquoi-talos.html':
        page["mainEntity"] = {"@id": ORG_ID}

    g = [organisation(),
         {"@type": "WebSite", "@id": SITE_ID, "url": SITE, "name": "Talos",
          "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}},
         page]

    if f in ('index.html', 'tarifs.html', 'offres.html'):
        g.append(logiciel(grille))
    if f == 'index.html':
        g.append({"@type": "FAQPage", "@id": SITE + "#faq",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in faq()]})
    if f == 'calculateur-tva-btp.html':
        g.append({"@type": "WebApplication", "@id": url(f) + "#outil",
                  "name": "Calculateur de TVA pour travaux du BTP",
                  "description": desc, "url": url(f),
                  "applicationCategory": "BusinessApplication",
                  "operatingSystem": "Web", "browserRequirements": "JavaScript",
                  "inLanguage": "fr-FR", "isAccessibleForFree": True,
                  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
                  "publisher": {"@id": ORG_ID}})
        g.append({"@type": "FAQPage", "@id": url(f) + "#faq",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in faq_details(f)]})
    if f in ASSISTANTS:
        g.append({"@type": "Service", "@id": url(f) + "#service",
                  "name": ASSISTANTS[f] + " Talos", "description": desc,
                  "serviceType": ASSISTANTS[f],
                  "provider": {"@id": ORG_ID}, "areaServed": "FR",
                  "audience": {"@type": "BusinessAudience",
                               "name": "Artisans et entreprises du bâtiment"},
                  "url": url(f)})
    if f != 'index.html':
        g.append(fil(f, titre.split(' | ')[0]))
    return {"@context": "https://schema.org", "@graph": g}


def meta(s, attr, cle, valeur):
    """Remplace le content d'une balise <meta attr="cle">, ou l'ajoute."""
    pat = r'<meta %s="%s" content="[^"]*">' % (attr, re.escape(cle))
    neuf = u'<meta %s="%s" content="%s">' % (attr, cle, esc(valeur))
    if re.search(pat, s):
        return re.sub(pat, lambda m: neuf, s, count=1)
    return s.replace('</title>', '</title>\n' + neuf, 1)


def traiter(f, titre, desc, grille):
    s = lire(f)
    avant = s
    if titre:
        assert len(titre) <= 62, (f, len(titre))
        s = re.sub(r'<title>[^<]*</title>', lambda m: u'<title>%s</title>' % esc(titre), s, count=1)
        s = meta(s, 'property', 'og:title', titre)
    else:
        titre = html.unescape(re.search(r'<title>([^<]*)</title>', s).group(1))
    if desc:
        assert len(desc) <= 160, (f, len(desc))
        s = meta(s, 'name', 'description', desc)
        s = meta(s, 'property', 'og:description', desc)
    else:
        m = re.search(r'<meta name="description" content="([^"]*)">', s)
        desc = html.unescape(m.group(1)) if m else None

    # l'accueil est servi sous « / » : c'est cette adresse qui doit compter,
    # pas /index.html, que Google traiterait comme un doublon
    if f == 'index.html':
        s = s.replace('<link rel="canonical" href="%sindex.html">' % SITE,
                      '<link rel="canonical" href="%s">' % SITE)
        s = s.replace('<meta property="og:url" content="%sindex.html">' % SITE,
                      '<meta property="og:url" content="%s">' % SITE)

    bloc = (u'<!-- seo:jsonld — généré par _build/seo.py, ne pas éditer à la main -->\n'
            u'<script type="application/ld+json">\n%s\n</script>\n<!-- /seo:jsonld -->\n'
            % json.dumps(graphe(f, titre, desc, grille), ensure_ascii=False, indent=1)
              .replace('</', '<\\/'))
    # remplacé sur place : nav_sync.py repose ses feuilles juste avant
    # </head>, déplacer le bloc ferait se relayer les deux scripts sans fin
    s, n = re.subn(r'<!-- seo:jsonld .*?<!-- /seo:jsonld -->\n', lambda m: bloc, s, count=1, flags=re.S)
    if not n:
        s = s.replace('</head>', bloc + '</head>', 1)

    if s != avant:
        ecrire(f, s)
        return u'mis à jour'
    return u'déjà à jour'


def sitemap():
    lignes = [u'<?xml version="1.0" encoding="UTF-8"?>',
              u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f, _, _ in sorted(PAGES, key=lambda p: (p[0] != 'index.html', p[0])):
        d = date_git(f)
        lignes.append(u'  <url>\n    <loc>%s</loc>%s\n  </url>'
                      % (url(f), u'\n    <lastmod>%s</lastmod>' % d if d else u''))
    lignes.append(u'</urlset>\n')
    ecrire('sitemap.xml', u'\n'.join(lignes))


def llms(grille):
    """llms.txt : un résumé lisible par les IA. Effet non démontré sur le
    classement, mais il coûte dix minutes et lève toute ambiguïté."""
    def ligne(f):
        s = lire(f)
        t = html.unescape(re.search(r'<title>([^<]*)</title>', s).group(1)).split(' | ')[0]
        m = re.search(r'<meta name="description" content="([^"]*)">', s)
        return u'- [%s](%s): %s' % (t, url(f), html.unescape(m.group(1)) if m else u'')

    prix = u'\n'.join(u'- %s : %d € par mois (%d assistant%s), %d € par mois en engagement 12 mois'
                      % (p['nom'], p['m'], p['max'], 's' if p['max'] > 1 else '', p['y'])
                      for p in grille)
    txt = u"""# Talos

> %s Talos s'adresse aux TPE du BTP en France. Chaque document est validé par l'artisan avant envoi.

Éditeur : Altay Sakalli, entrepreneur individuel, SIREN 920 171 774. Contact : contact@talos-ai.tech.

## Produit

%s

## Assistants

%s

## Tarifs

%s

TVA non applicable. Détail : %starifs.html

## Outils gratuits

%s

## Entreprise

%s
- [Mentions légales](%smentions-legales.html)
""" % (ENTITE,
       u'\n'.join(ligne(f) for f in ('index.html', 'offres.html', 'comment-ca-marche.html')),
       u'\n'.join(ligne(f) for f in ASSISTANTS),
       prix, SITE,
       ligne('calculateur-tva-btp.html'),
       u'\n'.join(ligne(f) for f in ('pourquoi-talos.html', 'blog.html', 'reserver.html')),
       SITE)
    ecrire('llms.txt', txt)


if __name__ == '__main__':
    grille = paliers()
    # la remise affichée par le site, pas un arrondi recalculé ici
    remise = int(re.search(r"k: 'y'[^}]*?off: (\d+)", lire('panier.js')).group(1))
    desc_tarifs = (u"%s par mois. Jusqu'à −%d %% en vous engageant 12 mois. "
                   u"Comparez les formules du logiciel devis et facture Talos."
                   % (u', '.join(u'%s %d €' % (p['nom'], p['m']) for p in grille), remise))
    PAGES = [(f, t, desc_tarifs if f == 'tarifs.html' else d) for f, t, d in PAGES]
    for f, t, d in PAGES:
        print(u'%-28s %s' % (f, traiter(f, t, d, grille)))
    sitemap()
    llms(grille)
    print(u'sitemap.xml et llms.txt écrits')
