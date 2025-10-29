import pygame
import sys
import os

# --- Constantes globales ---
NB_LIGNES = 9
NB_COLONNES = 5
MARGE = 2
LARGEUR_GRILLE_FIXE = 400
HAUTEUR_GRILLE_FIXE = 720
LARGEUR_CASE = LARGEUR_GRILLE_FIXE // NB_COLONNES
HAUTEUR_CASE = HAUTEUR_GRILLE_FIXE // NB_LIGNES

COUL_FOND = (30, 30, 30)
COUL_CASE = (80, 80, 80)
COUL_INVENTAIRE = (50, 50, 70)
COUL_TEXTE = (255, 255, 255)

TAILLE_ICONE = 40


class Joueur:
    def __init__(self, ligne=0, colonne=2):
        self.ligne = ligne
        self.colonne = colonne
        self.orientation = "haut"
        self.footprint = 70

    def orienter(self, direction):
        self.orientation = direction

    def deplacer(self):
        ancienne_pos = (self.ligne, self.colonne)
        if self.orientation == "haut" and self.ligne < NB_LIGNES - 1:
            self.ligne += 1
        elif self.orientation == "bas" and self.ligne > 0:
            self.ligne -= 1
        elif self.orientation == "gauche" and self.colonne > 0:
            self.colonne -= 1
        elif self.orientation == "droite" and self.colonne < NB_COLONNES - 1:
            self.colonne += 1

        if (self.ligne, self.colonne) != ancienne_pos:
            self.footprint = max(0, self.footprint - 1)


class Inventaire:
    def __init__(self):
        self.images = []
        noms = ["footprint.png", "coins.png", "diamond.png", "key.png", "dice.png"]
        for nom in noms:
            chemin = os.path.join("Images", nom)
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.smoothscale(img, (TAILLE_ICONE, TAILLE_ICONE))
            self.images.append(img)

    def dessiner(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font):
        x_inv = LARGEUR_GRILLE_FIXE
        largeur_inv = max(largeur_fenetre - LARGEUR_GRILLE_FIXE, 200)
        zone = pygame.Rect(x_inv, 0, largeur_inv, hauteur_fenetre)
        pygame.draw.rect(surface, COUL_INVENTAIRE, zone)

        titre = font.render("Inventaire", True, COUL_TEXTE)
        surface.blit(titre, (x_inv + 20, 60))

        compteur_texte = font.render(str(joueur.footprint), True, COUL_TEXTE)
        x_compteur = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_texte.get_width() - 5
        y_compteur = 68
        surface.blit(compteur_texte, (x_compteur, y_compteur))

        marge_x, marge_y, espace = 20, 60, 20
        for i, img in enumerate(self.images):
            x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
            y = marge_y + i * (TAILLE_ICONE + espace)
            surface.blit(img, (x, y))


class Manoir:
    def __init__(self):
        self.entrance_img = pygame.transform.smoothscale(
            pygame.image.load(os.path.join("Images", "Entrance_Hall_Icon.png")).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )
        self.antechamber_img = pygame.transform.smoothscale(
            pygame.image.load(os.path.join("Images", "Antechamber_Icon.png")).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )

    def dessiner(self, surface, joueur, x_offset, y_offset):
        for i in range(NB_LIGNES):
            for j in range(NB_COLONNES):
                y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + y_offset + MARGE
                x = j * LARGEUR_CASE + x_offset + MARGE
                rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
                pygame.draw.rect(surface, COUL_CASE, rect)

                if i == 0 and j == 2:
                    surface.blit(self.entrance_img, (x + MARGE, y + MARGE))
                elif i == NB_LIGNES - 1 and j == 2:
                    surface.blit(self.antechamber_img, (x + MARGE, y + MARGE))

        # --- Dessine le joueur ---
        joueur_x = x_offset + joueur.colonne * LARGEUR_CASE + MARGE
        joueur_y = y_offset + (NB_LIGNES - 1 - joueur.ligne) * HAUTEUR_CASE + MARGE
        joueur_rect = pygame.Rect(joueur_x, joueur_y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        # Orientation visible par un côté plus épais
        ep = 6
        rouge = (255, 0, 0)
        if joueur.orientation == "haut":
            pygame.draw.line(surface, rouge, (joueur_rect.left, joueur_rect.top), (joueur_rect.right, joueur_rect.top), ep)
        elif joueur.orientation == "bas":
            pygame.draw.line(surface, rouge, (joueur_rect.left, joueur_rect.bottom), (joueur_rect.right, joueur_rect.bottom), ep)
        elif joueur.orientation == "gauche":
            pygame.draw.line(surface, rouge, (joueur_rect.left, joueur_rect.top), (joueur_rect.left, joueur_rect.bottom), ep)
        elif joueur.orientation == "droite":
            pygame.draw.line(surface, rouge, (joueur_rect.right, joueur_rect.top), (joueur_rect.right, joueur_rect.bottom), ep)


class Jeu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Manoir magique")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.joueur = Joueur()
        self.inventaire = Inventaire()
        self.manoir = Manoir()
        self.plein_ecran = False

    def boucle_principale(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.plein_ecran:
                        self.plein_ecran = False
                        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)
                    elif event.key == pygame.K_f:
                        self.plein_ecran = True
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                    elif event.key == pygame.K_z:
                        self.joueur.orienter("haut")
                    elif event.key == pygame.K_s:
                        self.joueur.orienter("bas")
                    elif event.key == pygame.K_q:
                        self.joueur.orienter("gauche")
                    elif event.key == pygame.K_d:
                        self.joueur.orienter("droite")
                    elif event.key == pygame.K_SPACE:
                        self.joueur.deplacer()

                elif event.type == pygame.VIDEORESIZE and not self.plein_ecran:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            largeur, hauteur = self.screen.get_size()
            self.screen.fill(COUL_FOND)
            self.manoir.dessiner(self.screen, self.joueur, 0, (hauteur - HAUTEUR_GRILLE_FIXE)//2)
            self.inventaire.dessiner(self.screen, self.joueur, largeur, hauteur, self.font)
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    Jeu().boucle_principale()
