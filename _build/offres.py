# -*- coding: utf-8 -*-
"""Régénère les fiches assistant refaites — toutes, ou une seule.

    python3 _build/offres.py                 toutes les fiches v2
    python3 _build/offres.py commercial      celle-là seulement

pages.py produit exactement les mêmes fichiers ; ce script existe pour
retoucher une fiche sans réécrire les quinze autres pages du site.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coquille import part, page
import fiche, fiches
import nav_sync

CSS = part('fiche.css')
JS = part('fiche.js')


def hub(resync=True):
    """La page Offres — l'équipe en carrousel, et les trois compteurs."""
    import assistants
    page('offres.html',
         u"Offres — Talos | Votre équipe de cinq assistants IA",
         u"Cinq assistants spécialisés qui gèrent devis, facturation, trésorerie, relation "
         u"client et administratif pendant que vous êtes sur le chantier. Mise en place incluse.",
         part('asst.css') + u'\n' + part('offres.css'), assistants.hub(), u'',
         og_title=u"Votre équipe Talos — cinq assistants qui travaillent pour vous",
         og_desc=u"Devis, facturation, trésorerie, relation client, administratif : chaque "
                 u"assistant a ses missions. Vous prenez ceux dont vous avez besoin.")
    if resync:
        print(u'%-28s %s' % nav_sync.sync('offres.html'))


def construire(f, resync=True):
    nom = 'assistant-%s.html' % f['slug']
    page(nom, f['titre'], f['desc'], CSS, fiche.corps(f), JS,
         og_title=f['og_titre'], og_desc=f['og_desc'])
    if resync:
        # la barre sort du gabarit sans aria-current ni feuille du menu déroulant
        print(u'%-28s %s' % nav_sync.sync(nom))


if __name__ == '__main__':
    voulus = sys.argv[1:]
    for _f in fiches.FICHES:
        if voulus and _f['slug'] not in voulus:
            continue
        construire(_f)
    if not voulus or 'offres' in voulus:
        hub()
