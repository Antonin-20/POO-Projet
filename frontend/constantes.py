# --- Constantes globales ---

NB_LIGNES = 9
NB_COLONNES = 5
MARGE = 2

LARGEUR_GRILLE_FIXE = 400
HAUTEUR_GRILLE_FIXE = 720

LARGEUR_CASE = LARGEUR_GRILLE_FIXE // NB_COLONNES      # 400 // 5 = 80
HAUTEUR_CASE = HAUTEUR_GRILLE_FIXE // NB_LIGNES        # 720 // 9 = 80


# --- Thème graphique : Blueprint ---

# Fond du manoir (bleu très foncé)
COUL_FOND = (10, 27, 42)            # #0A1B2A

# Couleur des cases (bleu foncé un peu plus clair)
COUL_CASE = (14, 42, 71)            # #0E2A47

# Lignes, contours, grille (cyan lumineux)
COUL_LIGNE = (100, 200, 255)        # #64C8FF


# Couleur du texte (blanc légèrement bleuté)
COUL_TEXTE = (230, 244, 255)        # #E6F4FF
COUL_TEXTE_CYAN = (100, 200, 255)

COUL_INVENTAIRE = (42, 101, 161) # Bleu grisâtre

COUL_CHOIX = (100, 120, 200) # Bleu

# Texte secondaire / faible
COUL_TEXTE_FAIBLE = (170, 190, 210)

# Sélection (cyan clair)
COUL_SELECTION = (164, 228, 255)    # #A4E4FF

# Menus (bleu nuit)
COUL_MENU = (8, 18, 30)             # très sombre

# Couleur accent (doré pour objets rares)
COUL_DORE = (249, 214, 92)

# Feedback
COUL_SUCCES = (140, 255, 180)
COUL_ECHEC = (255, 130, 130)


# --- Autres constantes ---

TAILLE_ICONE = 40
