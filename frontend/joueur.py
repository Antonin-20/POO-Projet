import pygame
import sys
import os
from frontend.constantes import *


class Joueur:
    def __init__(self, ligne=0, colonne=2):
        self.ligne = ligne
        self.colonne = colonne
        self.orientation = "haut"

        self.footprint = 70
        self.coins = 0
        self.gems = 2
        self.keys = 0
        self.dice = 0


        

    def orienter(self, direction):
        self.orientation = direction
        

    ORIENTATION_TO_DOOR = {
    "haut": "N",
    "bas": "S",
    "gauche": "W",
    "droite": "E"
    }

    def deplacer(self, manoir, inventaire):
        ancienne_pos = (self.ligne, self.colonne)

        piece = manoir.grille[self.ligne][self.colonne]
        if piece is None:
            return
        salle_id = piece.id
        portes = piece.doors        #chaque pièce a son attribut "doors"

        porte = self.ORIENTATION_TO_DOOR[self.orientation]

        if porte not in portes:
            inventaire.message = "Pas de porte dans cette direction !"
            inventaire.message_timer = pygame.time.get_ticks()
            return  # la porte dans cette direction n'existe pas
        
        # Réinitialiser le message si le déplacement est possible
        inventaire.message = ""

        if self.orientation == "haut" and self.ligne < NB_LIGNES - 1: #cette condition évite de sortir de la grille
            self.ligne += 1
        elif self.orientation == "bas" and self.ligne > 0:
            self.ligne -= 1
        elif self.orientation == "gauche" and self.colonne > 0:
            self.colonne -= 1
        elif self.orientation == "droite" and self.colonne < NB_COLONNES - 1:
            self.colonne += 1

        if (self.ligne, self.colonne) != ancienne_pos:
            self.footprint = max(0, self.footprint - 1)