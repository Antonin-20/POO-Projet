import pygame
import sys
import os

# --- Constantes globales ---
NB_LIGNES = 9
NB_COLONNES = 5
MARGE = 2

LARGEUR_GRILLE_FIXE = 400
HAUTEUR_GRILLE_FIXE = 720

LARGEUR_CASE = LARGEUR_GRILLE_FIXE // NB_COLONNES #400 // 5 = 80
HAUTEUR_CASE = HAUTEUR_GRILLE_FIXE // NB_LIGNES #720 // 9 = 80

COUL_FOND = (30, 30, 30) # Gris très foncé
COUL_CASE = (80, 80, 80) # Gris moyen
COUL_INVENTAIRE = (50, 50, 70) # Bleu grisâtre
COUL_TEXTE = (255, 255, 255) # Blanc
COUL_CHOIX = (100, 120, 200) # Bleu
COUL_SELECTION = (255, 200, 100) # Jaune

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
        if self.orientation == "haut" and self.ligne < NB_LIGNES - 1: #cette condition évite de sortir de la grille
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
        noms = ["footprint.png", "coins.png", "diamond.png", "key.png", "de.png"]
        for nom in noms:
            chemin = f"Images/{nom}"
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.smoothscale(img, (TAILLE_ICONE, TAILLE_ICONE))
            self.images.append(img)

        # Contrôle des choix
        self.afficher_room_choices = False
        self.room_choice_index = 0  # sélection actuelle

    def dessiner(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font):
        x_inv = LARGEUR_GRILLE_FIXE
        largeur_inv = max(largeur_fenetre - LARGEUR_GRILLE_FIXE, 200)
        zone = pygame.Rect(x_inv, 0, largeur_inv, hauteur_fenetre)
        pygame.draw.rect(surface, COUL_INVENTAIRE, zone)

        titre = font.render("Inventaire", True, COUL_TEXTE)
        surface.blit(titre, (x_inv + 20, 60))

        #Compteur de pas pour chaque déplacement
        compteur_texte = font.render(str(joueur.footprint), True, COUL_TEXTE)
        x_compteur = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_texte.get_width() - 5
        y_compteur = 68
        surface.blit(compteur_texte, (x_compteur, y_compteur))

        # Affichage des icônes
        marge_x, marge_y, espace = 20, 60, 20
        # for i, img in enumerate(self.images):
        #     x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
        #     y = marge_y + i * (TAILLE_ICONE + espace)
        #     surface.blit(img, (x, y))

        for i in range(len(self.images)):
            x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
            y = marge_y + i * (TAILLE_ICONE + espace)
            surface.blit(self.images[i], (x, y))

        if self.afficher_room_choices:
            self.draw_room_choices(surface, largeur_inv, hauteur_fenetre, x_inv)

    def draw_room_choices(self, surface, largeur_inv, hauteur_fenetre, x_inv):
        """Affiche trois carrés en bas à gauche de l'inventaire"""
        taille = 80
        espace = 25
        base_y = hauteur_fenetre - taille - 40
        base_x = x_inv + 40

        for i in range(3):
            rect = pygame.Rect(base_x + i * (taille + espace), base_y, taille, taille)
            couleur = COUL_SELECTION if i == self.room_choice_index else COUL_CHOIX
            pygame.draw.rect(surface, couleur, rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), rect, 2)

        font = pygame.font.SysFont("arial", 20)
        txt = font.render("Choix de salle :", True, (255, 255, 255))
        surface.blit(txt, (x_inv + 40, base_y - 30))

    def changer_selection(self, direction):
        """Change la sélection (gauche/droite)"""
        if direction == "gauche":
            self.room_choice_index = (self.room_choice_index - 1) % 3
        elif direction == "droite":
            self.room_choice_index = (self.room_choice_index + 1) % 3


class Manoir:
    def __init__(self):
        self.entrance_img = pygame.transform.smoothscale(
            pygame.image.load(('Images/Entrance_Hall_Icon.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )
        self.antechamber_img = pygame.transform.smoothscale(
            pygame.image.load(('Images/Antechamber_Icon.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )

    def dessiner(self, surface, joueur, x_offset, y_offset):
        # x_offset = 0 et y_offset = 90 dans la boucle principale
        #HAUTEUR_CASE = 80, MARGE = 2, LARGEUR_CASE = 80
        for i in range(NB_LIGNES): # de 0 à 8
            for j in range(NB_COLONNES): # de 0 à 4
                y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + y_offset + MARGE #position verticale de la case
                x = j * LARGEUR_CASE + x_offset + MARGE #position horizontale de la case
                
                rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE) #rectangle de la case
                pygame.draw.rect(surface, COUL_CASE, rect) #dessine la case

                if i == 0 and j == 2:
                    surface.blit(self.entrance_img, (x + MARGE, y + MARGE))
                elif i == NB_LIGNES - 1 and j == 2:
                    surface.blit(self.antechamber_img, (x + MARGE, y + MARGE))

        joueur_x = x_offset + joueur.colonne * LARGEUR_CASE + MARGE
        joueur_y = y_offset + (NB_LIGNES - 1 - joueur.ligne) * HAUTEUR_CASE + MARGE
        joueur_rect = pygame.Rect(joueur_x, joueur_y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)
        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

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
        self.phase_choix = False  # vrai quand on choisit une salle

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

                    elif not self.phase_choix:  # phase normale
                        if event.key == pygame.K_z:
                            self.joueur.orienter("haut")
                        elif event.key == pygame.K_s:
                            self.joueur.orienter("bas")
                        elif event.key == pygame.K_q:
                            self.joueur.orienter("gauche")
                        elif event.key == pygame.K_d:
                            self.joueur.orienter("droite")
                        elif event.key == pygame.K_SPACE:
                            # Active la phase de choix
                            self.phase_choix = True
                            self.inventaire.afficher_room_choices = True
                    else:  # phase de choix
                        if event.key == pygame.K_LEFT:
                            self.inventaire.changer_selection("gauche")
                        elif event.key == pygame.K_RIGHT: 
                            self.inventaire.changer_selection("droite")
                        elif event.key == pygame.K_SPACE:
                            # Confirmation du choix
                            self.phase_choix = False
                            self.inventaire.afficher_room_choices = False
                            self.joueur.deplacer()

                elif event.type == pygame.VIDEORESIZE and not self.plein_ecran:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            largeur, hauteur = self.screen.get_size()
            self.screen.fill(COUL_FOND)

            self.manoir.dessiner(self.screen, self.joueur, 0, 0) #y_offset = 90
            #x_offset = 0 car la grille commence tout à gauche
            #hauteur = 900
            #HAUTEUR_GRILLE_FIXE = 720 => hauteur occupé de par la grille
            #espace libre = 900 - 720 = 180
            #on divise par 2 pour centrer verticalement => 90 pixels en haut et 90 pixels en bas

            self.inventaire.dessiner(self.screen, self.joueur, largeur, hauteur, self.font)
            pygame.display.flip()
            self.clock.tick(30)



