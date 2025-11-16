from backend.loader import charger_catalogue
from typing import Tuple
import random

ROOM_CATALOG = charger_catalogue() #on récupère le catalogue des pièces depuis le loader

#print(ROOM_CATALOG["kitchen"]["doors"]) #je me garde un exemple d'accès aux données du catalogue, ne pas suppr tt de suite svp

class Piece :
    def __init__(self, id_piece: str, position: Tuple[int, int], direction_regard: str):
        """Classe permettant de créer une instance de pièce lors du dessin.

        Args:
            id_piece (str): nom de la pièce choisie par l'utilisateur (parmis les 3 sorties du pool pour lui)
            position (tuple[int, int]): coordonnées (x,y) de la pièce dans la grille du manoir
            direction_regard (str): position du regard du joueur lors du choix de la pièce ('haut','bas','gauche','droite') pour en déduire l'orientation de cette dernière, en degrés.
        """
        self.id = id_piece
        self.position = position  # (x, y) coordonnées dans la grille du manoir

        if direction_regard == 'haut':
            self.orientation = 0
        elif direction_regard == 'gauche':
            self.orientation = 90
        elif direction_regard == 'bas':
            self.orientation = 180
        elif direction_regard == 'droite':
            self.orientation = 270

    #on met dans cette instance toutes les infos de la pièce depuis le catalogue
        self.name = ROOM_CATALOG[self.id]["name"]
        self.color = ROOM_CATALOG[self.id]["color"]
        self.rarity = ROOM_CATALOG[self.id]["rarity"]
        self.gem_cost = ROOM_CATALOG[self.id]["gem_cost"]
        self.image_path = ROOM_CATALOG[self.id]["image"]
        self.doors = ROOM_CATALOG[self.id]["doors"]
        #print(f"Portes avant orientation de la pièce {self.id} : {self.doors}")
        self.doors = self.calculer_portes_orientees()  #on modifie les portes selon l'orientation
        #print(f"Portes après orientation de la pièce {self.id} : {self.doors}")
        self.placement = ROOM_CATALOG[self.id]["placement"] 
        self.loot_table = ROOM_CATALOG[self.id]["loot"] 
        #print(f"Table de loot de la pièce {self.id} : {self.loot_table}")
        self.loot = self.generer_loot() #on génère le loot de la pièce à sa création
        #print(f"Loot généré pour la pièce {self.id} : {self.loot}")
    
    def calculer_portes_orientees(self):
            """Renvoie la liste des portes pivotées selon l'orientation de la pièce."""
            if not self.doors:                          #on s'assure qu'il y ait des portes dans la pièce
                return []
            rotation_map = {0:0, 90:1, 180:2, 270:3}  #nb de quarts de tour à effectuer selon l'angle de la pièce
            nb_quarts = rotation_map[self.orientation]

            directions = ["N", "E", "S", "W"]
            portes_orientees = []
            for d in self.doors:
                idx = directions.index(d)
                new_idx = (idx - nb_quarts) % 4                 #att au -, nécessaire car pygame fait des rotations hraires
                portes_orientees.append(directions[new_idx])
            return portes_orientees
    
    def which_locked_door(self):
        """Fonction à implémenter : prend en entrée la liste des portes de la pièce et la position de la pièce, renvoie une liste de taille identique à celle de la pièce originale*
        pour indiquer l'état de chaque porte. Ex : ["N","S"] ---> [1,0] si la porte Nord est verrouillée et la porte Sud déverrouillée.  
        """
        self.locked_door = None


    def generer_loot(self):

        resultat = []
        if not self.loot_table:   #pour les 2 pièces de début et toute pièce sans llot
            return []
        
        table = self.loot_table[0]
        print("table:",table)

        # -----------------------------
        # CAS 1 : LOOT DE TYPE "POOL"
        # -----------------------------
        if table.get("type") == "pool":

            items = table["items"]
            take = table["take"]

            # Construire la liste des candidats
            candidats = []

            for item in items:
                qty = item.get("qty", 1)

                if isinstance(qty, dict):
                    # quantité min/max aléatoire
                    n = random.randint(qty.get("min", 1), qty.get("max", 1))
                else:
                    n = qty

                # Ajouter n fois l'ID à la liste des candidats
                candidats.extend([item["id"]] * n)

            # Tirage aléatoire de "take" éléments
            tirage = random.sample(candidats, min(take, len(candidats)))
            resultat.extend(tirage)

            return resultat

        # --------------------------------------
        # CAS 2 : LOOT PROBABILISTE SIMPLE
        # --------------------------------------
        else:
            for item in self.loot_table:
                qty = item.get("qty", 1)

                if isinstance(qty, dict):
                    n = random.randint(qty.get("min", 1), qty.get("max", 1))
                else:
                    n = qty

                # On fait "n" tirages indépendants avec probabilité p
                p = item.get("p", 1)
                for _ in range(n):
                    if random.random() < p:
                        resultat.append(item["id"])

            return resultat
