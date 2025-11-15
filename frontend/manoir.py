import pygame
import json
import os 
from typing import Optional, List
from .constantes import *

class Manoir:

    def __init__(self,room_catalog):

        self.room_catalog = room_catalog  #dictionnaire se rapportant au .json avec tt les salles

        # --- Chargement des images ---
        self.images = {}
        for room_id, room in self.room_catalog.items():
            img_path = os.path.join("assets", room["image"])

            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.smoothscale(
                    img,
                    (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
                )
                self.images[room_id] = img
            except Exception as e:
                print(f"[WARNING] Impossible de charger {img_path} : {e}")

        # --- Création de la grille ---
        self.grille: List[List[Optional[str]]] = [
            [None for _ in range(NB_COLONNES)]
            for _ in range(NB_LIGNES)
        ]

        # 2 pièces initiales
        self.grille[0][2] = "entrance"
        self.grille[NB_LIGNES - 1][2] = "antechamber"


    # ---------------------------------------------------------------
    # Dessin de la grille + pièces + joueur
    # ---------------------------------------------------------------
    def ajout_piece(self, surface, joueur, x_offset, y_offset):

        for i in range(NB_LIGNES):
            for j in range(NB_COLONNES):

                # Coordonnées écran
                y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + y_offset + MARGE
                x = j * LARGEUR_CASE + x_offset + MARGE

                # Rectangle de la case
                rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)

                # Fond de la case
                pygame.draw.rect(surface, COUL_CASE, rect)

                # --- Récupération de la pièce associée ---
                piece_id = self.grille[i][j]

                if piece_id is not None:
                    img = self.images.get(piece_id)
                    if img:
                        surface.blit(img, (x + MARGE, y + MARGE))

        # -------------------------------------------------------
        # Dessin du joueur
        # -------------------------------------------------------
        joueur_x = x_offset + joueur.colonne * LARGEUR_CASE + MARGE
        joueur_y = y_offset + (NB_LIGNES - 1 - joueur.ligne) * HAUTEUR_CASE + MARGE

        joueur_rect = pygame.Rect(
            joueur_x, joueur_y,
            LARGEUR_CASE - 2*MARGE,
            HAUTEUR_CASE - 2*MARGE
        )

        # Contour blanc
        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        # Orientation
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
