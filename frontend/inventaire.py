import pygame
import sys
import os
from frontend.constantes import *

class Inventaire:
    def __init__(self):
        self.images = []
        noms = ["footprint.png", "coins.png", "diamond.png", "key.png", "de.png"]
        for nom in noms:
            chemin = f"assets/Images/icone_inv/{nom}"
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.smoothscale(img, (TAILLE_ICONE, TAILLE_ICONE))
            self.images.append(img)

        # Contrôle des choix
        self.afficher_room_choices = False
        self.room_choice_index = 0  # sélection actuelle

    

    def affichage(self, surface, joueur, largeur_fenetre, hauteur_fenetre, font):
        x_inv = LARGEUR_GRILLE_FIXE
        largeur_inv = max(largeur_fenetre - LARGEUR_GRILLE_FIXE, 200)
        zone = pygame.Rect(x_inv, 0, largeur_inv, hauteur_fenetre)
        pygame.draw.rect(surface, COUL_INVENTAIRE, zone)

         # --- Inventaire en bas ---
        # Position verticale de l'inventaire (en bas mais avec marge)
        inventaire_y = hauteur_fenetre - 180  # 180 px du bas, tu peux ajuster
            
        # Titre "Inventaire"
        titre = font.render("Inventaire", True, COUL_TEXTE)
        surface.blit(titre, (x_inv + 20, inventaire_y - 120))

        # Rectangle pour la position actuelle du joueur / pièce
        titre2 = font.render("Pièce actuelle", True, COUL_TEXTE)
        surface.blit(titre2, (x_inv + 130, inventaire_y - 440))

        # Case plus grande
        taille_case = 180  # augmente la taille
        pos_x = x_inv + 100
        pos_y = inventaire_y - 400
        joueur_rect = pygame.Rect(pos_x, pos_y, taille_case, taille_case)
        pygame.draw.rect(surface, (100, 100, 150), joueur_rect)  # couleur temporaire
        pygame.draw.rect(surface, (255, 255, 255), joueur_rect, 3)  # bordure blanche


        #Compteur de pas pour chaque déplacement
        compteur_texte = font.render(str(joueur.footprint), True, COUL_TEXTE)
        x_compteur = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_texte.get_width() - 10
        y_compteur = 68
        surface.blit(compteur_texte, (x_compteur, y_compteur))

        # Compteur de coins
        compteur_coins = font.render(str(joueur.coins), True, COUL_TEXTE)
        x_coins = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_coins.get_width() - 10
        y_coins = 68 + 1*TAILLE_ICONE + 20   
        surface.blit(compteur_coins, (x_coins, y_coins)) 

        # Compteur de gemmes
        compteur_gems = font.render(str(joueur.gems), True, COUL_TEXTE)
        x_gems = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_gems.get_width() - 10
        y_gems = 68 + 2*TAILLE_ICONE + 40
        surface.blit(compteur_gems, (x_gems, y_gems))

        # Compteur de keys
        compteur_keys = font.render(str(joueur.keys), True, COUL_TEXTE)
        x_keys = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_keys.get_width() - 10
        y_keys = 68 + 3*TAILLE_ICONE + 60
        surface.blit(compteur_keys, (x_keys, y_keys))

        # Compteur de dice
        compteur_dice = font.render(str(joueur.dice), True, COUL_TEXTE)
        x_dice = x_inv + largeur_inv - TAILLE_ICONE - 20 - compteur_dice.get_width() - 10
        y_dice = 68 + 4*TAILLE_ICONE + 80
        surface.blit(compteur_dice, (x_dice, y_dice))

        # Affichage des icônes
        marge_x, marge_y, espace = 20, 60, 20
        # for i, img in enumerate(self.images):
        #     x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
        #     y = marge_y + i * (TAILLE_ICONE + espace)
        #     surface.blit(img, (x, y))

        # Affichage des icônes en haut à droite
        for i in range(len(self.images)):
            x = x_inv + largeur_inv - TAILLE_ICONE - marge_x
            y = marge_y + i * (TAILLE_ICONE + espace)
            surface.blit(self.images[i], (x, y))

        if self.afficher_room_choices:
            self.draw_room_choices_window(surface, largeur_fenetre, hauteur_fenetre)

    def draw_room_choices_window(self, surface, largeur_fenetre, hauteur_fenetre):
        """Affiche une vraie fenêtre popup centrée pour choisir une salle."""

        # --- Taille et position ---
        w = 720
        h = 380
        x = (largeur_fenetre - w) // 2
        y = (hauteur_fenetre - h) // 2

        # --- Fenêtre ---
        rect_fenetre = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COUL_MENU, rect_fenetre, border_radius=12)
        pygame.draw.rect(surface, COUL_TEXTE_CYAN, rect_fenetre, 3, border_radius=12)

        # --- Titre ---
        font = pygame.font.SysFont("arial", 26)
        titre = font.render("Choisissez une salle :", True, COUL_TEXTE)
        surface.blit(titre, (x + 20, y + 12))

        # --- Cases de choix ---
        taille = 160
        espace = 45
        total_w = 3 * taille + 2 * espace
        base_x = x + (w - total_w) // 2
        base_y = y + 60

        for i in range(3):
            rect = pygame.Rect(base_x + i * (taille + espace), base_y, taille, taille)

            couleur = (255, 0, 0) if i == self.room_choice_index else COUL_TEXTE_CYAN

            pygame.draw.rect(surface, COUL_CASE, rect, border_radius=8)
            pygame.draw.rect(surface, couleur, rect, 3, border_radius=8)

        # --- Indication ---
        font_small = pygame.font.SysFont("arial", 18)
        txt = font_small.render("(Q D pour choisir • ESPACE pour valider)", True, COUL_TEXTE_FAIBLE)
        surface.blit(txt, (x + 20, y + h - 30))

    # Permet de choisir une salle avec les flèches gauche/droite
    def changer_selection(self, direction):
        """Change la sélection (gauche/droite)"""
        if direction == "gauche":
            self.room_choice_index = (self.room_choice_index - 1) % 3
        elif direction == "droite":
            self.room_choice_index = (self.room_choice_index + 1) % 3