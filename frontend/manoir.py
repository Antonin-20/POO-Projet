import pygame
import sys
import os
from .joueur import Joueur
from .inventaire import Inventaire
from .constantes import * 




class Manoir:
    def __init__(self):
        self.entrance_img = pygame.transform.smoothscale(
            pygame.image.load(('assets/Images/rooms/Entrance_Hall.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )
        self.antechamber_img = pygame.transform.smoothscale(
            pygame.image.load(('assets/Images/rooms/Antechamber.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )
        self.grille =  [[None for i in range(NB_COLONNES)] for i in range(NB_LIGNES)] #on crée une grille (vide pour le moment) qui va contenir toutes les pièces créées lors de la génération
        #2 pièces sont toujours initialisées : l'entrée et l'antichambre
        self.grille[0][2] = "entrance"
        self.grille[NB_LIGNES-1][2] = "antechamber"
    

    def ajout_piece(self, surface, joueur, x_offset=0, y_offset=0):

        largeur_fenetre, hauteur_fenetre = surface.get_size()

        # On veut montrer la grille DU BAS VERS LE HAUT :
        # ligne 0 = bas, ligne 8 = haut.
        #
        # On calcule un y_offset pour que tout soit visible et centré :
        y_offset = (hauteur_fenetre - NB_LIGNES * HAUTEUR_CASE) // 2

        for i in range(NB_LIGNES):
            for j in range(NB_COLONNES):

                # Conversion : ligne logique → position visuelle inversée
                ligne_affichee = (NB_LIGNES - 1 - i)

                x = j * LARGEUR_CASE + x_offset + MARGE
                y = ligne_affichee * HAUTEUR_CASE + y_offset + MARGE

                rect = pygame.Rect(
                    x, y,
                    LARGEUR_CASE - 2 * MARGE,
                    HAUTEUR_CASE - 2 * MARGE
                )

                pygame.draw.rect(surface, COUL_CASE, rect)
                pygame.draw.rect(surface, (255, 255, 255), rect, 1)

                salle = self.grille[i][j]
                if salle == "entrance":
                    surface.blit(self.entrance_img, (x + MARGE, y + MARGE))
                elif salle == "antechamber":
                    surface.blit(self.antechamber_img, (x + MARGE, y + MARGE))

        # --- Affichage du joueur ---
        ligne_affichee = (NB_LIGNES - 1 - joueur.ligne)

        joueur_x = joueur.colonne * LARGEUR_CASE + x_offset + MARGE
        joueur_y = ligne_affichee * HAUTEUR_CASE + y_offset + MARGE

        joueur_rect = pygame.Rect(
            joueur_x, joueur_y,
            LARGEUR_CASE - 2*MARGE,
            HAUTEUR_CASE - 2*MARGE
        )

        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        # Indication orientation
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
