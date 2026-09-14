# -*- coding: utf-8 -*-
"""Régénère la seule page « assistant commercial ».

    python3 _build/ac.py

Elle ne passe pas par le gabarit commun des fiches assistant : ses huit blocs
vivent dans _build/parts/ac.{css,html,js}. pages.py produit exactement la même
page — ce script sert juste à la retoucher sans réécrire les quinze autres.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coquille import part, page
import nav_sync

FICHIER = 'assistant-commercial.html'
TITRE = u"Assistant commercial — Talos | Il ne laisse passer aucune opportunité"
DESC = (u"L'assistant commercial de Talos capte vos demandes même le soir, prépare vos "
        u"devis depuis un mail, un vocal ou une photo, les fait signer avec l'acompte, "
        u"puis relance jusqu'à la réponse du client.")
OG_T = u"Votre commercial qui ne laisse passer aucune opportunité"
OG_D = (u"Il capte vos demandes, prépare vos devis et relance vos clients jusqu'à la "
        u"signature. Même quand vous êtes sur un chantier.")


def construire():
    page(FICHIER, TITRE, DESC,
         part('ac.css'), part('ac.html'), part('ac.js'),
         og_title=OG_T, og_desc=OG_D)
    # la barre sort du gabarit sans aria-current ni feuille du menu déroulant
    print(u'%-28s %s' % nav_sync.sync(FICHIER))


if __name__ == '__main__':
    construire()
