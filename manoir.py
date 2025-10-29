import pygame
import sys
import os  # pour construire le chemin vers les images

# --- Paramètres du manoir ---
NB_LIGNES = 9
NB_COLONNES = 5
MARGE = 2 # espace entre les cases

# Taille fixe de la grille (elle ne s’étire jamais)
LARGEUR_GRILLE_FIXE = 400
HAUTEUR_GRILLE_FIXE = 720
LARGEUR_CASE = LARGEUR_GRILLE_FIXE // NB_COLONNES
HAUTEUR_CASE = HAUTEUR_GRILLE_FIXE // NB_LIGNES

# Couleurs
COUL_FOND = (30, 30, 30)
COUL_CASE = (80, 80, 80)
COUL_JOUEUR = (0, 100, 255)
COUL_INVENTAIRE = (50, 50, 70)
COUL_TEXTE = (255, 255, 255)

# Initialisation
pygame.init()
pygame.display.set_caption("Manoir magique")
font = pygame.font.SysFont("arial", 24)
TAILLE_ECRAN = (900, 720)
screen = pygame.display.set_mode(TAILLE_ECRAN, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Joueur
joueur_ligne = 0
joueur_colonne = 2

# --- Chargement des images de l’inventaire ---
nom_images = ["footprint.png", "coins.png", "diamond.png", "key.png", "dice.png"]
inventaire_images = []
TAILLE_ICONE = 40  # taille en pixels

for nom in nom_images:
    chemin = os.path.join("Images", nom)
    img = pygame.image.load(chemin)
    if nom.lower().endswith(".png"):
        img = img.convert_alpha()
    else:
        img = img.convert()
    img = pygame.transform.scale(img, (TAILLE_ICONE, TAILLE_ICONE))
    inventaire_images.append(img)

plein_ecran = False

def dessiner_grille(surface, x_offset, y_offset):
    """Dessine la grille à gauche avec taille fixe."""
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + y_offset + MARGE
            x = j * LARGEUR_CASE + x_offset + MARGE
            rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
            pygame.draw.rect(surface, COUL_CASE, rect)

    # Dessiner le "joueur" sous forme de bordure blanche
    joueur_x = x_offset + joueur_colonne * LARGEUR_CASE + MARGE
    joueur_y = y_offset + (NB_LIGNES - 1 - joueur_ligne) * HAUTEUR_CASE + MARGE
    joueur_rect = pygame.Rect(joueur_x, joueur_y,
                              LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
    pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)  # 3 = épaisseur du contour

def dessiner_inventaire(surface, largeur_fenetre, hauteur_fenetre):
    """Dessine la zone d’inventaire à droite avec texte et images en colonne en haut."""
    x_inv = LARGEUR_GRILLE_FIXE
    largeur_inv = max(largeur_fenetre - LARGEUR_GRILLE_FIXE, 200)
    zone = pygame.Rect(x_inv, 0, largeur_inv, hauteur_fenetre)
    pygame.draw.rect(surface, COUL_INVENTAIRE, zone)

    # Titre
    titre = font.render("Inventaire", True, COUL_TEXTE)
    surface.blit(titre, (x_inv + 20, 60))

    # --- Images alignées en colonne en haut à droite ---
    marge_x = 20
    marge_y = 60  # à partir du haut de la zone
    espace = 10
    for i, img in enumerate(inventaire_images):
        x = x_inv + largeur_inv - TAILLE_ICONE - marge_x  # coller à droite
        y = marge_y + i * (TAILLE_ICONE + espace)        # verticalement
        surface.blit(img, (x, y))


# --- Boucle principale ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and plein_ecran:
                plein_ecran = False
                screen = pygame.display.set_mode(TAILLE_ECRAN, pygame.RESIZABLE)
            elif event.key == pygame.K_f:
                plein_ecran = True
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif event.key == pygame.K_z and joueur_ligne < NB_LIGNES - 1:
                joueur_ligne += 1
            elif event.key == pygame.K_s and joueur_ligne > 0:
                joueur_ligne -= 1
            elif event.key == pygame.K_q and joueur_colonne > 0:
                joueur_colonne -= 1
            elif event.key == pygame.K_d and joueur_colonne < NB_COLONNES - 1:
                joueur_colonne += 1
        elif event.type == pygame.VIDEORESIZE and not plein_ecran:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    largeur, hauteur = screen.get_size()
    screen.fill(COUL_FOND)
    dessiner_grille(screen, 0, (hauteur - HAUTEUR_GRILLE_FIXE) // 2)
    dessiner_inventaire(screen, largeur, hauteur)
    pygame.display.flip()
    clock.tick(30)
