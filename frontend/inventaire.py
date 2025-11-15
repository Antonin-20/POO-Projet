import pygame
import sys
import os
from frontend.constantes import *
from backend.aleatoire_generation_pieces import *
import json

# --- Chargement du JSON pour récupérer toutes les infos des rooms ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)
rooms = data["rooms"]


class Inventaire:
    def __init__(self):
        # --- Icônes joueur ---
        self.images = []
        noms = ["footprint.png", "coins.png", "diamond.png", "key.png", "de.png"]
        for nom in noms:
            chemin = f"assets/Images/icone_inv/{nom}"
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.smoothscale(img, (TAILLE_ICONE,TAILLE_ICONE))
            self.images.append(img)

        # --- Contrôle du choix de salle ---
        self.room_choices = []
        self.room_choice_index = 0
        self.afficher_room_choices = False

        # --- Précharger les images des pièces pour le popup ---
        self.room_images = {}
        taille_popup = 160
        for r in rooms:
            chemin = os.path.join("assets", r["image"])
            if os.path.exists(chemin):
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.smoothscale(img, (taille_popup-10, taille_popup-10))
                self.room_images[r["id"]] = img
        
        self.message = ""
        self.message_timer = 0

        # --- Orientation des pièces tirées dans le popup ---
        self.room_orientations = {}

    # --- Affichage de l'inventaire et du popup ---
    def affichage(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font):
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

        # Popup choix de salle
        if self.afficher_room_choices:
            self.draw_room_choices_window(surface, largeur_fenetre, hauteur_fenetre)

    # --- Popup pour choisir une salle ---
    def draw_room_choices_window(self, surface, largeur_fenetre, hauteur_fenetre):
        w, h = 720, 380
        x = (largeur_fenetre - w) // 2
        y = (hauteur_fenetre - h) // 2

        rect_fenetre = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COUL_MENU, rect_fenetre, border_radius=12)
        pygame.draw.rect(surface, COUL_TEXTE_CYAN, rect_fenetre, 3, border_radius=12)

        font = pygame.font.SysFont("arial", 26)
        titre = font.render("Choisissez une salle :", True, COUL_TEXTE)
        surface.blit(titre, (x + 20, y + 12))

        taille, espace = 160, 45
        total_w = 3 * taille + 2 * espace
        base_x = x + (w - total_w) // 2
        base_y = y + 60

        for i, room_id in enumerate(self.room_choices):
            rect = pygame.Rect(base_x + i * (taille + espace), base_y, taille, taille)
            couleur = (255, 0, 0) if i == self.room_choice_index else COUL_TEXTE_CYAN
            pygame.draw.rect(surface, COUL_CASE, rect, border_radius=8)
            pygame.draw.rect(surface, couleur, rect, 3, border_radius=8)

            # Image de la pièce (sans rotation)
            if room_id in self.room_images:
                img = self.room_images[room_id]
                surface.blit(img, (rect.x + 5, rect.y + 5))

        font_small = pygame.font.SysFont("arial", 18)
        txt = font_small.render("(Q D pour choisir • ESPACE pour valider)", True, COUL_TEXTE_FAIBLE)
        surface.blit(txt, (x + 20, y + h - 30))


    # --- Changer la sélection ---
    def changer_selection(self, direction):
        if direction == "gauche":
            self.room_choice_index = (self.room_choice_index - 1) % 3
        elif direction == "droite":
            self.room_choice_index = (self.room_choice_index + 1) % 3
