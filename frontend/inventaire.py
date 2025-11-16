import pygame
import sys
import os
from frontend.constantes import *
from backend.aleatoire_generation_pieces import *
from frontend.joueur import Joueur
from backend.manoir import Manoir
import json

# --- Chargement du JSON pour récupérer toutes les infos des rooms ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)
rooms = data["rooms"]


class Inventaire:
    def __init__(self, room_catalog):
        # --- Icônes joueur ---
        self.images = []
        noms = ["footprint.png", "coins.png", "diamond.png", "key.png", "de.png"]
        for nom in noms:
            chemin = f"assets/Images/icone_inv/{nom}"
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.smoothscale(img, (TAILLE_ICONE,TAILLE_ICONE))
            self.images.append(img)

        
        self.message = ""
        self.message_timer = 0

        self.taille_case_piece = 180 #même taille que la case "pièce actuelle"

        # Précharger les images redimensionnées pour le carré "Pièce actuelle"
        # On redimensionne une seules fois tous les images des pièces à la taille de la case pour une bonne qualité
        self.room_images_scaled = {} #là où sera stocké l'id des images
        for r in rooms:
            chemin = os.path.join("assets", r["image"])
            if os.path.exists(chemin):
                img = pygame.image.load(chemin).convert_alpha()#récupère l'image
                # Redimensionne directement à la taille de la case
                img = pygame.transform.smoothscale(img, (self.taille_case_piece, self.taille_case_piece))
                self.room_images_scaled[r["id"]] = img


    # --- Affichage de l'inventaire ---
    """
    
    Cette méthode affiche le compteur des objets, la case actuelle du joueur et un message si le joueur
    rencontre un mur
                                     
    """
    def affichage(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font, manoir):
        """
    
        Cette méthode affiche le compteur des objets, la case actuelle du joueur et un message si le joueur
        rencontre un mur
                                            
        """
        x_inv = LARGEUR_GRILLE_FIXE
        largeur_inv = max(largeur_fenetre - LARGEUR_GRILLE_FIXE, 200)
        zone = pygame.Rect(x_inv, 0, largeur_inv, hauteur_fenetre)
        pygame.draw.rect(surface, COUL_INVENTAIRE, zone)

        # Position verticale de l'inventaire
        inventaire_y = hauteur_fenetre - 180

        # Titre "Inventaire"
        titre = font.render("Inventaire", True, COUL_TEXTE)
        surface.blit(titre, (x_inv + 20, inventaire_y - 120))

        # Case "Pièce actuelle"
        titre2 = font.render("Pièce actuelle", True, COUL_TEXTE)
        surface.blit(titre2, (x_inv + 130, inventaire_y - 440))

        taille_case = 180
        pos_x_current_pos = x_inv + 100
        pos_y_current_pos = inventaire_y - 400
        joueur_rect = pygame.Rect(pos_x_current_pos, pos_y_current_pos, taille_case, taille_case)
        pygame.draw.rect(surface, (100, 100, 150), joueur_rect)
        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)

        #récupérer la pièce actuelle
        ligne, col = joueur.ligne, joueur.colonne
        piece_actuelle = manoir.grille[ligne][col]

        # --- Afficher l'image de la pièce actuelle ---
        if piece_actuelle is not None:
            room_id = piece_actuelle.id
            if room_id in self.room_images_scaled:
                img = self.room_images_scaled[room_id]
                # Affiche l'image directement dans le carré
                surface.blit(img, joueur_rect.topleft)

        #Affichage du message quand pas de portes 
        if self.message and pygame.time.get_ticks() - self.message_timer < 3000:
            elapsed = pygame.time.get_ticks() - self.message_timer
            if elapsed < 3000:  # moins de 3 secondes
                font_msg = pygame.font.SysFont("arial", 20)
                texte_msg = font_msg.render(self.message, True, (255, 255, 150))  # couleur dorée
                surface.blit(texte_msg, (pos_x_current_pos, pos_y_current_pos + taille_case + 10))
            else:
                self.message = ""  # effacer après 3 secondes

        # Compteurs
        compteur_texte = font.render(str(joueur.footprint), True, COUL_TEXTE)
        x_compteur = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_texte.get_width() - 10
        y_compteur = 68
        surface.blit(compteur_texte, (x_compteur, y_compteur))

        compteur_coins = font.render(str(joueur.coins), True, COUL_TEXTE)
        y_coins = 68 + 1*TAILLE_ICONE + 20   
        surface.blit(compteur_coins, (x_compteur, y_coins))

        compteur_gems = font.render(str(joueur.gems), True, COUL_TEXTE)
        y_gems = 68 + 2*TAILLE_ICONE + 40
        surface.blit(compteur_gems, (x_compteur, y_gems))

        compteur_keys = font.render(str(joueur.keys), True, COUL_TEXTE)
        y_keys = 68 + 3*TAILLE_ICONE + 60
        surface.blit(compteur_keys, (x_compteur, y_keys))

        compteur_dice = font.render(str(joueur.dice), True, COUL_TEXTE)
        y_dice = 68 + 4*TAILLE_ICONE + 80
        surface.blit(compteur_dice, (x_compteur, y_dice))

        # Icônes en haut à droite
        marge_x, marge_y, espace = 20, 60, 20
        for i, img in enumerate(self.images):
            x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
            y = marge_y + i * (TAILLE_ICONE + espace)
            surface.blit(img, (x, y))