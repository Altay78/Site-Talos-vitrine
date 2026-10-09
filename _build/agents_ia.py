# -*- coding: utf-8 -*-
u"""Repositionne le site sur « agents IA pour artisans du BTP ».

index.html n'est plus régénéré (voir build.py) : on l'édite en place, comme
inject_crew.py. Les autres pages ne reçoivent que le libellé du menu.

    python3 _build/agents_ia.py
    python3 _build/seo.py          # titres, JSON-LD, sitemap, llms.txt

Le script est idempotent : chaque retouche vérifie qu'elle n'est pas déjà
faite. Ce qu'il change sur l'accueil :

  · une ligne catégorie dans le H1, au-dessus de la promesse ;
  · « vos agents IA s'en chargent » dans le sous-titre ;
  · un bloc « Talos, qu'est-ce que c'est ? » : la phrase que les moteurs et
    les IA doivent citer, et un tableau « Talos en bref » ;
  · les deux assistants « Bientôt » sortent du carrousel et du menu :
    une seule ligne sous la grille, on vend ce qui existe ;
  · l'agent responsable sous chaque étape « Du premier appel… » ;
  · la FAQ : une question « agent IA » et la réponse sur la transparence
    corrigée (règlement européen sur l'IA, art. 50) ;
  · les libellés de maquette (« Écran 01 · 340 × 720 px · WebP ») retirés ;
  · les images inlinées en base64 remplacées par leurs fichiers.
"""
import base64, hashlib, io, os, re, sys

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'

PAGES_MENU = ['index.html', 'offres.html', 'comment-ca-marche.html', 'tarifs.html',
              'simulateur.html', 'pourquoi-talos.html', 'blog.html', 'reserver.html',
              'commander.html', 'calculateur-tva-btp.html', '404.html',
              'assistant-commercial.html', 'assistant-facturation.html',
              'assistant-tresorerie.html', 'assistant-client.html',
              'assistant-administratif.html', 'mentions-legales.html', 'cgu.html',
              'cgv.html', 'confidentialite.html', 'merci.html']


def lire(f):
    return io.open(WEB + f, encoding='utf-8').read()


def ecrire(f, s):
    io.open(WEB + f, 'w', encoding='utf-8').write(s)


def remplace(s, avant, apres, deja=None):
    """Remplace une occurrence unique ; ne fait rien si `deja` est présent."""
    if (deja or apres) in s:
        return s
    assert s.count(avant) == 1, (avant[:80], s.count(avant))
    return s.replace(avant, apres)


# ═══════════════════════════════════════════════════════════════════════════
#  1 · LE MENU — « Agents IA » au lieu de « Offres », sans les « Bientôt »
# ═══════════════════════════════════════════════════════════════════════════

def menu(s):
    s = s.replace('href="offres.html">Offres<', 'href="offres.html">Agents IA<')
    s = s.replace('>Voir toutes les offres<', '>Voir les cinq agents IA<')
    # le menu mobile et le pied de page listent aussi « Offres »
    s = re.sub(r'(<a[^>]*href="offres\.html"[^>]*>)\s*Offres\s*(</a>)', r'\1Agents IA\2', s)
    s = re.sub(r'<span class="tnav-ag is-soon">(?:(?!<span class="tnav-ag|<a ).)*?</small></span>',
               '', s, flags=re.S)
    # un contact direct dans le pied de page : l'adresse est déjà publique
    # (mentions légales, JSON-LD), elle manquait là où on la cherche
    if 'href="mailto:contact@talos-ai.tech"' not in s:
        s = s.replace('<li><a href="reserver.html">Réserver une démo</a></li>\n        </ul>',
                      '<li><a href="reserver.html">Réserver une démo</a></li>\n'
                      '          <li><a href="mailto:contact@talos-ai.tech">Nous écrire</a></li>\n        </ul>', 1)
    return s


# ═══════════════════════════════════════════════════════════════════════════
#  2 · L'ACCUEIL
# ═══════════════════════════════════════════════════════════════════════════
CSS = u'''<style id="agents-ia-css">
/* agents_ia.py — catégorie du H1, bloc définition, agent par étape */
.hero-cat{display:block;margin:0 0 18px;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:12.5px;line-height:1.4;letter-spacing:.14em;text-transform:uppercase;font-weight:600;
  color:#E0631F}
html[data-theme="light"] .hero-cat{color:#B4491A}
.t-def{--bronze:#E0631F;--parch:#F6EEE7;--lin:#AB9F95;--ink:#140F0C;--ink-2:#1C1611;
  --line:rgba(246,238,231,.10);
  background:var(--ink);color:var(--parch);padding:88px 24px 8px;
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
html[data-theme="light"] .t-def{--bronze:#B4491A;--parch:#1C1310;--lin:#5E5149;--ink:#FBF6F2;
  --ink-2:#FFFFFF;--line:rgba(40,25,16,.14)}
.def-in{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.1fr .9fr;gap:40px;
  align-items:start;padding:36px;border:1px solid var(--line);border-radius:26px;
  background:linear-gradient(170deg,color-mix(in srgb,var(--bronze) 7%,var(--ink-2)),var(--ink-2))}
.def-in>*{min-width:0}
.def-k{margin:0 0 12px;font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:11.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--bronze)}
.t-def h2{margin:0 0 16px;font-size:clamp(26px,2.8vw,36px);line-height:1.08;letter-spacing:-1.2px;
  font-weight:800;color:var(--parch)}
.t-def p.def-a{margin:0;font-size:17px;line-height:1.65;color:var(--lin);max-width:60ch}
.t-def p.def-a strong{color:var(--parch);font-weight:700}
.def-t{width:100%;border-collapse:collapse;font-size:14.5px}
.def-t caption{text-align:left;margin-bottom:10px;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze)}
.def-t th,.def-t td{padding:11px 0;border-top:1px solid var(--line);text-align:left;vertical-align:top}
.def-t th{width:38%;font-weight:600;color:var(--parch);padding-right:16px}
.def-t td{color:var(--lin)}
@media (max-width:860px){.def-in{grid-template-columns:1fr;padding:26px}.t-def{padding-top:64px}}
.def-q{grid-column:1/-1;margin:8px 0 0;padding:26px 0 0;border-top:1px solid var(--line)}
.def-q blockquote{margin:0}
.def-q blockquote p{margin:0;font-size:clamp(20px,2vw,26px);line-height:1.3;letter-spacing:-.5px;
  font-weight:600;color:var(--parch);max-width:52ch}
.def-q figcaption{margin-top:12px;font-size:14px;color:var(--lin)}
.def-q cite{font-style:normal;font-weight:600;color:var(--parch)}
.int-lead{margin:12px auto 0;max-width:62ch;text-align:center;font-size:16px;line-height:1.6;
  color:var(--color-ink-soft,#8C8480)}
.crew-later{margin:14px auto 0;max-width:60ch;padding:0 24px;text-align:center;font-size:14px;
  line-height:1.6;color:var(--lin)}
.crew-later b{color:var(--parch);font-weight:600}
.t-feat .fx-agent{margin:10px 0 0;font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--acc,#E0631F)}
</style>
'''

DEF = u'''
<!-- ═══ DÉFINITION — agents_ia.py ═══════════════════════════════════════════ -->
<section class="t-def" id="talos" aria-labelledby="def-t">
  <div class="def-in">
    <div>
      <p class="def-k">Agents IA pour le BTP</p>
      <h2 id="def-t">Talos, qu’est-ce que c’est&nbsp;?</h2>
      <p class="def-a"><strong>Talos est une équipe d’agents IA pour les artisans et les entreprises
        du bâtiment.</strong> Cinq agents spécialisés préparent les devis, les factures, les relances
        d’impayés, les rendez-vous et le tri des mails, à partir de vos prix et de vos habitudes.
        Chaque document est validé par l’artisan avant envoi. Talos se connecte à 24 outils du
        métier, dont Batigest, EBP Bâtiment, Obat, Gmail et WhatsApp Business. L’offre démarre à
        99&nbsp;€ par mois pour un agent, mise en place incluse, et plus de 30 artisans du bâtiment
        sont déjà accompagnés.</p>
    </div>
    <table class="def-t">
      <caption>Talos en bref</caption>
      <tbody>
        <tr><th scope="row">Pour qui</th><td>Artisans et TPE du bâtiment, en France</td></tr>
        <tr><th scope="row">Ce que font les agents</th><td>Devis, factures, relances, rendez-vous, tri des mails</td></tr>
        <tr><th scope="row">Qui décide</th><td>Vous : rien ne part sans votre validation</td></tr>
        <tr><th scope="row">Mise en route</th><td>0 formation, mise en place incluse</td></tr>
        <tr><th scope="row">Données</th><td>Hébergées en France, jamais utilisées pour entraîner un modèle public</td></tr>
        <tr><th scope="row">Prix</th><td>À partir de 99&nbsp;€ par mois pour un agent</td></tr>
      </tbody>
    </table>
    <figure class="def-q">
      <blockquote><p>« Nous ne croyons pas à une IA qui remplace les humains. Nous croyons à une IA
        qui leur rend du temps. »</p></blockquote>
      <figcaption><cite>Altay Sakalli</cite>, fondateur de Talos, issu d’une famille d’artisans du BTP</figcaption>
    </figure>
  </div>
</section>
'''

# (titre de l'étape, agent qui la prend en charge)
ETAPES = [(u'Demande', u'Assistante client'), (u'Devis', u'Assistant commercial'),
          (u'Relance', u'Assistant commercial'), (u'Facture', u'Assistant facturation'),
          (u'Paiement', u'Assistante trésorerie'), (u'Planning', u'Assistante client')]

FAQ_AGENT = u'''
      <div class="item open">
        <button class="q" aria-expanded="true">
          <span>C’est quoi, un agent IA pour artisan&nbsp;?</span>
          <span class="plus"></span>
        </button>
        <div class="a"><div class="a-in">
          Un agent IA est un logiciel qui mène une tâche de bout en bout à votre place : il lit
          la demande, prépare le devis, la facture ou la relance, puis vous le soumet. Chez Talos,
          chaque agent a un métier (devis, factures, impayés, clients, mails) et rien ne part sans
          votre validation.
        </div></div>
      </div>
'''

ALT_CREW = {
    'client': u"Assistante client Talos, l'agent IA qui répond à vos clients",
    'commercial': u"Assistant commercial Talos, l'agent IA qui prépare vos devis",
    'facturation': u"Assistant facturation Talos, l'agent IA qui prépare vos factures",
    'tresorerie': u"Assistante trésorerie Talos, l'agent IA qui relance vos impayés",
    'administratif': u"Assistante administrative Talos, l'agent IA qui trie vos mails",
}

ALT_SHOTS = [u"Écran Talos en fin de journée : les devis déjà prêts à valider",
             u"Écran Talos : réponse au client en un quart d'heure",
             u"Écran Talos : relances et encaissements suivis automatiquement"]


def base64_vers_fichiers(s):
    """Chaque image inlinée devient un fichier : l'existant si le contenu est
    identique (logos/int/), sinon un nouveau fichier nommé d'après son alt."""
    connus = {}
    for d in ('logos/int', 'photos'):
        for f in os.listdir(WEB + d):
            p = WEB + d + '/' + f
            if os.path.isfile(p):
                connus[hashlib.sha1(open(p, 'rb').read()).hexdigest()] = d + '/' + f

    def sub(m):
        mime, data = m.group(1), m.group(2)
        brut = base64.b64decode(data)
        h = hashlib.sha1(brut).hexdigest()
        if h not in connus:
            alt = re.search(r'alt="([^"]*)"', s[m.end():m.end() + 600])
            nom = re.sub(r'[^a-z0-9]+', '-', (alt.group(1) if alt else h[:10]).lower()
                         .replace(u'é', 'e').replace(u'è', 'e').replace(u"'", '-')).strip('-')[:48]
            ext = 'webp' if 'webp' in mime else 'png'
            d = 'photos' if ext == 'webp' else 'logos/int'
            chemin = '%s/%s.%s' % (d, nom or h[:10], ext)
            open(WEB + chemin, 'wb').write(brut)
            connus[h] = chemin
        return 'src="%s"' % connus[h]

    return re.sub(r'src="data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]+)"', sub, s)


def accueil():
    s = lire('index.html')

    s = re.sub(r'<style id="agents-ia-css">.*?</style>\n', '', s, flags=re.S)
    s = remplace(s, '</head>', CSS + '</head>')

    # H1 : la catégorie d'abord, la promesse ensuite
    s = remplace(s, 'lg:text-[4.25rem]">Votre bureau tourne',
                 u'lg:text-[4.25rem]"><span class="hero-cat">Agents IA pour artisans et entreprises '
                 u'du BTP</span>Votre bureau tourne', deja='class="hero-cat"')
    s = remplace(s, u'votre assistant s’en charge.', u'vos agents IA s’en chargent.')

    # bloc définition, juste après la bande « On se branche à vos outils »
    s = re.sub(r'\n<!-- ═══ DÉFINITION — agents_ia\.py.*?</section>\n', '', s, flags=re.S)
    s = remplace(s, u'\n<!-- ═══ ÉQUIPE', DEF + u'\n<!-- ═══ ÉQUIPE')
    # une phrase sous « On se branche à vos outils » : ce que les logos ne disent pas
    s = remplace(s, u'<h2 class="int-sub">On se branche à vos outils.</h2>',
                 u'<h2 class="int-sub">On se branche à vos outils.</h2><p class="int-lead">Talos se '
                 u'connecte à 24 outils que les artisans utilisent déjà : messagerie, agenda, logiciels '
                 u'de devis du bâtiment (Batigest, EBP, Obat, Tolteck), comptabilité, paiement et '
                 u'signature électronique.</p>', deja='class="int-lead"')

    # carrousel : alt des portraits, et les « Bientôt » sortent
    for slug, alt in ALT_CREW.items():
        s = s.replace('<img src="perso/assistant-%s.webp" alt=""' % slug,
                      '<img src="perso/assistant-%s.webp" alt="%s"' % (slug, alt))
    s = re.sub(r'\s*<li class="crew-c" data-i="\d+">\s*<span class="crew-x">.*?</li>', '', s, flags=re.S)
    s = re.sub(r'<button type="button" role="tab" aria-label="Assistant (?:Chef de chantier|'
               r'Gestion de stock)" aria-selected="false"></button>', '', s)
    if 'class="crew-later"' not in s:
        a = s.find('<p class="crew-foot">')
        b = s.find('</p>', a) + 4
        assert a > 0
        s = s[:b] + (u'\n  <p class="crew-later"><b>Bientôt :</b> Assistant chef de chantier '
                     u'(plannings, comptes rendus) et Assistant gestion de stock (stocks, commandes).</p>') + s[b:]

    # l'agent responsable sous chaque étape du parcours
    if 'class="fx-agent"' not in s:
        for titre, agent in ETAPES:
            pat = re.compile(r'(<h3>%s</h3>\s*<p class="fx-win">.*?</p>)' % titre, re.S)
            s, n = pat.subn(lambda m: m.group(1) + u'\n          <p class="fx-agent">Agent : %s</p>'
                            % agent, s, count=1)
            assert n == 1, titre

    # FAQ : la question « agent IA » en tête, ouverte ; l'ancienne première se replie
    if u'C’est quoi, un agent IA pour artisan' not in s:
        acc = s.find('<div class="acc" id="acc">') + len('<div class="acc" id="acc">')
        tete = s[acc:acc + 400].replace('<div class="item open">', '<div class="item">', 1) \
                               .replace('aria-expanded="true"', 'aria-expanded="false"', 1)
        s = s[:acc] + u'\n' + FAQ_AGENT + tete + s[acc + 400:]
    s = remplace(s, u'''          Non, le ton est 100 % naturel. Talos répond avec courtoisie en suivant l'image de votre
          entreprise. Dès qu'un échange demande une visite terrain, l'IA vous passe la main.''',
                 u'''          Oui : le client est prévenu qu'un assistant IA lui répond pour vous, comme le prévoit
          le règlement européen sur l'IA. Le ton reste naturel et suit l'image de votre entreprise.
          Dès qu'un échange demande une visite terrain, l'IA vous passe la main.''')

    # libellés de maquette : lus par les moteurs, inutiles au visiteur
    s = re.sub(r'<b>Écran 0\d</b>', '', s)
    s = s.replace(u'<i>340 × 720 px · WebP</i>', '')
    for i, alt in enumerate(ALT_SHOTS):
        s = s.replace('<img id="shot%d" alt="">' % i, '<img id="shot%d" alt="%s">' % (i, alt))

    s = base64_vers_fichiers(s)
    # l'image du hero n'est plus dans le HTML : on la demande dès le <head>
    m = re.search(r'<div class="hero-diagonal[^"]*"><img src="([^"]+)"', s)
    if m and 'rel="preload" as="image"' not in s:
        s = s.replace('</head>', '<link rel="preload" as="image" href="%s" fetchpriority="high">\n</head>'
                      % m.group(1), 1)

    s = menu(s)
    ecrire('index.html', s)


# ═══════════════════════════════════════════════════════════════════════════
#  3 · LES AUTRES PAGES — la catégorie en tête du H1
# ═══════════════════════════════════════════════════════════════════════════
CATEGORIES = {
    'assistant-commercial.html': u'Agent IA devis et relances',
    'assistant-facturation.html': u'Agent IA facturation BTP',
    'assistant-tresorerie.html': u'Agent IA relance des impayés',
    'assistant-client.html': u'Agent IA accueil client et rendez-vous',
    'assistant-administratif.html': u'Agent IA tri des mails',
    'offres.html': u'5 agents IA pour artisans du BTP',
    'comment-ca-marche.html': u'Agents IA pour artisans du BTP',
}

CSS_CAT = u'''<style id="agents-ia-cat">
/* agents_ia.py — catégorie posée en tête du H1 */
h1 .h1-cat{display:block;margin:0 0 16px;font-family:ui-monospace,"SF Mono",Menlo,monospace;
  font-size:12.5px;line-height:1.4;letter-spacing:.14em;text-transform:uppercase;font-weight:600;
  font-style:normal;color:#E0631F;-webkit-text-fill-color:#E0631F;background:none}
html[data-theme="light"] h1 .h1-cat{color:#B4491A;-webkit-text-fill-color:#B4491A}
</style>
'''


def categorie(f, cat):
    s = lire(f)
    if 'class="h1-cat"' in s:
        return False
    s = remplace(s, '</head>', CSS_CAT + '</head>')
    s, n = re.subn(r'(<h1[^>]*>)', lambda m: m.group(1) + u'<span class="h1-cat">%s</span>' % cat, s, count=1)
    assert n == 1, f
    if f == 'offres.html':
        for slug, alt in ALT_CREW.items():
            s = s.replace('<img src="perso/assistant-%s.webp" alt=""' % slug,
                          '<img src="perso/assistant-%s.webp" alt="%s"' % (slug, alt))
    ecrire(f, s)
    return True


if __name__ == '__main__':
    accueil()
    for f, cat in CATEGORIES.items():
        print(u'%-28s %s' % (f, u'catégorie posée' if categorie(f, cat) else u'déjà à jour'))
    print(u'%-28s %s' % ('index.html', u'repositionné'))
    for f in PAGES_MENU[1:]:
        if not os.path.exists(WEB + f):
            continue
        avant = lire(f)
        apres = menu(avant)
        if apres != avant:
            ecrire(f, apres)
        print(u'%-28s %s' % (f, u'menu mis à jour' if apres != avant else u'déjà à jour'))
