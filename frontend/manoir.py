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

    def ajout_piece(self, surface, joueur, x_offset, y_offset):
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

        # Calcul de la position du joueur
        joueur_x = x_offset + joueur.colonne * LARGEUR_CASE + MARGE
        joueur_y = y_offset + (NB_LIGNES - 1 - joueur.ligne) * HAUTEUR_CASE + MARGE

        # Création du rectangle du joueur
        joueur_rect = pygame.Rect(joueur_x, joueur_y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)

        # Dessin du rectangle du joueur
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

