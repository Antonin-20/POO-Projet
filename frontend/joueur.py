import pygame
import sys
import os
from frontend.constantes import *


class Joueur:
    def __init__(self, ligne=0, colonne=2):
        self.ligne = ligne
        self.colonne = colonne
        self.orientation = "haut"
        self.footprint = 2

    def orienter(self, direction):
        self.orientation = direction

    def deplacer(self):
        ancienne_pos = (self.ligne, self.colonne)
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