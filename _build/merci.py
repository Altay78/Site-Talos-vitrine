# -*- coding: utf-8 -*-
"""La page de remerciement — là où Stripe renvoie après un paiement réussi.

Elle est générée seule, sans toucher aux autres pages :

    python3 _build/merci.py

Elle est en noindex : une page de confirmation n'a rien à faire dans
Google, et un client qui y arriverait par une recherche n'aurait rien
commandé du tout.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coquille import part, page

page('merci.html',
     u"Merci — votre commande Talos est enregistrée",
     u"Votre paiement est bien reçu. On vous appelle sous 24 h ouvrées pour "
     u"paramétrer vos assistants, et vos accès arrivent sous 72 h.",
     part('merci.css'), part('merci.html'), part('merci.js'),
     noindex=True)
