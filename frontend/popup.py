import pygame
import os
import json
from .constantes import *
from frontend.joueur import Joueur

# Chargement du JSON pour récupérer toutes les infos des rooms 
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")
with open(json_path, encoding="utf-8") as f:
    data = json.load(f)
rooms = data["rooms"]

class Popup:
    """
    Gère la fenêtre de tirage et de sélection des pièces après un déplacement.

    Cette classe :
      - précharge les images des pièces à la bonne taille pour l'affichage du tirage,
      - affiche un popup avec jusqu'à trois choix de salles,
      - permet de changer la sélection via Q/D et de la valider via ESPACE,
      - gère le bouton « Redraw » lié au nombre de dés du joueur,
      - affiche un message d'erreur temporaire si le joueur n'a plus de dés.
    """

    def __init__(self, joueur):
        """
        Initialise le popup et précharge les ressources graphiques.

        Instance du joueur utilisée notamment pour connaître le nombre
        de dés disponibles pour le bouton « Redraw ».

        room_images : dict {room_id: surface pygame} déjà chargées à la bonne taille
        """
        self.joueur = joueur
        # Précharger les images des pièces pour le popup 
        self.room_images = {}
        taille_popup = 160

        for r in rooms:
            chemin = os.path.join("assets", r["image"])
            if os.path.exists(chemin):
                img = pygame.image.load(chemin).convert_alpha()
                img = pygame.transform.smoothscale(img, (taille_popup-10, taille_popup-10))
                self.room_images[r["id"]] = img
        
       # On récupère l'image dé pour l'afficher dans le popup
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
        image_de_path = os.path.join(BASE_DIR, "assets", "Images", "de.png")

        # Charger et redimensionner l'image
        self.image_de = pygame.transform.smoothscale(
            pygame.image.load(image_de_path).convert_alpha(), (40, 40))

        # Liste des 3 pièces tirées
        self.room_choices = []

        # Index de la pièce actuellement sélectionnée dans le popup (0, 1 ou 2)
        self.room_choice_index = 0

        # Si True → le popup doit être affiché et les inputs Q/D/ESPACE le contrôlent
        self.afficher = False

        # valeur temporaire du bouton redraw
        self.redraw_button_rect = pygame.Rect(0, 0, 0, 0) 

        self.message_dé = ""
        self.message_timer = 0     # timestamp pour faire disparaître le message
        self.message_duration = 1000  # durée en ms (2s)

    def changer_selection(self, direction: str):
        """
        Change la sélection courante parmi les pièces tirées avec Q/D.

        direction : str
            Sens de la navigation : "gauche" ou "droite".
        """
        if not self.room_choices:
            return

        if direction == "gauche":
            self.room_choice_index = (self.room_choice_index - 1) % len(self.room_choices)
        elif direction == "droite":
            self.room_choice_index = (self.room_choice_index + 1) % len(self.room_choices)


    def affichage_popup(self, surface, largeur_fenetre, hauteur_fenetre):
        """
        Affiche la fenêtre de choix des pièces si `self.afficher` est True.

        Le popup :
          - assombrit l'arrière-plan,
          - affiche les 3 pièces tirées avec surbrillance sur la sélection,
          - affiche le bouton « Redraw » avec survol à la souris,
          - affiche l'icône du dé et le compteur de dés du joueur,
          - affiche un message d'erreur temporaire si le joueur n'a plus de dés.
        """
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

        # Vérifier si la souris est dessus
        souris_pos = pygame.mouse.get_pos()
        survol = self.redraw_button_rect.collidepoint(souris_pos)

        # Couleur et épaisseur du contour selon survol
        couleur_bord = (255, 255, 255) if survol else (0, 0, 0)
        epaisseur_bord = 4 if survol else 2
    
        
        # Centrer le texte dans le Rect 
        txt_rect = txt_redraw.get_rect(center=self.redraw_button_rect.center)
        pygame.draw.rect(surface, (50, 50, 100), self.redraw_button_rect)  # fond du bouton
        pygame.draw.rect(surface, couleur_bord, self.redraw_button_rect, epaisseur_bord)  # bordure
        surface.blit(txt_redraw, txt_rect)



        # --- AFFICHAGE DÉ ET DE SON COMPTEUR ---
        # Position du dé à gauche du bouton Redraw
        de_margin = 10
        de_x = self.redraw_button_rect.left - self.image_de.get_width() - de_margin
        de_y = self.redraw_button_rect.top + (self.redraw_button_rect.height - self.image_de.get_height()) // 2
        surface.blit(self.image_de, (de_x, de_y))

        # Afficher le nombre compteur de dés du joueur
        font = pygame.font.SysFont("arial", 24, bold=True)
        texte_de = font.render(str(self.joueur.dice), True, (255, 255, 255))
        # position à droite de l’image
        texte_x = de_x + self.image_de.get_width() - 60
        texte_y = de_y + (self.image_de.get_height() - texte_de.get_height()) // 2
        surface.blit(texte_de, (texte_x, texte_y))

        # ------ AFFICHAGE MESSAGE SI PLUS DE dÉS ------
        if self.message_dé:
        # disparaît après self.message_duration ms
            if pygame.time.get_ticks() - self.message_timer < self.message_duration:
                font_msg = pygame.font.SysFont("arial", 20, bold=True)
                txt_msg = font_msg.render(self.message_dé, True, (255, 50, 50))
                # Centrer sous le bouton Redraw
                txt_rect = txt_msg.get_rect(center=(self.redraw_button_rect.centerx, self.redraw_button_rect.top - 20))
                surface.blit(txt_msg, txt_rect)
            else:
                self.message_dé = ""  # effacer après le temps écoulé