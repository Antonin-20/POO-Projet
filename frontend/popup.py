import pygame
import os
import json
from .constantes import *

# --- Chargement du JSON pour récupérer toutes les infos des rooms ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)
rooms = data["rooms"]

class Popup:
    """Affichage du tirage des 3 pièces après avoir confirmé un déplacement."""

    def __init__(self):
        """
        room_images : dict {room_id: surface pygame} déjà chargées à la bonne taille
        """

        # --- Précharger les images des pièces pour le popup ---
        self.room_images = {}
        taille_popup = 160
        for r in rooms:
            chemin = os.path.join("assets", r["image"])
            if os.path.exists(chemin):
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.smoothscale(img, (taille_popup-10, taille_popup-10))
                self.room_images[r["id"]] = img

        # Liste des 3 pièces tirées
        self.room_choices = []

        # Index de la pièce actuellement sélectionnée dans le popup (0, 1 ou 2)
        self.room_choice_index = 0

        # Si True → le popup doit être affiché et les inputs Q/D/ESPACE le contrôlent
        self.afficher = False

        # valeur temporaire du bouton redraw
        self.redraw_button_rect = pygame.Rect(0, 0, 0, 0) 

   

    # --- Changer la sélection avec Q/D ---
    def changer_selection(self, direction: str):
        """direction = 'gauche' ou 'droite'"""
        if not self.room_choices:
            return

        if direction == "gauche":
            self.room_choice_index = (self.room_choice_index - 1) % len(self.room_choices)
        elif direction == "droite":
            self.room_choice_index = (self.room_choice_index + 1) % len(self.room_choices)

    # --- Dessiner la fenêtre de choix ---
    def affichage_popup(self, surface, largeur_fenetre, hauteur_fenetre):
        """Affiche le popup si self.afficher est True."""
        if not self.afficher:
            return  # on ne dessine rien
        else :
            # Taille popup
            w, h = 720, 380
            x = (largeur_fenetre - w) // 2
            y = (hauteur_fenetre - h) // 2

            # Fond semi-transparent derrière
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            surface.blit(overlay, (0, 0))

            # Fenêtre principale
            rect_fenetre = pygame.Rect(x, y, w, h)
            pygame.draw.rect(surface, COUL_MENU, rect_fenetre, border_radius=12)
            pygame.draw.rect(surface, COUL_TEXTE_CYAN, rect_fenetre, 3, border_radius=12)

            font = pygame.font.SysFont("arial", 26)
            titre = font.render("Choisissez une salle :", True, COUL_TEXTE)
            surface.blit(titre, (x + 20, y + 12))

            # Cases pour les 3 pièces
            taille, espace = 160, 45
            total_w = 3 * taille + 2 * espace
            base_x = x + (w - total_w) // 2
            base_y = y + 60

            for i, room_id in enumerate(self.room_choices):
                rect = pygame.Rect(base_x + i * (taille + espace), base_y, taille, taille)
                # couleur du contour selon la sélection
                couleur = (255, 0, 0) if i == self.room_choice_index else COUL_TEXTE_CYAN

                pygame.draw.rect(surface, COUL_CASE, rect, border_radius=8)
                pygame.draw.rect(surface, couleur, rect, 3, border_radius=8)

                # Image de la pièce
                if room_id in self.room_images:
                    img = self.room_images[room_id]
                    img_x = rect.x + (rect.width - img.get_width()) // 2
                    img_y = rect.y + (rect.height - img.get_height()) // 2
                    surface.blit(img, (img_x, img_y))

        # Petit texte d'aide
        font_small = pygame.font.SysFont("arial", 18)
        txt_aide = font_small.render("(Q / D pour choisir • ESPACE pour valider)", True, COUL_TEXTE_FAIBLE)
        surface.blit(txt_aide, (x + 20, y + h - 30))

        # --- BOUTON REDRAW ---
        bouton_largeur = 160
        bouton_hauteur = 40
        bx = x + w - bouton_largeur - 30   # à droite dans le popup
        by = y + h - bouton_hauteur - 30   # en bas du popup
        

        font = pygame.font.SysFont("arial", 28, bold=True)
        txt_redraw = font.render("Redraw", True, (255, 255, 255))
        
        # Stocker le Rect avec la taille du texte
        self.redraw_button_rect = pygame.Rect(bx, by, bouton_largeur, bouton_hauteur)
    
        
        # Centrer le texte dans le Rect si tu veux
        txt_rect = txt_redraw.get_rect(center=self.redraw_button_rect.center)
        pygame.draw.rect(surface, (50, 50, 100), self.redraw_button_rect)  # fond du bouton
        surface.blit(txt_redraw, txt_rect)