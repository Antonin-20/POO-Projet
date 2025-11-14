import pygame 
import sys
import os
from .constantes import *
from .joueur import Joueur
from .inventaire import Inventaire
from .manoir import Manoir


class Jeu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Manoir Magique")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)

        # instanciation des classes
        self.joueur = Joueur() # objet joueur
        self.inventaire = Inventaire() # objet inventaire
        self.manoir = Manoir() # objet manoir

        self.plein_ecran = False
        self.phase_choix = False  # vrai quand on choisit une salle

        self.message_fin = ""
        self.fin_jeu = False
        self.victoire = False

        self.menu_actif = True

    def afficher_menu(self):
        """Affiche le menu principal avant de lancer la partie."""
        self.screen.fill((20, 20, 30))  # fond sombre

        # Titre du jeu
        font_titre = pygame.font.SysFont("arial", 60, bold=True)
        titre = font_titre.render(" Blue Prince ", True, (200, 200, 255))
        rect_titre = titre.get_rect(center=(self.screen.get_width()//2, 120))
        self.screen.blit(titre, rect_titre)

        # Message de bienvenue
        font_texte = pygame.font.SysFont("arial", 28)
        bienvenue = font_texte.render("Bienvenue dans Blue Prince", True, (255, 255, 255))
        rect_bienvenue = bienvenue.get_rect(center=(self.screen.get_width()//2, 220))
        self.screen.blit(bienvenue, rect_bienvenue)

        # Instructions
        font_instr = pygame.font.SysFont("arial", 22)
        instructions = [
            "Naviguer dans le jeu et le menu : Z (haut), Q (gauche), S (bas), D (droite)",
            "Valider : Espace",
            "Atteins l’antichambre pour gagner",
            "Si tu n’as plus de pas, tu perds"
        ]
        for i, texte in enumerate(instructions):
            ligne = font_instr.render(texte, True, (220, 220, 220))
            self.screen.blit(ligne, (100, 320 + i * 40))

        # Message d’invitation à jouer
        font_start = pygame.font.SysFont("arial", 26, bold=True)
        start = font_start.render("Appuie sur [ESPACE] pour commencer", True, (255, 220, 150))
        rect_start = start.get_rect(center=(self.screen.get_width()//2, 600))
        self.screen.blit(start, rect_start)

        pygame.display.flip()

    
    def verification_fin(self):
        """Vérifie si la partie est terminée (victoire ou défaite)."""

        if self.joueur.ligne == NB_LIGNES - 1 and self.joueur.colonne == 2: # Position de l'Antichambre
            self.victoire = True
            self.fin_jeu = True
            self.message_fin = "bravo"

        elif self.joueur.footprint <= 0:
            self.victoire = False
            self.fin_jeu = True
            self.message_fin = "perdu, t'as plus de pas"

    def reinitialiser_jeu(self):
        """Réinitialise les variables du jeu pour une nouvelle partie."""
        self.joueur = Joueur()
        self.inventaire = Inventaire()
        self.phase_choix = False
        self.message_fin = ""
        self.fin_jeu = False
        self.victoire = False

    def afficher_message_fin(self):
        """Affiche un écran de fin avec message et option de recommencer."""

        # on défini une surface semi-transparente de taille de l'écran (self.screen.get_size() )
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA) # pygame.SRCALPHA pour la transparence

        overlay.fill((0, 0, 0, 180)) # 180 pour l'opacité, plus c'est grand

        # on place la surface semi transparente dans l'écran
        self.screen.blit(overlay, (0, 0))

        font_titre = pygame.font.SysFont("arial", 48, bold=True)
        font_instr = pygame.font.SysFont("arial", 24)

        couleur = (100, 255, 100) if self.victoire else (255, 100, 100)
        texte1 = font_titre.render(self.message_fin, True, couleur)
        texte2 = font_instr.render("Appuyez sur [ESPACE] pour recommencer", True, (255, 255, 255))

        # placement des textes
        rect1 = texte1.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30))
        rect2 = texte2.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 40))

        self.screen.blit(texte1, rect1)
        self.screen.blit(texte2, rect2)

    def boucle_principale(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.menu_actif:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # quitte le menu et démarre la partie
                        self.menu_actif = False
                    # on ignore tous les autres événements tant qu'on est dans le menu
                    continue
                
                elif event.type == pygame.KEYDOWN and self.fin_jeu:
                    if event.key == pygame.K_SPACE:
                        self.reinitialiser_jeu()
                    continue

                # Juste pour ajuster l'écran
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
                        if event.key == pygame.K_q:
                            self.inventaire.changer_selection("gauche")
                        elif event.key == pygame.K_d: 
                            self.inventaire.changer_selection("droite")
                        elif event.key == pygame.K_SPACE:
                            # Confirmation du choix
                            self.phase_choix = False
                            self.inventaire.afficher_room_choices = False
                            self.joueur.deplacer()
                            self.verification_fin()

                elif event.type == pygame.VIDEORESIZE and not self.plein_ecran:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if self.menu_actif:

                self.afficher_menu()  # affiche le menu

            else:
            
                largeur, hauteur = self.screen.get_size()
                self.screen.fill(COUL_FOND)

                self.manoir.ajout_piece(self.screen, self.joueur, 0, 0) #y_offset = 90
                #x_offset = 0 car la grille commence tout à gauche
                #hauteur = 900
                #HAUTEUR_GRILLE_FIXE = 720 => hauteur occupé de par la grille
                #espace libre = 900 - 720 = 180
                #on divise par 2 pour centrer verticalement => 90 pixels en haut et 90 pixels en bas

                self.inventaire.affichage(self.screen, self.joueur, largeur, hauteur, self.font)

                if self.fin_jeu:
                    self.afficher_message_fin()
                pygame.display.flip()
                self.clock.tick(30)