import pygame
import sys

# --- Paramètres généraux ---
NB_LIGNES = 9
NB_COLONNES = 5
MARGE = 2

# Taille automatique pour s'adapter à un écran de 800x600 max
LARGEUR_MAX, HAUTEUR_MAX = 800, 600
LARGEUR_CASE = 80
HAUTEUR_CASE = 80
TAILLE_ECRAN = (NB_COLONNES * LARGEUR_CASE, NB_LIGNES * HAUTEUR_CASE)
# Couleurs
COULEUR_FOND = (30, 30, 30)
COULEUR_CASE = (80, 80, 80)
COULEUR_JOUEUR = (0, 100, 255)

pygame.init()
screen = pygame.display.set_mode(TAILLE_ECRAN)
pygame.display.set_caption("Manoir magique - Prototype")

clock = pygame.time.Clock()

# Position du joueur (ligne, colonne) — commence en bas à gauche
joueur_ligne = 0
joueur_colonne = 2

def dessiner_grille():
    """Dessine la grille avec l'origine en bas à gauche."""
    screen.fill(COULEUR_FOND)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            # ligne 0 = en bas de l’écran
            y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + MARGE
            x = j * LARGEUR_CASE + MARGE
            rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
            pygame.draw.rect(screen, COULEUR_CASE, rect)

    # Dessiner le joueur
    x_centre = joueur_colonne * LARGEUR_CASE + LARGEUR_CASE // 2
    y_centre = (NB_LIGNES - 1 - joueur_ligne) * HAUTEUR_CASE + HAUTEUR_CASE // 2
    pygame.draw.circle(screen, COULEUR_JOUEUR, (x_centre, y_centre), 10)

    pygame.display.flip()

# --- Boucle principale ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and joueur_ligne < NB_LIGNES - 1:
                joueur_ligne += 1
            elif event.key == pygame.K_s and joueur_ligne > 0:
                joueur_ligne -= 1
            elif event.key == pygame.K_q and joueur_colonne > 0:
                joueur_colonne -= 1
            elif event.key == pygame.K_d and joueur_colonne < NB_COLONNES - 1:
                joueur_colonne += 1

    dessiner_grille()
    clock.tick(30)
