import json
import pygame
import os
from frontend.constantes import *


class PopupKey:

    def __init__(self, joueur):
        self.joueur = joueur
        self.afficher = False
        self.selection = 0  # 0 = Oui, 1 = Non
        self.message_timer = 0
        self.message_duration = 1000

        # Charger l'image de la clé
        cle_path = os.path.join("assets", "Images", "key.png")
        if os.path.exists(cle_path):
            self.image_cle = pygame.transform.smoothscale(
                pygame.image.load(cle_path).convert_alpha(), (50, 50)
            )
        else:
            self.image_cle = None

    def changer_selection_key(self, direction: str):
        if direction == "gauche" or direction == "haut":
            self.selection = (self.selection - 1) % 2
        elif direction == "droite" or direction == "bas":
            self.selection = (self.selection + 1) % 2

    def affichage_popup_key(self, surface, largeur_fenetre, hauteur_fenetre, joueur):
        if not self.afficher:
            return

        # Fenêtre
        w, h = 400, 200
        x, y = (largeur_fenetre - w)//2, (hauteur_fenetre - h)//2

        # Fond semi-transparent
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,120))
        surface.blit(overlay, (0,0))

        # Fenêtre principale
        rect_fenetre = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COUL_MENU, rect_fenetre, border_radius=10)
        pygame.draw.rect(surface, COUL_TEXTE_CYAN, rect_fenetre, 3, border_radius=10)

        font = pygame.font.SysFont("arial", 24)
        titre = font.render("Voulez-vous utiliser une clé ?", True, COUL_TEXTE)
        surface.blit(titre, (x + 20, y + 20))

        # Icône clé + compteur
        if self.image_cle:
            surface.blit(self.image_cle, (x + 20, y + 70))
        font_compteur = pygame.font.SysFont("arial", 22)
        compteur = font_compteur.render(f"x {self.joueur.keys}", True, COUL_TEXTE)
        surface.blit(compteur, (x + 80, y + 80))

        # Options Oui / Non
        font_opt = pygame.font.SysFont("arial", 28, bold=True)
        oui_couleur = (255,0,0) if self.selection == 0 else COUL_TEXTE
        non_couleur = (255,0,0) if self.selection == 1 else COUL_TEXTE
        txt_oui = font_opt.render("Oui", True, oui_couleur)
        txt_non = font_opt.render("Non", True, non_couleur)

        surface.blit(txt_oui, (x + 100, y + 150))
        surface.blit(txt_non, (x + 250, y + 150))

    
    


