# -*- coding: utf-8 -*-
"""Les contenus des fiches assistant — un dictionnaire par collègue.

La mise en forme est dans fiche.py et ne change pas d'un assistant à l'autre.
Ici on écrit ce qui se lit : la promesse, les trois missions, le scénario
minute par minute, les quatre cartes de fonctionnalités, le duo, l'avant /
après et l'appel final.

L'assistant commercial sert de modèle d'écriture : phrases courtes, sujet
« vous », un chiffre plutôt qu'un adjectif, et jamais de promesse que le
produit ne tient pas.

Clés qui demandent une explication :
  pronom / e   « il » ou « elle », et le « e » de « Je veux mon assistant(e) »
  missions     (numéro, titre, texte, icône, capture, alt) × 3
  etapes       (jour court, heure, horodatage lisible, icône, titre, corps) × 7
  cartes       role = l'étiquette du haut, lab = le sur-titre, acc/acc2 = la
               ligne d'accroche en deux tons, puces = (icône, texte)
"""

from fiche import chips, prix, cite, dire, gain


# ═══════════════════════════════════════════════════════════════════════════
#  ASSISTANT COMMERCIAL
# ═══════════════════════════════════════════════════════════════════════════

COMMERCIAL = dict(
 slug='commercial', pw=530, ph=1400, pronom=u'il', e=u'',
 alt=u"L'assistant commercial de Talos",
 role=u"Assistant commercial", role_bas=u"l'assistant commercial",
 titre=u"Assistant commercial — Talos | Il ne laisse passer aucune opportunité",
 desc=u"L'assistant commercial de Talos capte vos demandes même le soir, prépare vos devis "
      u"depuis un mail, un vocal ou une photo, les fait signer avec l'acompte, puis relance "
      u"jusqu'à la réponse du client.",
 og_titre=u"Votre commercial qui ne laisse passer aucune opportunité",
 og_desc=u"Il capte vos demandes, prépare vos devis et relance vos clients jusqu'à la "
         u"signature. Même quand vous êtes sur un chantier.",

 h1=u"Votre commercial qui ne laisse passer <em>aucune opportunité</em>.",
 lede=u"Il capte vos demandes, prépare vos devis et relance vos clients jusqu'à la signature. "
      u"Même quand vous êtes sur un chantier ou que votre journée est terminée.",
 atouts=[('chat', u"Capte les demandes jour et nuit"),
         ('doc', u"Rédige vos devis en minutes"),
         ('grille', u"Chiffre sur votre grille tarifaire"),
         ('edit', u"Fait signer et encaisse l'acompte"),
         ('loop', u"Relance à J+3, J+7 et J+14")],

 b2_h2=u"Transformez chaque demande en <em>opportunité</em>.",
 missions=[
  (u"01 — Capter", u"Aucune demande ne reste sans réponse",
   u"Votre assistant répond aux demandes, même le soir et le week-end, et récupère les "
   u"informations nécessaires pour comprendre le projet.",
   'chat', 'ec-reponse_247',
   u"Écran des réponses envoyées automatiquement, de nuit comme le week-end"),
  (u"02 — Préparer les devis", u"Vos devis commencent à se préparer tout seuls",
   u"À partir d'un email, d'une photo ou d'une note vocale, Talos transforme la demande en "
   u"devis selon votre manière de chiffrer.",
   'doc', 'ec-devis_auto',
   u"Écran des devis préparés par Talos, prêts à relire"),
  (u"03 — Convertir", u"Vos devis sont suivis jusqu'à la réponse",
   u"Un devis envoyé n'est pas un devis oublié. Talos suit automatiquement chaque dossier et "
   u"adapte les relances à la réaction du client.",
   'loop', 'ec-relance_devis',
   u"Écran du suivi des devis et des relances programmées"),
 ],

 b3_h2=u"La demande du vendredi soir devient un <em>devis signé</em>.",
 b3_sub=u"Un chantier de salle de bain à Paris, de la première question du client jusqu'à "
        u"l'acompte encaissé. Vous n'intervenez qu'une fois : pour valider.",
 b3_note_t=u"Votre part du travail : deux minutes.",
 b3_note_p=u"Relire le devis préparé pendant la nuit, puis appuyer sur envoyer. Le reste est "
           u"déjà fait quand vous ouvrez Talos le matin.",
 etapes=[
  (u"Ven.", u"19:42", u"Vendredi · 19:42", 'msg', u"Nouveau message",
   cite(u"Bonjour, je voudrais refaire ma salle de bain…")
   + dire(u"Vous êtes encore sur un chantier. Personne ne décroche — et pourtant la demande "
          u"est déjà prise en charge.")),
  (u"Ven.", u"19:43", u"Vendredi · 19:43", 'chat', u"Talos répond",
   cite(u"Bonsoir, merci pour votre demande. Pour vous orienter au mieux, pouvez-vous me "
        u"préciser la surface, l'état actuel de la pièce et la date de démarrage souhaitée ?")
   + dire(u"Une minute après. Ton posé, questions utiles, votre signature en bas du message.")),
  (u"Ven.", u"19:45", u"Vendredi · 19:45", 'filter', u"Demande qualifiée",
   chips(u"Salle de bain", u"12 m²", u"Paris", u"Rénovation complète",
         u"Démarrage souhaité : octobre")
   + dire(u"La fiche est complète avant même que vous rentriez.")),
  (u"Sam.", u"09:12", u"Samedi · 09:12", 'edit', u"Devis préparé",
   prix((u"Éco", u"8 450 €", False), (u"Standard", u"10 900 €", True),
        (u"Premium", u"13 200 €", False))
   + dire(u"Chiffré sur votre grille tarifaire, avec vos prestations et vos marges. Vous "
          u"relisez, vous corrigez si besoin.")),
  (u"Sam.", u"09:15", u"Samedi · 09:15", 'send', u"Devis envoyé",
   chips(u"Signature électronique", u"Acompte 30 %", u"Valable 30 jours")
   + dire(u"Le client signe depuis son téléphone, sans imprimer ni scanner. L'acompte est "
          u"demandé au moment de la signature.")),
  (u"Mar.", u"10:00", u"Mardi · 10:00", 'loop', u"Relance automatique",
   cite(u"Bonjour M. Dupont, avez-vous eu le temps de consulter votre devis ? Je reste "
        u"disponible si vous souhaitez en discuter.")
   + dire(u"Celle que personne ne pense à faire. Elle s'arrête net dès que le client répond.")),
  (u"Mar.", u"14:32", u"Mardi · 14:32", 'shield', u"Devis signé",
   gain(u"3 270 €", u"d'acompte encaissé — le chantier démarre avec de la trésorerie.")
   + dire(u"Quatre jours entre la demande et la signature. Zéro appel passé le soir.")),
 ],

 b4_h2=u"Quatre étapes, <em>zéro oubli</em>.",
 b4_sub=u"De la demande reçue à 22 h jusqu'à l'acompte encaissé, voici exactement ce que votre "
        u"assistant commercial fait à votre place.",
 cartes=[
  dict(role=u"Réception", lab=u"Capter la demande",
       titre=u"Rien ne se perd, même à 22 h",
       acc=u"Réponse immédiate", acc2=u"sur tous vos canaux",
       puces=[('clock', u"Répond le soir et le week-end"),
              ('chat', u"Pose les questions manquantes"),
              ('pin', u"Chantier, adresse, délai, budget"),
              ('msg', u"Mail, formulaire et WhatsApp réunis"),
              ('bell', u"Vous alerte sur les demandes chaudes")],
       cta=u"Voir le scénario complet", href=u"#scenario"),
  dict(role=u"Chiffrage", lab=u"Préparer le devis",
       titre=u"Le devis s'écrit pendant que vous roulez",
       acc=u"Cinq façons de le lancer", acc2=u"une seule grille tarifaire",
       puces=[('msg', u"Depuis un e-mail client"),
              ('voice', u"Depuis une note vocale"),
              ('cam', u"Depuis une photo ou un plan"),
              ('doc', u"Depuis le formulaire du site"),
              ('grille', u"Sur votre grille et vos marges")],
       cta=u"Le voir chiffrer mes devis", href=u"reserver.html"),
  dict(role=u"Signature", lab=u"Envoyer &amp; faire signer",
       titre=u"Il repart signé, avec l'acompte",
       acc=u"Signature en ligne", acc2=u"acompte encaissé à la commande",
       puces=[('grid', u"Variantes Éco, Standard, Premium"),
              ('edit', u"Signature depuis son téléphone"),
              ('bag', u"Acompte de 30 % à la signature"),
              ('cal', u"Date de validité sur chaque devis"),
              ('doc', u"Conditions de paiement posées")],
       cta=u"Faire signer mes devis en ligne", href=u"reserver.html"),
  dict(role=u"Relance", lab=u"Relancer &amp; suivre",
       titre=u"Il relance à votre place, et sait s'arrêter",
       acc=u"J+3, J+7, J+14", acc2=u"puis plus rien",
       puces=[('loop', u"Relance à J+3, courte et polie"),
              ('chat', u"Relance à J+7, appel proposé"),
              ('cal', u"Relance à J+14, validité rappelée"),
              ('shield', u"S'arrête dès qu'il répond"),
              ('send', u"S'arrête à la signature"),
              ('search', u"Repère les devis relus"),
              ('star', u"Les dossiers chauds en haut de pile")],
       cta=u"Ne plus relancer moi-même", href=u"reserver.html"),
 ],

 b5_h2=u"Vous gardez vos outils, <em>il travaille avec</em>.",
 b5_sub=u"Pas de migration, pas de logiciel à apprendre, pas de données à ressaisir. Il se "
        u"branche sur votre messagerie, votre agenda et vos outils actuels.",

 b6_h2=u"Combinez-le avec <em>l'Assistant Facturation</em> pour plus de résultats.",
 duo_slug='facturation', duo_role=u"Assistant facturation",
 duo_titre=u"Du devis signé à la facture.",
 duo_texte=u"Dès que votre client signe, votre Assistant Facturation prend le relais : "
           u"acompte, facture, situations, archivage et export comptable. Vous ne ressaisissez "
           u"rien, et vous ne courez plus après une pièce manquante.",

 b7_h2=u"Avant, et <em>avec Talos</em>.",
 avant_apres=[
  (u"Vous rappelez les demandes le soir", u"Talos répond immédiatement"),
  (u"Vous reprenez les infos à la main", u"Talos les qualifie"),
  (u"Vous faites vos devis le soir", u"Talos les prépare"),
  (u"Vous devez penser aux relances", u"Talos les effectue"),
  (u"Vous cherchez où en est chaque client", u"Talos vous le signale"),
  (u"Vous perdez parfois des demandes", u"Chaque demande est suivie"),
 ],

 b8_h2=u"Vous avez besoin d'un <em>commercial en plus</em> ?",
 b8_sub=u"Celui-ci travaille les soirs, les week-ends et les jours de chantier. Il commence "
        u"une semaine après votre appel, sur vos vrais devis.",
 b8_reassure=[u"Mise en place personnalisée", u"Sans engagement",
              u"Données hébergées en France"],
)


# ═══════════════════════════════════════════════════════════════════════════
#  ASSISTANTE TRÉSORERIE
# ═══════════════════════════════════════════════════════════════════════════

TRESORERIE = dict(
 slug='tresorerie', pw=652, ph=1400, pronom=u'elle', e=u'e',
 alt=u"L'assistante trésorerie de Talos",
 role=u"Assistante trésorerie", role_bas=u"l'assistante trésorerie",
 titre=u"Assistante trésorerie — Talos | Elle fait rentrer l'argent sans que vous insistiez",
 desc=u"L'assistante trésorerie de Talos repère vos factures en retard, relance à J+7, J+15 "
      u"et J+30, prépare les pénalités et la mise en demeure, et vous dit chaque lundi ce qui "
      u"va rentrer.",
 og_titre=u"Votre trésorerie qui ne laisse filer aucun impayé",
 og_desc=u"Elle repère les retards, relance à votre place avec le bon ton au bon moment, et "
         u"vous dit ce qui rentre cette semaine.",

 h1=u"Votre trésorerie qui ne laisse filer <em>aucun impayé</em>.",
 lede=u"Elle repère les factures en retard, relance vos clients avec le bon ton au bon moment, "
      u"et vous dit chaque lundi ce qui va rentrer. Vous n'avez plus à jouer le mauvais rôle.",
 atouts=[('clock', u"Repère les factures en retard"),
         ('loop', u"Relance à J+7, J+15 et J+30"),
         ('grille', u"Calcule les pénalités qui vous sont dues"),
         ('doc', u"Prépare la mise en demeure"),
         ('chart', u"Prévoit vos encaissements")],

 b2_h2=u"Transformez chaque retard en <em>encaissement</em>.",
 missions=[
  (u"01 — Repérer", u"Vous savez qui doit, et depuis quand",
   u"Dès l'échéance dépassée, la facture bascule dans les impayés avec son ancienneté et le "
   u"montant en jeu. Plus besoin d'éplucher vos relevés le dimanche.",
   'clock', 'ec-relance_impayes',
   u"Écran des factures en retard, classées par ancienneté"),
  (u"02 — Relancer", u"Le bon ton, au bon moment, à votre place",
   u"J+7 un rappel poli, J+15 plus direct, J+30 la dernière chance avant mise en demeure. "
   u"Chaque niveau est déjà écrit : vous relisez et vous validez.",
   'loop', 'ec-facturation_facturx',
   u"Écran de la relance graduée préparée par Talos"),
  (u"03 — Encaisser", u"Vous voyez le trou arriver avant d'y tomber",
   u"Pénalités calculées, échéancier proposé, projection des encaissements semaine par "
   u"semaine, et une alerte le lundi matin si le solde passe sous votre seuil.",
   'chart', 'ec-dashboard_treso',
   u"Écran de la prévision de trésorerie et des encaissements à venir"),
 ],

 b3_h2=u"La facture oubliée de février devient un <em>virement encaissé</em>.",
 b3_sub=u"Une facture de 6 200 € chez un client qui traîne, de l'échéance dépassée jusqu'au "
        u"solde. Vous n'intervenez qu'une fois : pour valider le ton.",
 b3_note_t=u"Vous ne réclamez plus rien vous-même.",
 b3_note_p=u"Chaque relance est écrite à l'avance et attend votre feu vert. Un client que vous "
           u"voulez ménager, vous le mettez en pause — il reste dans le suivi.",
 etapes=[
  (u"", u"Échéance", u"Le jour de l'échéance", 'clock', u"Échéance dépassée",
   chips(u"F-2026-084", u"6 200 €", u"SCI Horizon", u"8 jours de retard")
   + dire(u"Vous ne l'aviez pas vu passer. Elle, si — dès le lendemain de la date limite.")),
  (u"", u"J+7", u"Sept jours après l'échéance", 'msg', u"Premier rappel",
   cite(u"Bonjour, sauf erreur de notre part, la facture F-2026-084 du 12 février reste "
        u"impayée à ce jour. Pouvez-vous nous confirmer sa mise en règlement ?")
   + dire(u"Courtois, court, sans reproche. Sept retards sur dix ne sont qu'un oubli — "
          u"celui-là suffit souvent.")),
  (u"", u"J+11", u"Onze jours après l'échéance", 'search', u"Le client hésite",
   chips(u"Mail ouvert 3 fois", u"Aucune réponse", u"6 200 € en jeu")
   + dire(u"Un rappel relu trois fois sans réponse, c'est un client qui repousse. Le dossier "
          u"remonte en haut de votre pile.")),
  (u"", u"J+15", u"Quinze jours après l'échéance", 'bell', u"Le ton change",
   cite(u"…à défaut de règlement sous huit jours, des pénalités de retard au taux légal ainsi "
        u"que l'indemnité forfaitaire de 40 € prévue par l'article L441-10 seront appliquées.")
   + dire(u"Annoncer les pénalités change le comportement du payeur bien avant d'avoir à les "
          u"appliquer.")),
  (u"", u"J+18", u"Dix-huit jours après l'échéance", 'chat', u"Le client rappelle",
   prix((u"1er versement", u"2 067 €", True), (u"2e versement", u"2 067 €", False),
        (u"3e versement", u"2 066 €", False))
   + dire(u"Il ne peut pas tout payer d'un coup. Plutôt qu'un bras de fer, un échéancier en "
          u"trois fois — préparé et envoyé dans la foulée.")),
  (u"", u"J+21", u"Vingt et un jours après l'échéance", 'bag', u"Premier versement reçu",
   gain(u"2 067 €", u"rapprochés automatiquement avec votre compte — la relance se met en pause.")
   + dire(u"Elle ne relancera pas sur une facture déjà en cours de règlement.")),
  (u"", u"Soldé", u"Deux mois après l'échéance", 'shield', u"Facture soldée",
   gain(u"6 342 €", u"encaissés, dont 142 € de pénalités de retard que vous n'auriez pas réclamées.")
   + dire(u"Zéro appel gênant, zéro relation client abîmée, et un client qui revient.")),
 ],

 b4_h2=u"Trois leviers, <em>zéro bras de fer</em>.",
 b4_sub=u"De l'échéance dépassée jusqu'au virement reçu, voici exactement ce que votre "
        u"assistante trésorerie fait à votre place.",
 cartes=[
  dict(role=u"Détection", lab=u"Repérer les retards",
       titre=u"Vous savez qui doit, et depuis quand",
       acc=u"Dès le lendemain de l'échéance", acc2=u"sans éplucher vos relevés",
       puces=[('clock', u"Dès l'échéance dépassée"),
              ('chart', u"Classé par ancienneté et montant"),
              ('lock', u"Rapprochement bancaire, lecture seule"),
              ('shield', u"S'arrête dès le virement reçu"),
              ('user', u"Historique par client")],
       cta=u"Voir le scénario complet", href=u"#scenario"),
  dict(role=u"Relance", lab=u"Relancer sans s'énerver",
       titre=u"Le bon ton, au bon moment",
       acc=u"J+7, J+15, J+30", acc2=u"trois niveaux, un seul clic",
       puces=[('msg', u"J+7, courtoise"),
              ('loop', u"J+15, directe, facture jointe"),
              ('bell', u"J+30, dernier rappel"),
              ('filter', u"Seuil en dessous duquel on n'insiste pas"),
              ('user', u"Mise en pause d'un client")],
       cta=u"Ne plus relancer moi-même", href=u"reserver.html"),
  dict(role=u"Recouvrement", lab=u"Sortir le vocabulaire légal",
       titre=u"Les mots que vous n'osez pas écrire",
       acc=u"Pénalités et mise en demeure", acc2=u"aux bonnes mentions",
       puces=[('grille', u"Pénalités au taux légal"),
              ('bag', u"Indemnité de 40 € par facture"),
              ('doc', u"Mise en demeure prête à envoyer"),
              ('cal', u"Échéancier en trois ou quatre fois"),
              ('info', u"Pénalités annoncées dès le 2ᵉ rappel")],
       cta=u"Réclamer ce qui m'est dû", href=u"reserver.html"),
  dict(role=u"Prévision", lab=u"Voir venir",
       titre=u"Vous savez ce qui rentre, et quand",
       acc=u"Alerte tous les lundis à 8 h", acc2=u"solde prévu, retards, priorités",
       puces=[('chart', u"Encaissements semaine par semaine"),
              ('bell', u"Alerte hebdo par e-mail et SMS"),
              ('clock', u"Signal sous votre seuil"),
              ('star', u"Les priorités, montant en tête")],
       cta=u"Voir ma trésorerie à trois mois", href=u"reserver.html"),
 ],

 b5_h2=u"Vous gardez votre banque et vos outils, <em>elle travaille avec</em>.",
 b5_sub=u"Votre compte professionnel est consulté en lecture seule, uniquement pour rapprocher "
        u"les paiements. Elle ne peut initier aucun virement.",

 b6_h2=u"Combinez-la avec <em>l'Assistant Facturation</em> pour plus de résultats.",
 duo_slug='facturation', duo_role=u"Assistant facturation",
 duo_titre=u"Une facture juste se relance mieux.",
 duo_texte=u"La moitié des impayés viennent d'une facture partie en retard, mal numérotée ou "
           u"sans les bonnes mentions. L'Assistant Facturation l'émet propre et à l'heure ; "
           u"l'Assistante Trésorerie n'a plus qu'à la faire payer.",

 b7_h2=u"Avant, et <em>avec Talos</em>.",
 avant_apres=[
  (u"Vous découvrez les retards trop tard", u"Talos les repère dès l'échéance"),
  (u"Vous n'osez pas relancer vos clients", u"Talos écrit la relance, vous validez"),
  (u"Vous relancez tous sur le même ton", u"Le ton monte d'un cran à chaque niveau"),
  (u"Vous ne réclamez jamais les pénalités", u"Elles sont calculées et annoncées"),
  (u"Vous ignorez ce qui rentre ce mois-ci", u"La projection arrive chaque lundi"),
  (u"Un impayé finit par passer à la perte", u"Chaque facture est suivie jusqu'au solde"),
 ],

 b8_h2=u"Vous avez besoin d'une <em>trésorerie tenue</em> ?",
 b8_sub=u"Elle réclame à votre place, avec les mots justes et au bon moment. Vous gardez la "
        u"relation client, elle prend le mauvais rôle.",
 b8_reassure=[u"Mise en place personnalisée", u"Aucun virement possible",
              u"Données hébergées en France"],
)


# ═══════════════════════════════════════════════════════════════════════════
#  ASSISTANTE CLIENT
# ═══════════════════════════════════════════════════════════════════════════

CLIENT = dict(
 slug='client', pw=411, ph=1400, pronom=u'elle', e=u'e',
 alt=u"L'assistante client de Talos",
 role=u"Assistante client", role_bas=u"l'assistante client",
 titre=u"Assistante client — Talos | Aucun appel manqué ne se perd",
 desc=u"L'assistante client de Talos répond à vos clients 24 h/24, qualifie leurs demandes, "
      u"propose des créneaux compatibles avec vos trajets et envoie les confirmations et les "
      u"rappels.",
 og_titre=u"Votre standard qui ne laisse aucun appel sans réponse",
 og_desc=u"Elle répond jour et nuit, qualifie la demande, cale le rendez-vous dans votre "
         u"agenda et rappelle le client avant l'heure.",

 h1=u"Votre standard qui ne laisse <em>aucun appel sans réponse</em>.",
 lede=u"Elle répond à vos clients jour et nuit, qualifie leur demande, cale le rendez-vous "
      u"dans votre agenda et le leur rappelle. Vous ne rappelez plus personne le soir.",
 atouts=[('chat', u"Répond jour et nuit, week-end compris"),
         ('pin', u"Qualifie la demande et vérifie votre zone"),
         ('cal', u"Propose des créneaux qui tiennent"),
         ('grid', u"Pose le rendez-vous dans votre agenda"),
         ('bell', u"Rappelle la veille et deux heures avant")],

 b2_h2=u"Transformez chaque appel manqué en <em>rendez-vous</em>.",
 missions=[
  (u"01 — Répondre", u"Un client sans réponse est un client perdu",
   u"Le soir, le week-end, pendant les congés : elle répond dans la minute depuis votre base "
   u"de connaissances — vos prestations, votre zone, vos délais.",
   'chat', 'ec-reponse_247',
   u"Écran des réponses envoyées automatiquement, de nuit comme le week-end"),
  (u"02 — Qualifier", u"La bonne demande, avec les bonnes infos",
   u"Nature des travaux, adresse, urgence, budget évoqué : elle pose les questions qui manquent "
   u"et vérifie que le chantier est bien dans votre zone d'intervention.",
   'pin', 'ec-rdv_auto',
   u"Écran de la demande qualifiée et du rendez-vous proposé"),
  (u"03 — Caler", u"Votre agenda se remplit sans vous",
   u"Elle propose des créneaux compatibles avec vos déplacements, pose l'événement dans votre "
   u"agenda, puis rappelle le client la veille et deux heures avant.",
   'cal', 'ec-rappels_rdv',
   u"Écran des rappels de rendez-vous envoyés aux clients"),
 ],

 b3_h2=u"L'appel manqué du samedi soir devient un <em>rendez-vous calé</em>.",
 b3_sub=u"Un dépannage de chaudière au Perreux, du premier message jusqu'au client qui vous "
        u"attend sur le pas de la porte. Vous n'intervenez pas une seule fois.",
 b3_note_t=u"Votre part du travail : rien.",
 b3_note_p=u"Le rendez-vous est dans votre agenda avec l'adresse, le motif et la fiche client. "
           u"Vous le découvrez le lundi matin, déjà confirmé.",
 etapes=[
  (u"Sam.", u"20:14", u"Samedi · 20:14", 'msg', u"Message reçu",
   cite(u"Bonsoir, ma chaudière ne chauffe plus depuis ce matin. Vous intervenez sur Le "
        u"Perreux ?")
   + dire(u"Vous êtes à table. Le téléphone vibre, personne ne décroche — et pourtant.")),
  (u"Sam.", u"20:15", u"Samedi · 20:15", 'chat', u"Talos répond",
   cite(u"Bonsoir, oui, Le Perreux fait partie de notre secteur. Pour vous proposer le bon "
        u"créneau : s'agit-il d'une panne totale, et connaissez-vous la marque de la chaudière ?")
   + dire(u"Une minute. Le client sait qu'il est pris en charge, et il arrête de chercher un "
          u"autre artisan.")),
  (u"Sam.", u"20:18", u"Samedi · 20:18", 'pin', u"Demande qualifiée",
   chips(u"Chaudière gaz", u"Panne totale", u"Le Perreux (94)", u"Dans votre zone",
         u"Pas d'urgence vitale")
   + dire(u"Adresse, nature de la panne, marque, niveau d'urgence. Et surtout : le chantier "
          u"est dans votre secteur.")),
  (u"Sam.", u"20:21", u"Samedi · 20:21", 'cal', u"Créneaux proposés",
   prix((u"Mardi", u"9 h 00", True), (u"Mardi", u"14 h 30", False),
        (u"Mercredi", u"8 h 00", False))
   + dire(u"Trois créneaux compatibles avec votre agenda réel et vos temps de trajet. Pas une "
          u"liste théorique.")),
  (u"Sam.", u"20:22", u"Samedi · 20:22", 'shield', u"Rendez-vous confirmé",
   chips(u"Mardi 9 h 00", u"Posé dans votre agenda", u"Fiche client créée",
         u"Récapitulatif envoyé")
   + dire(u"Huit minutes entre le premier message et le rendez-vous confirmé. Votre assiette "
          u"n'a pas refroidi.")),
  (u"Lun.", u"18:00", u"Lundi · 18:00", 'bell', u"Rappel la veille",
   cite(u"Bonjour, nous confirmons notre intervention demain mardi à 9 h au 14 rue des "
        u"Lilas. Répondez STOP si vous devez reporter.")
   + dire(u"C'est ce message-là qui vide les déplacements pour rien.")),
  (u"Mar.", u"07:00", u"Mardi · 07:00", 'star', u"Rappel deux heures avant",
   gain(u"9 h 00", u"le client est là, vous aussi — et vous n'avez passé aucun coup de fil.")
   + dire(u"S'il avait eu un empêchement, elle aurait proposé un autre créneau plutôt "
          u"qu'annuler.")),
 ],

 b4_h2=u"Trois missions, <em>zéro appel le soir</em>.",
 b4_sub=u"Du message reçu à 21 h jusqu'au rappel deux heures avant l'intervention, voici "
        u"exactement ce que votre assistante client fait à votre place.",
 cartes=[
  dict(role=u"Réponse", lab=u"Répondre 24 h/24",
       titre=u"Personne ne tombe sur la messagerie",
       acc=u"Réponse en moins d'une minute", acc2=u"nuit, week-end et congés",
       puces=[('chat', u"Hors horaires, week-end et congés"),
              ('doc', u"Réponses tirées de vos infos"),
              ('lock', u"Aucun prix ferme sans vous"),
              ('msg', u"E-mail, formulaire, WhatsApp, SMS"),
              ('user', u"Vous passe la main hors cadre")],
       cta=u"Voir le scénario complet", href=u"#scenario"),
  dict(role=u"Qualification", lab=u"Poser les bonnes questions",
       titre=u"La demande arrive complète",
       acc=u"Tout ce qu'il vous faut", acc2=u"avant même de décrocher",
       puces=[('filter', u"Urgence, devis, renseignement, suivi"),
              ('pin', u"Vérifie votre zone"),
              ('info', u"Complète ce qui manque"),
              ('user', u"Crée la fiche client"),
              ('bell', u"Remonte les vraies urgences")],
       cta=u"Qualifier mes demandes", href=u"reserver.html"),
  dict(role=u"Agenda", lab=u"Caler le rendez-vous",
       titre=u"Votre semaine se remplit toute seule",
       acc=u"Créneaux compatibles", acc2=u"trajets compris",
       puces=[('cal', u"Créneaux tirés de votre agenda"),
              ('pin', u"Temps de trajet compris"),
              ('grid', u"Ajout dans Google Agenda ou Outlook"),
              ('send', u"Récapitulatif envoyé au client"),
              ('lock', u"Aucun rendez-vous hors zone")],
       cta=u"Remplir mon agenda", href=u"reserver.html"),
  dict(role=u"Rappels", lab=u"Confirmer et rappeler",
       titre=u"Moins de déplacements pour rien",
       acc=u"J-1 et H-2", acc2=u"par SMS et par e-mail",
       puces=[('bell', u"Rappel la veille, heure et adresse"),
              ('clock', u"Rappel deux heures avant"),
              ('msg', u"Sur son canal habituel"),
              ('shield', u"Confirmé dès qu'il répond"),
              ('loop', u"Replanifie en cas d'empêchement")],
       cta=u"Réduire mes rendez-vous manqués", href=u"reserver.html"),
 ],

 b5_h2=u"Vous gardez votre agenda et vos outils, <em>elle travaille avec</em>.",
 b5_sub=u"Elle écrit dans l'agenda que vous utilisez déjà et répond sur les canaux où vos "
        u"clients vous écrivent. Rien de nouveau à installer sur votre téléphone.",

 b6_h2=u"Combinez-la avec <em>l'Assistant Commercial</em> pour plus de résultats.",
 duo_slug='commercial', duo_role=u"Assistant commercial",
 duo_titre=u"Elle qualifie, il chiffre.",
 duo_texte=u"Une demande bien qualifiée devient un devis juste. Dès que l'Assistante Client a "
           u"réuni la surface, l'adresse et le délai, l'Assistant Commercial prépare le devis "
           u"sur votre grille tarifaire et le relance jusqu'à la signature.",

 b7_h2=u"Avant, et <em>avec Talos</em>.",
 avant_apres=[
  (u"Vous rappelez le soir, entre deux repas", u"Talos répond dans la minute"),
  (u"Un appel manqué est un client perdu", u"Chaque message reçoit une réponse"),
  (u"Vous posez les questions au téléphone", u"La demande arrive déjà qualifiée"),
  (u"Vous vous déplacez hors de votre zone", u"Le secteur est vérifié avant le rendez-vous"),
  (u"Vous enchaînez deux chantiers trop loin", u"Le trajet est pris en compte"),
  (u"Des clients oublient le rendez-vous", u"Ils sont rappelés la veille et H-2"),
 ],

 b8_h2=u"Vous avez besoin d'un <em>standard qui ne dort pas</em> ?",
 b8_sub=u"Elle répond pendant que vous êtes sur un toit, et cale les rendez-vous dans les "
        u"trous de votre semaine. Vous ouvrez votre agenda le matin, il est rempli.",
 b8_reassure=[u"Mise en place personnalisée", u"Sans engagement",
              u"Données hébergées en France"],
)


# ═══════════════════════════════════════════════════════════════════════════
#  ASSISTANT FACTURATION
# ═══════════════════════════════════════════════════════════════════════════

FACTURATION = dict(
 slug='facturation', pw=402, ph=1400, pronom=u'il', e=u'',
 alt=u"L'assistant facturation de Talos",
 role=u"Assistant facturation", role_bas=u"l'assistant facturation",
 titre=u"Assistant facturation — Talos | Il ne laisse passer aucune facture",
 desc=u"L'assistant facturation de Talos transforme chaque devis signé en facture conforme : "
      u"acompte, situations de travaux, TVA, numérotation continue, format électronique 2026 "
      u"et archivage.",
 og_titre=u"Votre facturation qui ne laisse passer aucune ligne",
 og_desc=u"Acompte, situations, solde, TVA et format 2026 : la facture sort juste, à l'heure, "
         u"sans une seule ressaisie.",

 h1=u"Votre facturation qui ne laisse passer <em>aucune ligne</em>.",
 lede=u"Dès que le devis est signé, il sort la facture d'acompte, suit les situations de "
      u"travaux et solde le chantier. Au bon taux de TVA, au format 2026, archivé.",
 atouts=[('doc', u"Facture dès le devis signé"),
         ('bag', u"Émet acomptes et situations de travaux"),
         ('grille', u"Pose la TVA et les mentions obligatoires"),
         ('grid', u"Numérote sans trou ni doublon"),
         ('send', u"Archive et exporte pour votre comptable")],

 b2_h2=u"Transformez chaque signature en <em>facture conforme</em>.",
 missions=[
  (u"01 — Émettre", u"La facture démarre à la signature",
   u"Le devis signé devient facture d'acompte sans ressaisie : mêmes lignes, mêmes prix, même "
   u"client. Vous n'ouvrez pas un tableur.",
   'doc', 'ec-devis_auto',
   u"Écran du devis signé qui bascule en facture"),
  (u"02 — Suivre", u"Chaque situation à son moment",
   u"Sur les chantiers longs, les situations suivent l'avancement que vous déclarez. Le reste "
   u"à facturer est toujours juste, le solde tient compte de tout.",
   'chart', 'ec-facturation_facturx',
   u"Écran d'une situation de travaux et du reste à facturer"),
  (u"03 — Classer", u"Conforme, archivé, exportable",
   u"Numérotation continue, TVA au bon taux, mentions obligatoires, format électronique "
   u"attendu en 2026 — puis l'archivage et l'export que votre comptable attend.",
   'shield', 'ec-suivi_chantier',
   u"Écran de l'archive des factures et de l'export comptable"),
 ],

 b3_h2=u"Le devis signé du lundi devient une <em>facture conforme</em>.",
 b3_sub=u"Un chantier de 46 000 € sur deux mois, de la signature jusqu'à l'export du "
        u"comptable. Vous déclarez l'avancement, il fait le reste.",
 b3_note_t=u"Votre part du travail : déclarer l'avancement.",
 b3_note_p=u"Deux clics par situation. Les montants, les mentions, la numérotation et le "
           u"format électronique sont posés sans vous.",
 etapes=[
  (u"Lun.", u"11:40", u"Lundi · 11:40", 'edit', u"Devis signé",
   chips(u"Groupe Café Central", u"46 000 €", u"Signé en ligne", u"Acompte 30 %")
   + dire(u"La signature arrive. Vous êtes sur un autre chantier, et ça n'a aucune "
          u"importance.")),
  (u"Lun.", u"11:41", u"Lundi · 11:41", 'doc', u"Facture d'acompte",
   gain(u"13 800 €", u"facturés à la commande, une minute après la signature.")
   + dire(u"Mêmes lignes que le devis, numéro suivant de votre série, mentions et TVA "
          u"posées. Vous relisez, vous envoyez.")),
  (u"", u"Sem. 3", u"Troisième semaine de chantier", 'chart', u"Situation n° 1",
   chips(u"Avancement 40 %", u"18 400 € facturés", u"Reste à facturer 13 800 €")
   + dire(u"Vous déclarez l'avancement depuis le chantier. La situation se calcule, l'acompte "
          u"est déduit.")),
  (u"", u"Sem. 6", u"Sixième semaine de chantier", 'chart', u"Situation n° 2",
   chips(u"Avancement 75 %", u"16 100 € facturés", u"Reste à facturer 11 500 €")
   + dire(u"Aucun double comptage, aucun oubli. Le cumul est juste à l'euro près.")),
  (u"", u"Réception", u"À la réception du chantier", 'shield', u"Facture de solde",
   gain(u"11 500 €", u"de solde — après déduction de tout ce qui a déjà été facturé.")
   + dire(u"La retenue de garantie et les conditions de paiement du devis sont reprises "
          u"telles quelles.")),
  (u"", u"J+1", u"Le lendemain de la réception", 'send', u"Transmise au format 2026",
   chips(u"Factur-X", u"Numérotation continue", u"TVA 10 %", u"Archivée 10 ans")
   + dire(u"Le format attendu par la réforme, sans que vous ayez eu à changer quoi que ce "
          u"soit à vos habitudes.")),
  (u"", u"Fin mois", u"Le dernier jour du mois", 'grid', u"Export comptable",
   gain(u"1 fichier", u"pour douze factures — dans le format que votre cabinet attend.")
   + dire(u"Fini l'enveloppe de janvier et les trois relances de votre comptable.")),
 ],

 b4_h2=u"Trois temps, <em>zéro ressaisie</em>.",
 b4_sub=u"Du devis signé jusqu'à l'export du comptable, voici exactement ce que votre "
        u"assistant facturation fait à votre place.",
 cartes=[
  dict(role=u"Émission", lab=u"Sortir la facture",
       titre=u"Elle part sans que vous y pensiez",
       acc=u"Dès la signature", acc2=u"sans une seule ressaisie",
       puces=[('doc', u"Générée depuis le devis signé"),
              ('bag', u"Acompte au pourcentage convenu"),
              ('shield', u"Solde, déductions faites"),
              ('loop', u"Avoirs rattachés à l'origine"),
              ('lock', u"Rien ne part sans vous")],
       cta=u"Voir le scénario complet", href=u"#scenario"),
  dict(role=u"Avancement", lab=u"Suivre les chantiers longs",
       titre=u"Chaque situation à son moment",
       acc=u"Vous déclarez l'avancement", acc2=u"il calcule le reste",
       puces=[('chart', u"Situations selon l'avancement"),
              ('grille', u"Reste à facturer recalculé"),
              ('doc', u"Retenue de garantie reprise"),
              ('cal', u"Échéances et conditions posées"),
              ('search', u"Alerte si écart devis / facturé")],
       cta=u"Suivre mes chantiers longs", href=u"reserver.html"),
  dict(role=u"Conformité", lab=u"Tenir la réforme",
       titre=u"Conforme 2026, sans y penser",
       acc=u"Factur-X et numérotation continue", acc2=u"la première chose qu'on contrôle",
       puces=[('grid', u"Numérotation sans trou ni doublon"),
              ('grille', u"TVA et autoliquidation au bon taux"),
              ('send', u"Format électronique 2026"),
              ('info', u"Mentions obligatoires posées"),
              ('loop', u"Reprend votre numérotation")],
       cta=u"Être prêt pour 2026", href=u"reserver.html"),
  dict(role=u"Archivage", lab=u"Ranger et transmettre",
       titre=u"Tout est retrouvable en deux clics",
       acc=u"Dix ans d'archives", acc2=u"et un export mensuel propre",
       puces=[('lock', u"Dix ans, facture et devis liés"),
              ('search', u"Recherche par client ou chantier"),
              ('grid', u"Export au format de votre cabinet"),
              ('user', u"Accès lecture pour le comptable"),
              ('doc', u"Pièces du chantier au même endroit")],
       cta=u"Simplifier ma fin de mois", href=u"reserver.html"),
 ],

 b5_h2=u"Vous gardez votre compta et vos outils, <em>il travaille avec</em>.",
 b5_sub=u"Il reprend votre numérotation là où elle en est et exporte dans le format que votre "
        u"cabinet attend. Personne n'a à changer de logiciel, ni vous ni lui.",

 b6_h2=u"Combinez-le avec <em>l'Assistante Trésorerie</em> pour plus de résultats.",
 duo_slug='tresorerie', duo_role=u"Assistante trésorerie",
 duo_titre=u"Une facture émise n'est pas une facture payée.",
 duo_texte=u"Dès que l'échéance est dépassée, l'Assistante Trésorerie prend le relais : "
           u"relance graduée, pénalités de retard, échéancier et mise en demeure. Vous voyez "
           u"enfin ce qui rentre, et quand.",

 b7_h2=u"Avant, et <em>avec Talos</em>.",
 avant_apres=[
  (u"Vous refaites la facture le dimanche", u"Elle part le jour de la signature"),
  (u"Vous ressaisissez les lignes du devis", u"Rien n'est retapé"),
  (u"Vous recalculez le reste à facturer", u"Le cumul est juste à chaque situation"),
  (u"Vous cherchez le bon taux de TVA", u"Il est posé selon le chantier"),
  (u"Vous redoutez la réforme de 2026", u"Le format est déjà celui attendu"),
  (u"Votre comptable relance trois fois", u"L'export part en fin de mois"),
 ],

 b8_h2=u"Vous avez besoin d'une <em>facturation carrée</em> ?",
 b8_sub=u"Il facture pendant que vous êtes sur le chantier, au bon montant et au bon format. "
        u"La réforme 2026 arrive — celui-ci l'a déjà passée.",
 b8_reassure=[u"Mise en place personnalisée", u"Conforme à la réforme 2026",
              u"Données hébergées en France"],
)


# ═══════════════════════════════════════════════════════════════════════════
#  ASSISTANTE ADMINISTRATIVE
# ═══════════════════════════════════════════════════════════════════════════

ADMINISTRATIF = dict(
 slug='administratif', pw=411, ph=1400, pronom=u'elle', e=u'e',
 alt=u"L'assistante administrative de Talos",
 role=u"Assistante administrative", role_bas=u"l'assistante administrative",
 titre=u"Assistante administrative — Talos | Elle ne laisse passer aucun mail important",
 desc=u"L'assistante administrative de Talos trie votre boîte mail en six catégories, résume "
      u"les longs échanges, remonte les urgences et classe chaque pièce au bon chantier.",
 og_titre=u"Votre boîte mail qui ne laisse passer aucune urgence",
 og_desc=u"Elle trie la nuit, résume les fils qui traînent, remonte ce qui ne peut pas "
         u"attendre et range chaque pièce au bon chantier.",

 h1=u"Votre boîte mail qui ne laisse passer <em>aucune urgence</em>.",
 lede=u"Elle trie vos mails pendant la nuit, résume les échanges qui traînent, remonte ce qui "
      u"ne peut pas attendre et range chaque pièce au bon chantier. Vous ouvrez votre boîte "
      u"une fois par jour, pas vingt.",
 atouts=[('filter', u"Trie votre boîte en six catégories"),
         ('chat', u"Résume les longs échanges"),
         ('bell', u"Remonte ce qui ne peut pas attendre"),
         ('doc', u"Classe chaque pièce au bon chantier"),
         ('info', u"Signale ce qui manque au dossier")],

 b2_h2=u"Transformez chaque boîte pleine en <em>pile du matin</em>.",
 missions=[
  (u"01 — Trier", u"Six catégories, plus rien au hasard",
   u"Demande client, facture fournisseur, administratif, chantier, publicité, sans suite : "
   u"chaque mail est rangé dès son arrivée, avec ce qu'il contient.",
   'filter', 'ec-tri_inbox',
   u"Écran de la boîte mail triée en catégories"),
  (u"02 — Résumer", u"Vingt échanges tiennent en trois lignes",
   u"Un fil qui traîne depuis dix jours est résumé : ce qui a été décidé, ce qui bloque, et ce "
   u"qu'on attend de vous. Avec les montants et les dates sortis du texte.",
   'chat', 'ec-reponse_247',
   u"Écran du résumé d'un long échange de mails"),
  (u"03 — Classer", u"Chaque pièce à son chantier",
   u"Facture fournisseur, PV de réception, attestation : le document est détaché, nommé et "
   u"rangé dans le dossier du bon chantier. Retrouvable en une question.",
   'doc', 'ec-home',
   u"Écran du dossier de chantier avec ses pièces classées"),
 ],

 b3_h2=u"Les quarante-trois mails de la nuit deviennent <em>trois décisions</em>.",
 b3_sub=u"Une boîte du lundi matin comme les autres. Elle a trié, résumé, classé et alerté "
        u"pendant que vous dormiez.",
 b3_note_t=u"Votre part du travail : deux minutes de lecture.",
 b3_note_p=u"Elle ne supprime rien et ne répond à personne à votre place. Elle range, elle "
           u"résume, et elle vous montre ce qui compte vraiment.",
 etapes=[
  (u"", u"23:00", u"Dimanche · 23:00", 'msg', u"Vous fermez votre boîte",
   chips(u"43 mails non lus", u"3 qui comptent vraiment")
   + dire(u"Vous ne savez pas encore lesquels. C'est bien ça le problème.")),
  (u"", u"02:14", u"Lundi · 02:14", 'filter', u"Tri en six catégories",
   chips(u"Demandes client 6", u"Factures fournisseurs 9", u"Chantier 4", u"Administratif 3",
         u"Publicité 19", u"Sans suite 2")
   + dire(u"Rien n'est supprimé. Les publicités sortent de la boîte principale, elles "
          u"restent consultables.")),
  (u"", u"05:30", u"Lundi · 05:30", 'chat', u"Un fil de 22 messages résumé",
   cite(u"Décidé : la pose est reportée au 14. Bloque : l'attestation décennale manque au "
        u"dossier. Attendu de vous : l'envoyer avant vendredi.")
   + dire(u"Trois lignes au lieu de vingt-deux messages. Et l'action à faire, en clair.")),
  (u"", u"06:10", u"Lundi · 06:10", 'doc', u"Pièces détachées et classées",
   chips(u"9 factures fournisseurs rangées", u"2 PV de réception", u"1 attestation manquante")
   + dire(u"Chaque pièce jointe rejoint le dossier de son chantier, nommée proprement. Ce qui "
          u"manque vous est signalé avant que ce soit un problème.")),
  (u"", u"06:40", u"Lundi · 06:40", 'bell', u"Une urgence remonte",
   cite(u"Chantier Val-Fleuri : la livraison de carrelage est annulée, l'équipe est sur place "
        u"lundi matin.")
   + dire(u"Ce mail-là passe devant les quarante-deux autres, avec le motif de l'alerte.")),
  (u"", u"07:00", u"Lundi · 07:00", 'send', u"Accusés de réception partis",
   dire(u"Les six clients savent que leur message est arrivé et qu'on revient vers eux. "
        u"C'est le seul message qui part automatiquement — et vous en fixez le texte.")),
  (u"", u"07:02", u"Lundi · 07:02", 'shield', u"Votre pile du matin",
   gain(u"3 décisions", u"à prendre. Le reste est déjà rangé, résumé et classé.")
   + dire(u"Deux minutes de lecture au lieu d'une heure de tri. Et vous n'avez rien raté.")),
 ],

 b4_h2=u"Trois gestes, <em>zéro mail perdu</em>.",
 b4_sub=u"Du tri de la nuit jusqu'au classement des pièces au bon chantier, voici exactement "
        u"ce que votre assistante administrative fait à votre place.",
 cartes=[
  dict(role=u"Tri", lab=u"Vider la boîte",
       titre=u"Six catégories, dès l'arrivée",
       acc=u"Trié pendant la nuit", acc2=u"rien n'est jamais supprimé",
       puces=[('filter', u"Six catégories dès la réception"),
              ('search', u"Adresses, dates et montants extraits"),
              ('grid', u"Publicités écartées, jamais supprimées"),
              ('send', u"Accusé de réception au client"),
              ('lock', u"Expéditeurs exclus sur demande")],
       cta=u"Voir le scénario complet", href=u"#scenario"),
  dict(role=u"Résumé", lab=u"Comprendre vite",
       titre=u"Vingt échanges en trois lignes",
       acc=u"Décidé, bloqué, attendu de vous", acc2=u"rien d'autre",
       puces=[('chat', u"Les longs fils en trois lignes"),
              ('info', u"Décidé, bloqué, attendu de vous"),
              ('grille', u"Montants, dates et références"),
              ('user', u"Historique client rattaché")],
       cta=u"Ne plus tout relire", href=u"reserver.html"),
  dict(role=u"Urgences", lab=u"Faire remonter",
       titre=u"Ce qui ne peut pas attendre passe devant",
       acc=u"En haut de la pile", acc2=u"avec le motif de l'alerte",
       puces=[('bell', u"Urgences chantier et administratives"),
              ('clock', u"Échéances repérées dans le mail"),
              ('star', u"En haut de pile, motif inclus"),
              ('info', u"Pièces manquantes rappelées")],
       cta=u"Ne plus rater une urgence", href=u"reserver.html"),
  dict(role=u"Classement", lab=u"Ranger au bon endroit",
       titre=u"Chaque pièce à son chantier",
       acc=u"Détachée, nommée, rangée", acc2=u"et prête pour le comptable",
       puces=[('doc', u"Rattaché au bon chantier"),
              ('bag', u"Factures fournisseurs prêtes"),
              ('shield', u"Devis, PV et attestations réunis"),
              ('search', u"Recherche en langage courant"),
              ('loop', u"Une correction ne se répète pas")],
       cta=u"Ranger mes chantiers", href=u"reserver.html"),
 ],

 b5_h2=u"Vous gardez votre boîte mail, <em>elle travaille dedans</em>.",
 b5_sub=u"On branche votre adresse professionnelle, pas votre boîte privée. Vos dossiers "
        u"restent les vôtres : elle range, elle ne déménage rien.",

 b6_h2=u"Combinez-la avec <em>l'Assistante Client</em> pour plus de résultats.",
 duo_slug='client', duo_role=u"Assistante client",
 duo_titre=u"Elle trie, l'autre répond.",
 duo_texte=u"Une demande client repérée dans le tri de la nuit n'attend pas votre réveil : "
           u"l'Assistante Client y répond dans la minute, la qualifie et cale le rendez-vous. "
           u"Votre boîte se vide toute seule, par les deux bouts.",

 b7_h2=u"Avant, et <em>avec Talos</em>.",
 avant_apres=[
  (u"Vous triez vos mails le soir", u"C'est fait avant votre réveil"),
  (u"Vous relisez vingt messages d'affilée", u"Le fil tient en trois lignes"),
  (u"Une urgence se perd dans la masse", u"Elle passe en haut de la pile"),
  (u"Vous cherchez une facture fournisseur", u"Elle est au dossier du chantier"),
  (u"Le client attend un signe de vie", u"L'accusé de réception est parti"),
  (u"Il manque une pièce au dossier", u"Le manque vous est signalé"),
 ],

 b8_h2=u"Vous avez besoin d'une <em>boîte mail tenue</em> ?",
 b8_sub=u"Elle trie la nuit et vous remet trois décisions le matin. Le reste est rangé, "
        u"résumé, classé — et toujours consultable.",
 b8_reassure=[u"Mise en place personnalisée", u"Aucune suppression",
              u"Données hébergées en France"],
)


FICHES = [COMMERCIAL, TRESORERIE, CLIENT, FACTURATION, ADMINISTRATIF]
PAR_SLUG = dict((f['slug'], f) for f in FICHES)
