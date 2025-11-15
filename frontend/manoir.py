import pygame
import json
import os 
from typing import Optional, List
from .constantes import *
import json


class Manoir:
    def __init__(self, room_catalog):
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


        # --- c'est ici qu'on va charger toutes les pieces du json ---
        self.images = {
            "entrance": self.entrance_img,
            "antechamber": self.antechamber_img
        }

        # On charge les autres rooms depuis le JSON
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")

        if os.path.exists(json_path):
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            rooms = data.get("rooms", [])
        else:
            rooms = []

        for r in rooms:
            room_id = r.get("id")
            image_rel = r.get("image")

            if not room_id or not image_rel:
                continue

            # On évite de recharger les 2 rooms déjà faites
            if room_id in ["entrance", "antechamber"]:
                continue

            img_path = os.path.join("assets", image_rel)
            if not os.path.exists(img_path):
                continue

            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.smoothscale(
                img,
                (LARGEUR_CASE - 4 * MARGE, HAUTEUR_CASE - 4 * MARGE)
            )
            self.images[room_id] = img
        
        self.room_doors = {r['id']: r['doors'] for r in rooms}
        
        # orientation des rooms (même taille que la grille)
        self.room_orientations = [[None for i in range(NB_COLONNES)] for j in range(NB_LIGNES)]
    

    def ajout_piece(self, surface, joueur, x_offset=0, y_offset=0):

        largeur_fenetre, hauteur_fenetre = surface.get_size()

        # On veut montrer la grille DU BAS VERS LE HAUT :
        # ligne 0 = bas, ligne 8 = haut.
        #
        # On calcule un y_offset pour que tout soit visible et centré :
        y_offset = (hauteur_fenetre - NB_LIGNES * HAUTEUR_CASE) // 2

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

        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        # Indication orientation
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
