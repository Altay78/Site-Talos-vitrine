# -*- coding: utf-8 -*-
"""Aligne la barre de navigation, le menu mobile et le pied de page
sur TOUTES les pages du site.

Trois anomalies existaient avant ce script :
  · chaque page retirait son propre lien de la barre (on ne pouvait plus
    savoir où l'on était, et la barre changeait de largeur d'une page
    à l'autre) ;
  · « Simulateurs » pointait sur index.html#simulateur alors que le
    simulateur a désormais sa page ;
  · Blog n'existait dans aucun menu, et espace-client.html n'avait
    pas de barre du tout.

La page courante garde son lien, marqué aria-current="page" : la DA
souligne déjà ce cas (.tnav-links a[aria-current="page"]).

    python3 _build/nav_sync.py
"""
import io, os, re

WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'

# (libellé, href) — l'ordre fait foi partout
LINKS = [
    (u'Offres',             'offres.html'),
    (u'Comment ça marche',  'comment-ca-marche.html'),
    (u'Tarifs',             'tarifs.html'),
    (u'Simulateur',         'simulateur.html'),
    (u'Pourquoi Talos',     'pourquoi-talos.html'),
    (u'Blog',               'blog.html'),
]

PAGES = ['index.html', 'offres.html', 'comment-ca-marche.html',
         'tarifs.html', 'pourquoi-talos.html', 'reserver.html',
         'espace-client.html', 'simulateur.html', 'blog.html',
         # les fiches assistants portent la même barre : oubliées ici,
         # elles gardaient un menu « Offres » d'une version en retard
         'assistant-commercial.html', 'assistant-tresorerie.html',
         'assistant-client.html', 'assistant-facturation.html',
         'assistant-administratif.html',
         # commander et merci manquaient : régénérées par offres.py et
         # merci.py, elles repartaient sans le menu « Offres » et sans
         # le pied de page réaligné. Deux pages du tunnel d'achat, donc
         # les dernières qu'on peut se permettre de laisser de côté.
         'commander.html', 'merci.html',
         # les pages juridiques ont la barre elles aussi : absentes d'ici,
         # elles gardaient les six liens à plat pendant que le reste du
         # site passait aux menus
         'cgu.html', 'cgv.html', 'mentions-legales.html',
         'confidentialite.html']

LOGO_SVG = ('<svg viewBox="253 302 472 550" width="23" height="27" aria-hidden="true">'
            '<mask id="navsync-marteau" maskUnits="userSpaceOnUse" x="253" y="302" width="472" height="550">'
            '<rect x="253" y="302" width="472" height="550" fill="#fff"/>'
            '<path d="M 310 302 L 725 302 L 688 406 L 558 406 L 502 640 L 372 640 L 400 406 L 362 406 C 338 409 316 430 300 457 C 291 472 265 468 258 447 C 250 420 255 389 263 363 C 276 324 288 302 310 302 Z" fill="#000" stroke="#000" stroke-width="32" stroke-linejoin="round"/></mask>'
            '<g mask="url(#navsync-marteau)"><path d="M 494 536 L 642 536 L 399 852 L 459 684 Z" fill="#C75C24"/></g>'
            '<path d="M 310 302 L 725 302 L 688 406 L 558 406 L 502 640 L 372 640 L 400 406 L 362 406 C 338 409 316 430 300 457 C 291 472 265 468 258 447 C 250 420 255 389 263 363 C 276 324 288 302 310 302 Z" fill="currentColor"/></svg>')


# Bascule de thème du menu mobile : sous 600px la pastille de la barre est
# masquée (plus la place), le réglage n'était atteignable nulle part.
# Pas de <div> ici : sync() découpe le menu jusqu'au premier </div>.
M_THEME = (
    u'<button type="button" class="theme-toggle m-theme" aria-label="Changer de thème">'
    u'<svg class="moon" width="17" height="17" viewBox="0 0 24 24" fill="none" '
    u'stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
    u'<path d="M 21 12.72C 20.53 18.61 14.36 22.93 7.99 20.12C 6.14 19.31 4.64 17.8 3.84 15.95C 1.11 9.59 5.4 3.48 11.27 3C 10.71 5.52 11.41 8.47 13.25 10.31C 15.08 12.14 18.27 13.33 21 12.72Z"/></svg>'
    u'<svg class="sun" width="17" height="17" viewBox="0 0 24 24" fill="none" '
    u'stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'
    u'<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M4.2 4.2l1.7 1.7'
    u'M18.1 18.1l1.7 1.7M2 12h2.4M19.6 12H22M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>'
    u'<span class="lbl-dark">Mode clair</span>'
    u'<span class="lbl-light">Mode sombre</span></button>')


# ── Le menu « Offres » ────────────────────────────────────────────────────
# Au survol (ou au focus clavier) il déploie l'équipe : un visage, un nom,
# une mission. Aucun <div> ici — sync() découpe la barre jusqu'au premier
# </div> rencontré, un conteneur de plus casserait le remplacement.
EQUIPE = [
    ('commercial',    u'Assistant commercial',    u'Devis, signature, relances',    'assistant-commercial.html'),
    ('tresorerie',    u'Assistante trésorerie',   u'Impayés et prévision',          'assistant-tresorerie.html'),
    ('client',        u'Assistante client',       u'Réponses et rendez-vous',       'assistant-client.html'),
    ('facturation',   u'Assistant facturation',   u'Factures conformes 2026',       'assistant-facturation.html'),
    ('administratif', u'Assistante administrative', u'Tri des mails et classement',   'assistant-administratif.html'),
    ('chantier',      u'Assistant chef de chantier', u'Planning, suivi, rapports',     None),
    ('stock',         u'Assistant gestion de stock', u'Stocks, commandes, alertes',    None),
]
# Ceux-là n'ont pas encore de page : on les montre quand même, marqués
# « Bientôt » et non cliquables — un lien vers une page absente serait pire
# que pas de lien du tout.
BIENTOT = {'chantier', 'stock'}

CHEV = (u'<svg class="tnav-chev" width="11" height="11" viewBox="0 0 24 24" fill="none" '
        u'stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
        u'stroke-linejoin="round" aria-hidden="true"><path d="M6 9.5l6 6 6-6"/></svg>')
FLECHE = (u'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          u'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          u'<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


# ── Deux menus de plus : « Tarifs » et « Pourquoi Talos » ────────────────
# Six libellés dans la barre, c'était deux de trop : « Simulateur » passe
# sous « Tarifs » (on simule un prix), « Blog » sous « Pourquoi Talos »
# (on y raconte la même chose, en plus long). Même carte que le menu
# « Offres », en une colonne : deux entrées ne méritent pas deux colonnes.
#
# Un regroupement ne doit jamais éloigner une page : les six liens restent
# à plat dans le menu du téléphone et dans le pied de page.
IC_TARIF = (u'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            u'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            u'<path d="M20.6 13.3l-7.3 7.3a1.9 1.9 0 0 1-2.7 0l-7.2-7.2a1.9 1.9 0 0 1-.5-1.3V4.6'
            u'a1.6 1.6 0 0 1 1.6-1.6h7.5c.5 0 1 .2 1.3.5l7.3 7.3a1.9 1.9 0 0 1 0 2.5z"/>'
            u'<circle cx="8.1" cy="8.1" r="1.3"/></svg>')
IC_SIM = (u'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          u'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          u'<rect x="4.5" y="2.5" width="15" height="19" rx="2.4"/><path d="M8.2 6.6h7.6"/>'
          u'<path d="M8.4 11.2h.02M12 11.2h.02M15.6 11.2h.02M8.4 14.6h.02M12 14.6h.02'
          u'M15.6 14.6h.02M8.4 18h.02M12 18h.02M15.6 18h.02"/></svg>')
IC_HIST = (u'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           u'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           u'<path d="M12 2.8c.6 3.1 2.4 4.6 4 6.2 1.6 1.6 2.6 3.3 2.6 5.5a6.6 6.6 0 0 1-13.2 0'
           u'c0-2.5 1.2-4 2.6-5.3"/><path d="M12 21a3.2 3.2 0 0 1-3.2-3.2c0-1.8 1.4-2.7 2.1-4'
           u'.4.8 1.7 2.1 2.6 2.1 4.4A3.2 3.2 0 0 1 12 21z"/></svg>')
IC_BLOG = (u'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           u'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           u'<path d="M19.5 4.8v13.4a2.3 2.3 0 0 1-2.3 2.3H5.6a2.1 2.1 0 0 1-2.1-2.1V6.9'
           u'a2.1 2.1 0 0 1 2.1-2.1h11.6a2.3 2.3 0 0 1 2.3 0z"/><path d="M7.4 8.7h8.2M7.4 12.3h8.2'
           u'M7.4 15.9h5"/></svg>')

MENUS = {
    'tarifs.html': [
        (IC_TARIF, u'Formules et tarifs', u'Solo, Pro, Business',       'tarifs.html'),
        (IC_SIM,   u'Simulateur',         u'Votre gain en 30 secondes', 'simulateur.html'),
    ],
    'pourquoi-talos.html': [
        (IC_HIST, u'Notre histoire', u'D\u2019o\xf9 vient Talos',        'pourquoi-talos.html'),
        (IC_BLOG, u'Blog',           u'Guides et cas de chantier',   'blog.html'),
    ],
}
# Les libell\xe9s qui restent dans la barre. Les autres vivent dans un menu.
BAR = ['offres.html', 'comment-ca-marche.html', 'tarifs.html', 'pourquoi-talos.html']


def drop_t(label, href, page):
    """Le libell\xe9 d'un menu. Quand la page ouverte est une de ses filles,
    il porte le trait : sinon, sur simulateur.html ou sur le blog, plus rien
    n'indique o\xf9 l'on se trouve."""
    filles = [h for _, _, _, h in MENUS.get(href, [])]
    ici = u' is-here' if (page in filles and page != href) else u''
    return (u'<a class="tnav-drop-t%s" href="%s"%s>%s%s</a>'
            % (ici, href, cur(href, page), label, CHEV))


def mini_html(label, href, page):
    items = []
    for ic, nom, mission, h in MENUS[href]:
        items.append(u'<a class="tnav-ag" href="%s"%s><span class="tnav-ic">%s</span>'
                     u'<b>%s</b><small>%s</small></a>' % (h, cur(h, page), ic, nom, mission))
    return (u'<span class="tnav-drop">%s<span class="tnav-pan is-mini">%s</span></span>'
            % (drop_t(label, href, page), u''.join(items)))


def offres_html(page):
    items = []
    for slug, nom, mission, href in EQUIPE:
        img = (u'<img src="perso/avatar-%s.webp" alt="" width="36" height="36" '
               u'loading="lazy" decoding="async">' % slug)
        if slug in BIENTOT:
            items.append(
                u'<span class="tnav-ag is-soon">%s'
                u'<b>%s <i class="tnav-soon">Bientôt</i></b><small>%s</small></span>'
                % (img, nom, mission))
        else:
            items.append(u'<a class="tnav-ag" href="%s">%s<b>%s</b><small>%s</small></a>'
                         % (href, img, nom, mission))
    return (u'<span class="tnav-drop">'
            u'<a class="tnav-drop-t" href="offres.html"%s>Offres%s</a>'
            u'<span class="tnav-pan">%s'
            u'<a class="tnav-pan-all" href="offres.html">Voir toutes les offres%s</a>'
            u'</span></span>' % (cur('offres.html', page), CHEV, u''.join(items), FLECHE))


# La feuille du menu est injectée dans chaque page : index.html embarque sa
# propre copie compilée du style, elle ne lit pas parts/shell.css.
JOINTS_CSS = u'''<style id="joints-css">
/* ── Les raccords entre sections ─────────────────────────────────────────
   Les sections partagent le même fond : le filet d'1 px qui les séparait
   coupait la page en tranches, et les lueurs de braise butaient dessus.
   Deux corrections, aucune couleur en dur :
     · le filet s'éteint vers les bords (border-image) au lieu de traverser
       l'écran d'un trait ;
     · chaque section démarre par un voile très léger qui se dissout sur
       220 px, ce qui relie visuellement le haut de la section à celle
       d'au-dessus.                                                        */
.int-band,.t-feat,.t-story,.t-how,.t-how2,.t-roi,.t-cat,.t-price,.t-faq{
  border-top:1px solid transparent;
  border-image:linear-gradient(90deg,transparent 0%,
      color-mix(in oklab,var(--border) 55%,transparent) 34%,
      color-mix(in oklab,var(--border) 55%,transparent) 66%,
      transparent 100%) 1;
  background-image:linear-gradient(180deg,
      color-mix(in oklab,var(--ink) 5%,transparent) 0,
      color-mix(in oklab,var(--ink) 2%,transparent) 90px,
      color-mix(in oklab,var(--ink) 0%,transparent) 300px)}
.int-band{border-bottom-color:transparent}
/* le carrousel n'a pas de filet : sa lueur fait déjà la jonction */
.t-crew{border-top:0}
/* et cette lueur ne doit plus s'arrêter net sur la couture */
.t-crew::before{-webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 96%);
                        mask-image:linear-gradient(180deg,#000 62%,transparent 96%)}
@media (prefers-reduced-motion:reduce){.t-crew::before{mask-image:none}}
</style>'''


PANEL_CSS = u"""<style id="tnav-drop-css">
.tnav-drop{position:relative;display:inline-flex}
.tnav-drop-t{display:inline-flex;align-items:center;gap:5px}
.tnav-chev{transition:transform .25s cubic-bezier(.16,1,.3,1)}
.tnav-drop:hover .tnav-chev,.tnav-drop:focus-within .tnav-chev{transform:rotate(180deg)}
.tnav-pan{position:absolute;top:100%;left:-18px;z-index:60;
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;
  width:min(640px,88vw);margin-top:16px;padding:10px;border-radius:20px;
  background:color-mix(in oklab,var(--surface-tint) 96%,transparent);
  border:1px solid var(--border);box-shadow:0 24px 60px rgba(0,0,0,.42);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  opacity:0;visibility:hidden;transform:translateY(-6px);
  transition:opacity .22s ease,transform .22s cubic-bezier(.16,1,.3,1),visibility .22s}
html[data-theme="light"] .tnav-pan{box-shadow:0 24px 60px rgba(40,25,16,.16)}
/* la zone de survol court jusqu'au panneau : sans ça le curseur le perd */
.tnav-drop::after{content:"";position:absolute;top:100%;left:0;right:0;height:18px}
.tnav-drop:hover .tnav-pan,.tnav-drop:focus-within .tnav-pan{
  opacity:1;visibility:visible;transform:translateY(0)}
.tnav-ag{display:grid;grid-template-columns:36px 1fr;column-gap:11px;
  align-items:center;padding:9px 11px;border-radius:14px;
  transition:background .2s ease}
.tnav-ag:hover{background:color-mix(in oklab,var(--ink) 7%,transparent)}
.tnav-ag::after{display:none}
.tnav-ag img{grid-row:1/3;width:36px;height:36px;border-radius:50%;object-fit:cover;
  background:color-mix(in oklab,var(--ink) 8%,transparent)}
.tnav-ag b{display:block;font-size:14px;font-weight:600;
  letter-spacing:-.2px;color:var(--ink)}
.tnav-ag small{font-size:12.5px;color:var(--ink-soft);letter-spacing:-.1px}
.tnav-soon{display:inline-block;vertical-align:1px;white-space:nowrap;
  font-style:normal;font-size:9.5px;font-weight:700;letter-spacing:.05em;
  text-transform:uppercase;padding:2px 6px;border-radius:100px;
  /* teintée par l'encre : assez sombre sur fond clair, assez claire sur
     fond sombre — 5:1 dans les deux thèmes, sans couleur en dur */
  color:color-mix(in oklab,var(--indigo) 72%,var(--ink));
  background:color-mix(in oklab,var(--indigo) 12%,transparent);
  border:1px solid color-mix(in oklab,var(--indigo) 55%,transparent)}
/* pas encore livré : on montre le personnage et la mission, mais rien à
   cliquer — donc ni curseur main, ni survol qui promettrait un lien */
.tnav-ag.is-soon{cursor:default}
.tnav-ag.is-soon:hover{background:none}
.tnav-pan-all{grid-column:1/-1;display:inline-flex;align-items:center;justify-content:center;
  gap:8px;margin-top:4px;padding:11px;border-radius:14px;
  background:color-mix(in oklab,var(--ink) 5%,transparent);
  font-size:13.5px;font-weight:600;color:var(--ink)}
.tnav-pan-all::after{display:none}
.tnav-pan-all:hover{background:color-mix(in oklab,var(--indigo) 14%,transparent);color:var(--indigo)}
/* \u2500\u2500 les deux menus courts \u2500\u2500
   M\xeame carte, m\xeame trame, m\xeame survol : une colonne au lieu de deux, et
   une pastille d'ic\xf4ne \xe0 la place du visage \u2014 « Tarifs » et « Blog » n'ont
   pas de portrait, et un rond vide serait pire qu'une ic\xf4ne. */
.tnav-pan.is-mini{grid-template-columns:minmax(0,1fr);width:min(322px,88vw);left:-16px}
.tnav-ic{grid-row:1/3;display:grid;place-items:center;width:36px;height:36px;
  border-radius:50%;color:var(--indigo);
  background:color-mix(in oklab,var(--indigo) 13%,transparent)}
.tnav-ag[aria-current="page"] b{color:var(--indigo)}
/* la page ouverte est une fille du menu : c'est le parent qui porte le trait */
.tnav-links .tnav-drop-t.is-here{color:var(--indigo)}
.tnav-links .tnav-drop-t.is-here::after{transform:scaleX(1)}
@media (max-width:1060px){.tnav-pan{display:none}}
@media (prefers-reduced-motion:reduce){.tnav-pan,.tnav-chev{transition:none}}
</style>"""

LEGAL_LINKS = (u'<a href="mentions-legales.html">Mentions légales</a>'
               u'<span class="dot">·</span>'
               u'<a href="cgu.html">CGU</a>'
               u'<span class="dot">·</span>'
               u'<a href="cgv.html">CGV</a>'
               u'<span class="dot">·</span>'
               u'<a href="confidentialite.html">Politique de confidentialité</a>')
RGPD_NOTE = (u'<p class="nform-rgpd">Votre adresse sert uniquement à vous envoyer nos '
             u'actualités. Désinscription en un clic — '
             u'<a href="confidentialite.html">politique de confidentialité</a>.</p>')
COPYRIGHT = (u'\u00a9 <span id="yr">2026</span> \u00b7 Talos \u2014 Altay Sakalli, '
             u'entrepreneur individuel \u00b7 SIREN 920 171 774')


def cur(href, page):
    return u' aria-current="page"' if href == page else u''


def links_html(page):
    """La barre : quatre libell\xe9s, dont trois ouvrent un menu."""
    out = []
    for t, h in LINKS:
        if h not in BAR:
            continue
        if h == 'offres.html':
            out.append(offres_html(page))
        elif h in MENUS:
            out.append(mini_html(t, h, page))
        else:
            out.append(u'<a href="%s"%s>%s</a>' % (h, cur(h, page), t))
    return u''.join(out)


def flat_links_html(page):
    """Le menu du t\xe9l\xe9phone : les six liens \xe0 plat. Les panneaux d\xe9roulants
    sont masqu\xe9s sous 1060 px \u2014 les y reprendre tels quels ferait dispara\xeetre
    « Simulateur » et « Blog » du t\xe9l\xe9phone."""
    return u''.join(u'<a href="%s"%s>%s</a>' % (h, cur(h, page), t) for t, h in LINKS)


def menu_html(page):
    esp = u' aria-current="page"' if page == 'espace-client.html' else u''
    res = u' aria-current="page"' if page == 'reserver.html' else u''
    return (flat_links_html(page)
            + u'<a class="m-esp" href="espace-client.html"%s>Espace client</a>' % esp
            + M_THEME
            + u'<a class="m-cta" href="reserver.html"%s>Réserver une démo</a>' % res)


def footer_html(page):
    items = [(u'Accueil', 'index.html#top' if page != 'index.html' else '#top')] + LINKS
    return u'\n'.join(u'          <li><a href="%s"%s>%s</a></li>'
                      % (h, cur(h, page), t) for t, h in items)


def nav_block(page):
    """Barre complète — pour les pages qui n'en avaient aucune."""
    return (
u'''<header class="tnav-wrap" id="tnav-wrap"><nav class="tnav" id="tnav" aria-label="Navigation principale"><a class="tnav-logo" href="index.html" aria-label="Talos — accueil">%s<span>Talos</span></a><div class="tnav-links">%s</div><div class="tnav-act"><button type="button" class="theme-toggle grid h-10 w-10 shrink-0 place-items-center rounded-lg" aria-label="Changer de thème"><svg class="moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M 21 12.72C 20.53 18.61 14.36 22.93 7.99 20.12C 6.14 19.31 4.64 17.8 3.84 15.95C 1.11 9.59 5.4 3.48 11.27 3C 10.71 5.52 11.41 8.47 13.25 10.31C 15.08 12.14 18.27 13.33 21 12.72Z"/></svg><svg class="sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M 18.36 5.64L 17.39 6.61M 6.61 17.39L 5.64 18.36M 18.36 18.36L 17.39 17.39M 6.61 6.61L 5.64 5.64"/><path d="M 12 7.8C 14.32 7.8 16.2 9.68 16.2 12C 16.2 14.32 14.32 16.2 12 16.2C 9.68 16.2 7.8 14.32 7.8 12C 7.8 9.68 9.68 7.8 12 7.8Z"/><path d="M 12 4.35V 4.37M 12 19.63V 19.65M 19.66 12H 19.63M 4.37 12H 4.34"/></svg></button><a class="tnav-esp" href="espace-client.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M 11.98 15.35C 8.12 15.35 4.81 15.93 4.81 18.27C 4.81 20.61 8.1 21.22 11.98 21.22C 15.85 21.22 19.15 20.63 19.15 18.29C 19.15 15.95 15.87 15.35 11.98 15.35Z"/><path d="M 11.98 12.01C 14.52 12.01 16.58 9.95 16.58 7.41C 16.58 4.87 14.52 2.81 11.98 2.81C 9.45 2.81 7.39 4.87 7.39 7.41C 7.38 9.94 9.42 12 11.95 12.01L 11.98 12.01Z"/></svg>Espace client</a><a class="tnav-cta" href="reserver.html">Réserver une démo</a><button class="tnav-burger" id="tnav-burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="tnav-menu"><i></i><i></i><i></i></button></div></nav><div class="tnav-menu" id="tnav-menu">%s</div></header>'''
        % (LOGO_SVG, links_html(page), menu_html(page)))


def sync(page):
    path = WEB + page
    s = io.open(path, encoding='utf-8').read()
    before = s
    notes = []

    # 1 · liens de la barre
    s, n = re.subn(r'(<div class="tnav-links">).*?(</div>)',
                   lambda m: m.group(1) + links_html(page) + m.group(2), s, flags=re.S)
    if n:
        notes.append('barre')

    # 2 · menu mobile
    s, n = re.subn(r'(<div class="tnav-menu" id="tnav-menu">).*?(</div>)',
                   lambda m: m.group(1) + menu_html(page) + m.group(2), s, flags=re.S)
    if n:
        notes.append('menu')

    # 3 · colonne « Navigation » du pied de page
    s, n = re.subn(r'(<h2>Navigation</h2>\s*<ul>).*?(</ul>)',
                   lambda m: m.group(1) + '\n' + footer_html(page) + '\n        ' + m.group(2),
                   s, flags=re.S)
    if n:
        notes.append('pied')

    # 4 · les liens juridiques du pied de page — obligation légale, ils
    #     doivent figurer sur chaque page, pas seulement sur l'accueil
    s, n = re.subn(r'(<div class="legal">).*?(</div>)',
                   lambda m: m.group(1) + LEGAL_LINKS + m.group(2), s, flags=re.S)
    if n:
        notes.append('juridique')
    s = re.sub(r'© <span id="yr">2026</span>[^<]*', COPYRIGHT, s)

    # la finalité du formulaire d'inscription doit être annoncée sur place
    # On vise le formulaire du pied de page (class="nform"), pas le premier
    # </form> de la page : sur l'accueil, c'est celui de la capture d'e-mail.
    if 'nform-rgpd' not in s:
        i = s.find('class="nform"')
        j = s.find('</form>', i) if i >= 0 else -1
        if j >= 0:
            s = s[:j + 7] + '\n      ' + RGPD_NOTE + s[j + 7:]

    # 5 · la feuille du menu déroulant, une fois par page
    #
    #  ⚠️  Ces deux blocs sont REMPLACÉS, pas complétés. Tout ce qu'on y
    #  écrit à la main disparaît au prochain passage. C'est arrivé le
    #  19/09 : le CSS des deux appareils du hero (.hd-mac, .hd-iph) avait
    #  été ajouté dans tnav-drop-css ; les maquettes se sont dépliées sur
    #  toute la page d'accueil, et rien ne l'a signalé.
    #  Le garde-fou ci-dessous relit l'ancien bloc et refuse d'effacer une
    #  règle qui n'est pas dans le nouveau.
    if '<div class="tnav-links">' in before:
        for bloc, neuf in (('tnav-drop-css', PANEL_CSS), ('joints-css', JOINTS_CSS)):
            m = re.search(r'<style id="%s">([\s\S]*?)</style>' % bloc, s)
            if not m:
                continue
            connus = set(re.findall(r'\.([a-zA-Z][\w-]+)', neuf))
            trouves = set(re.findall(r'\.([a-zA-Z][\w-]+)', m.group(1)))
            etrangers = sorted(trouves - connus)
            if etrangers:
                raise SystemExit(
                    "nav_sync : %s contient des règles qui ne sont pas à lui —\n"
                    "           %s\n"
                    "           Les réécrire les effacerait. Déplacez-les dans\n"
                    "           leur propre <style>, puis relancez."
                    % (page, ', '.join('.' + e for e in etrangers[:8])))
        s = re.sub(r'<style id="tnav-drop-css">.*?</style>', '', s, flags=re.S)
        s = re.sub(r'<style id="joints-css">.*?</style>', '', s, flags=re.S)
        s = s.replace('</head>', JOINTS_CSS + PANEL_CSS + '</head>', 1)
        notes.append('menu offres')

    if not notes:
        return page, 'AUCUN REPÈRE — à traiter à la main'
    if s == before:
        return page, 'déjà à jour (%s)' % '+'.join(notes)
    io.open(path, 'w', encoding='utf-8').write(s)
    return page, 'mis à jour : %s' % '+'.join(notes)


if __name__ == '__main__':
    for p in PAGES:
        name, msg = sync(p)
        print(u'%-24s %s' % (name, msg))
