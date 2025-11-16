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

    """
    Dessine l'inventaire (icônes + compteurs + pièce actuelle) sur la surface de jeu.
    fonctionalités : 
      - charger et mettre à l'échelle les icônes de ressources du joueur
      - affichager et mettre a jour les comptueurs de l'inventaire (cles, gemmes etc...)
      - précharger les images des pièces à la bonne taille pour l'affichage « Pièce actuelle »,
      - mémoriser et d'afficher un message de warning (a court de portes dans cette direction)
    """

    def __init__(self, room_catalog):

        """
            Initialise l'inventaire et précharge les ressources graphiques.

            Parametres:
            room_catalog : iterable
                Catalogue des pièces du manoir (par exemple la liste globale
                `rooms`). Chaque élément doit au minimum contenir :
                - une clé ``"id"`` : identifiant unique de la pièce,
                - une clé ``"image"`` : chemin relatif vers le fichier image
                    de la pièce (depuis ``assets/``).

            Bonus:
            - Les icônes de ressources du joueur (empreintes, pièces, gemmes,
            clés, dé) sont chargées depuis ``assets/Images/icone_inv/`` et
            redimensionnées à ``TAILLE_ICONE``.
            - Les images de pièces sont redimensionnées une seule fois à
            ``self.taille_case_piece`` pour optimiser l'affichage.
        """

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
        self.message_duration = 1000  # durée en ms (1s)

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

        self.objets_speciaux = []



    # --- Affichage de l'inventaire ---

    def affichage(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font, manoir):
        """
    
        Cette méthode affiche le compteur des objets, la case actuelle du joueur et un message si le joueur est a court de portes 
                                            
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

        # Titre "Contenu"
        titre1 = font.render("Contenu", True, COUL_TEXTE)
        surface.blit(titre1, (900 - 150 , inventaire_y - 120))

        # Case "Pièce actuelle"
        titre2 = font.render("Pièce actuelle", True, COUL_TEXTE)
        surface.blit(titre2, (x_inv + 130, inventaire_y - 440))

        # affichage des objets spéciaux en dessous de l'inventaire
        y_special = hauteur_fenetre - 260
        espacement_special = 30
        font = pygame.font.SysFont("arial", 18)

        for i, obj in enumerate(self.objets_speciaux):
            texte_surface = font.render(obj, True, COUL_TEXTE)
            surface.blit(texte_surface, (x_inv + 20, y_special + i * espacement_special))

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

        #Affichage du message quand pas de portes dispo
        if self.message and pygame.time.get_ticks() - self.message_timer < self.message_duration:
            elapsed = pygame.time.get_ticks() - self.message_timer
            if elapsed < 3000:  # moins de 3 secondes
                font_msg = pygame.font.SysFont("arial", 20)
                texte_msg = font_msg.render(self.message, True, (255, 255, 150))  # couleur dorée
                surface.blit(texte_msg, (pos_x_current_pos, pos_y_current_pos + taille_case + 10))
            else:
                self.message = ""  # effacer après 3 secondes

        # Compteurs : contenu + display  
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

        # Icônes associés aux compteurs en haut à droite
        marge_x, marge_y, espace = 20, 60, 20
        for i, img in enumerate(self.images):
            x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
            y = marge_y + i * (TAILLE_ICONE + espace)
            surface.blit(img, (x, y))

    def affichage_objet_piece(self, loot, surface, joueur, largeur_fenetre, hauteur_fenetre):
        """Méthode qui affiche les objets présents dans la pièce actuelle du joueur.
        Args:
            loot (list): liste des objets présents dans la pièce actuelle
            surface (pygame.Surface): surface sur laquelle dessiner
            joueur (Joueur): instance du joueur
            largeur_fenetre (int): largeur de la fenêtre
            hauteur_fenetre (int): hauteur de la fenêtre
            font (pygame.font.Font): police pour le texte
        """

        zones_loot = []  # liste de pygame.Rect correspondant à chaque objet


        if not loot:
            # afficher un message "Aucun objet dans cette pièce"
            return
        
        else:
            
            x_position = largeur_fenetre - 150
            y_position = hauteur_fenetre - 260
            espacement = 30
            font = pygame.font.SysFont("arial", 18)
            

            for i, obj in enumerate(loot):
                texte_surface = font.render(obj, True, COUL_TEXTE)
                rect = texte_surface.get_rect(topleft=(x_position, y_position + i * espacement))
                surface.blit(texte_surface, rect.topleft)
                zones_loot.append(rect)
        return zones_loot
    