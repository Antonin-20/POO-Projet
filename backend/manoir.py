import pygame
import json
import os 
from typing import Optional, List
from frontend.constantes import *
from backend.piece import Piece
import json


class Manoir:
    class Manoir:
        """
        Représente le manoir et sa grille de pièces.

        Cette classe gère :
        - la grille logique des pièces (entrance, antechamber, pièces générées),
        - le chargement et la mise à léchelle des images associées à chaque pièce,
        - le stockage des orientations de pièces,
        - et laffichage de la grille ainsi que du joueur sur la surface de jeu.
        """

    def __init__(self, room_catalog):
        # Antichambre et Entrance uniquement 
        self.entrance_img = pygame.transform.smoothscale(
            pygame.image.load(('assets/Images/rooms/Entrance_Hall.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )
        self.antechamber_img = pygame.transform.smoothscale(
            pygame.image.load(('assets/Images/rooms/Antechamber.png')).convert_alpha(),
            (LARGEUR_CASE - 4*MARGE, HAUTEUR_CASE - 4*MARGE)
        )


        # on crée une grille initialisee avec antichamber + entrance qui va ensuite contenir toutes les pièces créées lors de la génération
        self.grille =  [[None for i in range(NB_COLONNES)] for i in range(NB_LIGNES)] 
        self.grille[0][2] = Piece("entrance", (0, 2), "haut")
        self.grille[8][2] = Piece("antechamber", (8, 2), "haut")


        # Dictionnaire avec les images des pieces 
        self.images = {
            "entrance": self.entrance_img,
            "antechamber": self.antechamber_img
        }

        # ----------------------------
        # Charge les rooms du JSON                            #Cette partie doit être rendue obsolète par le loader, il faudra la corriger
        # ----------------------------
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # dossier Projet/
        json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")

        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            rooms = data.get("rooms", [])
        else:
            print("fichier JSON introuvable :", json_path)
            rooms = []

        # Chargement et mise à l’échelle des images des autres pièces
        for r in rooms:
            room_id = r.get("id")
            image_rel = r.get("image")

            if not room_id or not image_rel:
                continue

            # On ignore l'entrée et l'antichambre déjà gérées manuellement
            if room_id in ["entrance", "antechamber"]:
                continue

            img_path = os.path.join(BASE_DIR, "assets", image_rel)  # <- CHEMIN CORRECT
            if not os.path.exists(img_path):
                print("Image introuvable :", img_path)
                continue

            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.smoothscale(
                img,
                (LARGEUR_CASE - 4 * MARGE, HAUTEUR_CASE - 4 * MARGE)
            )
            self.images[room_id] = img
        
        # mapping id de pièce -> configuration de portes
        self.room_doors = {r['id']: r['doors'] for r in rooms}
        self.catalog = room_catalog

        # orientation des rooms (même taille que la grille)
        self.room_orientations = [[None for i in range(NB_COLONNES)] for j in range(NB_LIGNES)]
    

    def ajout_piece(self, surface, joueur, x_offset=0, y_offset=0):
        """
        Affiche la grille du manoir et le joueur sur la surface donnée.

        La grille est dessinée du bas vers le haut (ligne 0 en bas, ligne
        NB_LIGNES-1 en haut), avec les pièces orientées selon leur attribut
        `orientation`, puis le contour du joueur et son orientation sont tracés.
        """
        largeur_fenetre, hauteur_fenetre = surface.get_size()
        # ligne 0 = bas, ligne NB_LIGNES-1 = haut = 8
        # On calcule un y_offset pour que tout soit visible et centré :
        y_offset = (hauteur_fenetre - NB_LIGNES * HAUTEUR_CASE) // 2

        for i in range(NB_LIGNES):
            for j in range(NB_COLONNES):

                # Coordonnées écran (conversion grille -> écran)
                y = (NB_LIGNES - 1 - i) * HAUTEUR_CASE + y_offset + MARGE
                x = j * LARGEUR_CASE + x_offset + MARGE

                # Rectangle de la case
                rect = pygame.Rect(x, y, LARGEUR_CASE - 2*MARGE, HAUTEUR_CASE - 2*MARGE)

                # Fond de la case
                pygame.draw.rect(surface, COUL_CASE, rect)

                # Récupération de la pièce associée
                piece = self.grille[i][j]
                if piece is not None:
                    img = self.images.get(piece.id)  # récupère l'image via l'id
                    if piece.orientation != 0:
                        # Appliquer l’orientation (sens horaire pour pygame)
                        img = pygame.transform.rotate(img, piece.orientation) 
                    surface.blit(img, (x + MARGE, y + MARGE))

        # Dessin du joueur
        joueur_x = x_offset + joueur.colonne * LARGEUR_CASE + MARGE
        joueur_y = y_offset + (NB_LIGNES - 1 - joueur.ligne) * HAUTEUR_CASE + MARGE

        joueur_rect = pygame.Rect(
            joueur_x, joueur_y,
            LARGEUR_CASE - 2*MARGE,
            HAUTEUR_CASE - 2*MARGE
        )

        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        # Indication de l’orientation du joueur (trait rouge sur le bord correspondant)
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
