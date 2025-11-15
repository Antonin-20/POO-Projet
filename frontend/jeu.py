import pygame 
import sys
import os
from .constantes import *
from .joueur import Joueur
from .inventaire import Inventaire
from backend.piece import Piece
from backend.manoir import Manoir
from backend.aleatoire_generation_pieces import *



class Jeu:
    def __init__(self,room_catalog):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Manoir Magique")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)

        # instanciation des classes
        self.joueur = Joueur() # objet joueur
        self.inventaire = Inventaire() # objet inventaire
        self.manoir = Manoir(room_catalog) # objet manoir

        self.plein_ecran = False
        self.phase_choix = False  # vrai quand on choisit une salle

        self.message_fin = ""
        self.fin_jeu = False
        self.victoire = False

        self.menu_actif = True


    def afficher_menu(self):
        self.screen.fill(COUL_MENU)

        # Titre
        font_titre = pygame.font.SysFont("arial", 70, bold=True)
        titre = font_titre.render("BLUE PRINCE", True, COUL_TEXTE_CYAN)
        self.screen.blit(titre, titre.get_rect(center=(self.screen.get_width()//2, 140)))

        # Sous-titre
        font_texte = pygame.font.SysFont("arial", 28)
        bienvenue = font_texte.render("Bienvenue", True, COUL_TEXTE)
        self.screen.blit(bienvenue, bienvenue.get_rect(center=(self.screen.get_width()//2, 210)))

        # Instructions
        font_instr = pygame.font.SysFont("arial", 22)
        instructions = [
            "Déplacements : Z Q S D",
            "Choisir une porte : Q / D",
            "Valider : ESPACE",
            "But : Atteindre l’Antichambre avant de manquer de pas"
        ]

        for i, texte in enumerate(instructions):
            ligne = font_instr.render(texte, True, COUL_TEXTE_FAIBLE)
            self.screen.blit(ligne, (100, 320 + i * 40))

        # Lancement
        font_start = pygame.font.SysFont("arial", 26, bold=True)
        start = font_start.render("Appuie sur [ESPACE] pour commencer", True, COUL_DORE)
        self.screen.blit(start, start.get_rect(center=(self.screen.get_width()//2, 600)))

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

    def afficher_fenetre_choix(self):
        """Affiche une fenêtre centrale pour choisir la salle."""
        largeur, hauteur = self.screen.get_size()
        
        # Taille de la fenêtre
        fenetre_largeur = 400
        fenetre_hauteur = 150
        x_fen = (largeur - fenetre_largeur) // 2
        y_fen = (hauteur - fenetre_hauteur) // 2

        # Fond semi-transparent derrière la fenêtre
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # Fenêtre principale
        fenetre_rect = pygame.Rect(x_fen, y_fen, fenetre_largeur, fenetre_hauteur)
        pygame.draw.rect(self.screen, COUL_MENU, fenetre_rect, border_radius=10)
        pygame.draw.rect(self.screen, COUL_TEXTE, fenetre_rect, 3, border_radius=10)

        # Titre
        font_titre = pygame.font.SysFont("arial", 26, bold=True)
        titre = font_titre.render("Choisis une salle", True, COUL_TEXTE)
        self.screen.blit(titre, (x_fen + 20, y_fen + 10))

        # Les 3 cases
        taille_case = 80
        espace = 25
        base_x = x_fen + 30
        base_y = y_fen + 50

        for i in range(3):
            rect = pygame.Rect(base_x + i*(taille_case + espace), base_y, taille_case, taille_case)
            # couleur selon sélection
            if i == self.inventaire.room_choice_index:
                couleur = COUL_SELECTION
            else:
                couleur = COUL_CHOIX
            pygame.draw.rect(self.screen, couleur, rect, 3, border_radius=8)
            pygame.draw.rect(self.screen, (255,255,255), rect, 2)

    def creer_nouvelle_piece(self):
        # Tirer 3 pièces depuis le pool
        choix = extrait_pool()

        # Stocker pour le pop-up
        self.inventaire.room_choices = choix
        self.inventaire.room_choice_index = 0
        self.inventaire.afficher_room_choices = True
        self.phase_choix = True

        while self.phase_choix:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.inventaire.changer_selection("gauche")
                    elif event.key == pygame.K_d:
                        self.inventaire.changer_selection("droite")
                    elif event.key == pygame.K_SPACE:
                        selection = self.inventaire.room_choices[self.inventaire.room_choice_index]

                        # Placer la pièce
                        ligne, col = self.joueur.ligne, self.joueur.colonne
                        nouvelle_piece = Piece(selection, (ligne, col), self.joueur.orientation)
                        self.manoir.grille[ligne][col] = nouvelle_piece

                        # Retirer la pièce choisie et remettre les autres dans le pool
                        retirer_piece_du_pool(selection)
                        autres = [p for p in choix if p != selection]
                        remettre_pieces_dans_pool(autres)

                        # Fin du choix
                        self.phase_choix = False
                        self.inventaire.afficher_room_choices = False



    def boucle_principale(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # -----------------------------------------
                #                MENU PRINCIPAL
                # -----------------------------------------
                if self.menu_actif:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.menu_actif = False
                    continue

                # -----------------------------------------
                #                FIN DE PARTIE
                # -----------------------------------------
                if self.fin_jeu:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reinitialiser_jeu()
                    continue

                # -----------------------------------------
                #           FULLSCREEN / RESIZE
                # -----------------------------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.plein_ecran:
                        self.plein_ecran = False
                        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)

                    elif event.key == pygame.K_f:
                        self.plein_ecran = True
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                    # -----------------------------------------
                    #           PHASE NORMALE (déplacement)
                    # -----------------------------------------
                    elif not self.phase_choix:

                        # orientation du joueur
                        #sert pour direction_regard par la suite (dans manoir.py))
                        if event.key == pygame.K_z:
                            self.joueur.orienter("haut")
                        elif event.key == pygame.K_s:
                            self.joueur.orienter("bas")
                        elif event.key == pygame.K_q:
                            self.joueur.orienter("gauche")
                        elif event.key == pygame.K_d:
                            self.joueur.orienter("droite")

                        # entrée en mode CHOIX DE SALLE
                        elif event.key == pygame.K_SPACE:
                             # --- 1) CALCULER LA CASE CIBLE EN FONCTION DE L’ORIENTATION ---
                            cible_ligne = self.joueur.ligne
                            cible_colonne = self.joueur.colonne

                            if self.joueur.orientation == "haut" and self.joueur.ligne < NB_LIGNES - 1:
                                cible_ligne += 1
                            elif self.joueur.orientation == "bas" and self.joueur.ligne > 0:
                                cible_ligne -= 1
                            elif self.joueur.orientation == "gauche" and self.joueur.colonne > 0:
                                cible_colonne -= 1
                            elif self.joueur.orientation == "droite" and self.joueur.colonne < NB_COLONNES - 1:
                                cible_colonne += 1
                            else:
                                # bord de grille
                                self.inventaire.message = "Il n'y a pas de porte dans cette direction"
                                continue

                            # --- 2) VERIFIER SI LA PORTE EXISTE DANS CETTE ORIENTATION ---
                            piece_depart = self.manoir.grille[self.joueur.ligne][self.joueur.colonne]
                            if piece_depart is not None:
                                portes_depart = piece_depart.doors
                            else:
                                portes_depart = []

                            # Calcul position cible selon orientation
                            cible_ligne = self.joueur.ligne
                            cible_colonne = self.joueur.colonne
                            if self.joueur.orientation == "haut" and self.joueur.ligne < NB_LIGNES - 1:
                                cible_ligne += 1
                            elif self.joueur.orientation == "bas" and self.joueur.ligne > 0:
                                cible_ligne -= 1
                            elif self.joueur.orientation == "gauche" and self.joueur.colonne > 0:
                                cible_colonne -= 1
                            elif self.joueur.orientation == "droite" and self.joueur.colonne < NB_COLONNES - 1:
                                cible_colonne += 1
                            else:
                                self.inventaire.message = "Il n'y a pas de porte dans cette direction"
                                continue

                            # Pièce cible (si elle existe)
                            piece_cible = self.manoir.grille[cible_ligne][cible_colonne]
                            portes_cible = piece_cible.doors if piece_cible else []

                            # Vérification cohérence double porte
                            porte_depart = self.joueur.ORIENTATION_TO_DOOR[self.joueur.orientation]
                            opposite = {"N":"S", "S":"N", "E":"W", "W":"E"}
                            porte_arrivee = opposite[porte_depart]

                            if porte_depart not in portes_depart or (piece_cible and porte_arrivee not in portes_cible):
                                self.inventaire.message = "Pas de porte dans cette direction !"
                                self.inventaire.message_timer = pygame.time.get_ticks()
                                continue

                            # --- 3) CASE CIBLE ---
                            if piece_cible is not None:
                                # case déjà occupée → déplacement direct
                                self.joueur.deplacer(self.manoir, self.inventaire)
                                self.verification_fin()
                            else:
                                # case vide → créer la nouvelle pièce avec pop-up
                                self.creer_nouvelle_piece()
                                self.verification_fin()


                    # -----------------------------------------
                    #           PHASE CHOIX DE SALLE
                    # -----------------------------------------
                    else:
                        if event.key == pygame.K_q:
                            self.inventaire.changer_selection("gauche")

                        elif event.key == pygame.K_d:
                            self.inventaire.changer_selection("droite")

                        elif event.key == pygame.K_SPACE:
                            # quitter la fenêtre de choix
                            self.phase_choix = False
                            self.inventaire.afficher_room_choices = False

                            # mémoriser l’ancienne position (si besoin)
                            ancienne_ligne = self.joueur.ligne
                            ancienne_colonne = self.joueur.colonne

                            # déplacement réel du joueur
                            self.joueur.deplacer(self.manoir, self.inventaire)

                            # --- PLACER LA PIÈCE DANS LA GRILLE COMME INSTANCE ---
                            room_id = self.inventaire.room_choices[self.inventaire.room_choice_index]
                            if room_id is not None:
                                # vérifier qu'on n'écrase pas entrée/antichambre
                                if self.manoir.grille[self.joueur.ligne][self.joueur.colonne] is None:
                                    # créer l'instance Piece
                                    pos = (self.joueur.ligne, self.joueur.colonne)
                                    direction = self.joueur.orientation
                                    nouvelle_piece = Piece(room_id, pos, direction)

                                    # stocker dans la grille
                                    self.manoir.grille[self.joueur.ligne][self.joueur.colonne] = nouvelle_piece



                            # test de fin
                            self.verification_fin()

                # -----------------------------------------
                #         REDIMENSIONNEMENT DE FENÊTRE
                # -----------------------------------------
                if event.type == pygame.VIDEORESIZE and not self.plein_ecran:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # -----------------------------------------
            #              AFFICHAGE GLOBAL
            # -----------------------------------------

            if self.menu_actif:
                self.afficher_menu()
            else:
                largeur, hauteur = self.screen.get_size()
                self.screen.fill(COUL_FOND)

                # manoir centré verticalement
                self.manoir.ajout_piece(self.screen, self.joueur, 0, 0)

                # inventaire à droite
                self.inventaire.affichage(self.screen, self.joueur, largeur, hauteur, self.font)
                
                # fenêtre de fin
                if self.fin_jeu:
                    self.afficher_message_fin()

                pygame.display.flip()

            self.clock.tick(30)
