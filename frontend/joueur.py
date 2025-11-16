from backend import piece
import pygame
import sys
import os
from frontend.constantes import *



class Joueur:
    """
    Représente le joueur dans le manoir.

    Cette classe gère :
      - la position du joueur sur la grille (ligne, colonne),
      - son orientation actuelle,
      - ses ressources (empreintes, pièces, gemmes, clés, dés),
      - la pièce où il se trouve,
      - et le déplacement du joueur en tenant compte des portes disponibles.

    Le déplacement réduit la ressource "footprint" d’une unité à chaque
    mouvement réussi.
    """



    def __init__(self, ligne=0, colonne=2):
        """
        Initialise le joueur à une position et orientation données.

        ligne : int
            Ligne initiale du joueur dans la grille du manoir.
        colonne : int
            Colonne initiale du joueur dans la grille du manoir.
        """
        self.ligne = ligne
        self.colonne = colonne
        self.orientation = "haut"

        # Ressources du joueur
        self.footprint = 70
        self.coins = 0
        self.gems = 2

        self.keys = 0
        self.dice = 10

        self.objets_speciaux = ["lockpick"]


    def orienter(self, direction):
        """
        Change l’orientation du joueur.

        direction : str
            Nouvelle orientation ("haut", "bas", "gauche", "droite").
        """
        self.orientation = direction
        
    # Correspondance orientation → direction cardinale des portes
    ORIENTATION_TO_DOOR = {
    "haut": "N",
    "bas": "S",
    "gauche": "W",
    "droite": "E"
    }

    

    def deplacer(self, manoir, inventaire):
        """
        Tente de déplacer le joueur dans la direction où il est orienté.

        Le déplacement nest possible que si :
          - la pièce courante possède une porte dans cette direction,
          - la case visée se situe dans les limites de la grille.

        En cas dabsence de porte, un message temporaire est envoyé à
        l'inventaire. En cas de déplacement réussi, la ressource
        `footprint` est réduite de 1.

        manoir : Manoir
            Instance du manoir contenant la grille des pièces.
        inventaire : Inventaire
            Instance de linventaire utilisée pour afficher les messages.
        """
        ancienne_pos = (self.ligne, self.colonne)

        # Récupération de la pièce actuelle
        from backend.piece import Piece                 #on le met ici pour éviter les problèmes d'import circulaire
        piece = manoir.grille[self.ligne][self.colonne]
        if piece is None:
            return
        salle_id = piece.id
        portes = piece.doors        #chaque pièce a son attribut "doors"

        porte = self.ORIENTATION_TO_DOOR[self.orientation]

        # Vérifier l’existence d’une porte dans cette direction
        if porte not in portes:
            inventaire.message = "Pas de porte dans cette direction !"
            inventaire.message_timer = pygame.time.get_ticks()
            return  # la porte dans cette direction n'existe pas
        
        # Message vide si le déplacement est possible
        inventaire.message = ""

        # deplacement en considerant les bordures de la grille
        if self.orientation == "haut" and self.ligne < NB_LIGNES - 1: #cette condition évite de sortir de la grille
            self.ligne += 1
        elif self.orientation == "bas" and self.ligne > 0:
            self.ligne -= 1
        elif self.orientation == "gauche" and self.colonne > 0:
            self.colonne -= 1
        elif self.orientation == "droite" and self.colonne < NB_COLONNES - 1:
            self.colonne += 1

        # Décrément de la ressource footprint si déplacement réussi
        if (self.ligne, self.colonne) != ancienne_pos:
            self.footprint = max(0, self.footprint - 1)