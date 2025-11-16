import json
import pygame
import os
from frontend.constantes import *


class PopupKey:

    """
    Classe représentant un popup de confirmation pour l'utilisation d'une clé.

    Attributs :
        joueur (Joueur) : instance du joueur courant.
        afficher (bool) : indique si le popup doit être affiché.
        selection (int) : option sélectionnée, 0 = Oui, 1 = Non.
        message_timer (int) : timestamp pour gérer l'affichage temporaire des messages.
        message_duration (int) : durée d'affichage des messages en millisecondes.
    """

    def __init__(self, joueur):

        """
        Initialise le popup pour l'utilisation de clé.

        Args:
            joueur (Joueur) : instance du joueur qui va utiliser la clé.

        """
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

        """
        Change la sélection du popup

        Args:
            direction (str) : "gauche", "droite", "haut", ou "bas".
        
        """
        if direction == "gauche" or direction == "haut":
            self.selection = (self.selection - 1) % 2
        elif direction == "droite" or direction == "bas":
            self.selection = (self.selection + 1) % 2

    def affichage_popup_key(self, surface, largeur_fenetre, hauteur_fenetre, joueur):

        """
        Affiche le popup de confirmation pour utiliser une clé.

        Args:
            surface (pygame.Surface) : surface sur laquelle dessiner le popup.
            largeur_fenetre (int) : largeur de la fenêtre.
            hauteur_fenetre (int) : hauteur de la fenêtre.
            joueur (Joueur) : instance du joueur, utilisée pour les informations si nécessaire.
        """
        
        if not self.afficher:
            return

        # Dimensions et position
        w, h = 400, 200
        x, y = (largeur_fenetre - w)//2, (hauteur_fenetre - h)//2

        # Fond semi-transparent
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        # Fenêtre principale
        rect_fenetre = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COUL_MENU, rect_fenetre, border_radius=10)
        pygame.draw.rect(surface, COUL_TEXTE_CYAN, rect_fenetre, 3, border_radius=10)

        # Titre
        font = pygame.font.SysFont("arial", 24)
        titre = font.render("Voulez-vous utiliser une clé ?", True, COUL_TEXTE)
        surface.blit(titre, (x + 20, y + 20))

        # Texte du coût
        font_cout = pygame.font.SysFont("arial", 20)
        texte_cout = font_cout.render("Coût : x1 clé", True, COUL_TEXTE_FAIBLE)
        surface.blit(texte_cout, (x + 20, y + 60))

        # Options Oui / Non
        font_opt = pygame.font.SysFont("arial", 28, bold=True)
        oui_couleur = (255, 0, 0) if self.selection == 0 else COUL_TEXTE
        non_couleur = (255, 0, 0) if self.selection == 1 else COUL_TEXTE
        txt_oui = font_opt.render("Oui", True, oui_couleur)
        txt_non = font_opt.render("Non", True, non_couleur)
        surface.blit(txt_oui, (x + 100, y + 150))
        surface.blit(txt_non, (x + 250, y + 150))
