from backend.loader import charger_catalogue

ROOM_CATALOG = charger_catalogue() #on récupère le catalogue des pièces depuis le loader

#print(ROOM_CATALOG["kitchen"]["doors"]) #je me garde un exemple d'accès aux données du catalogue, ne pas suppr tt de suite svp

class Piece :
    def __init__(self, id_piece: str, position: tuple[int, int], direction_regard: str):
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
        self.doors = self.calculer_portes_orientees()  #on modifie les portes selon l'orientation
        self.placement = ROOM_CATALOG[self.id]["placement"] 
        self.loot = ROOM_CATALOG[self.id]["loot"] 
    
    def calculer_portes_orientees(self):
            """Renvoie la liste des portes pivotées selon l'orientation de la pièce."""
            if not self.doors: #on s'assure qu'il y ait des portes dans la pièce
                return []
            rotation_map = {0:0, 90:1, 180:2, 270:3}  #nb de quarts de tour
            nb_quarts = rotation_map.get(self.orientation, 0)

            directions = ["N", "E", "S", "W"]
            portes_orientees = []
            for d in self.doors:
                idx = directions.index(d)
                new_idx = (idx + nb_quarts) % 4
                portes_orientees.append(directions[new_idx])
            return portes_orientees
    
    def which_locked_door(self):
        """Fonction à implémenter : prend en entrée la liste des portes de la pièce et la position de la pièce, renvoie une liste de taille identique à celle de la pièce originale*
        pour indiquer l'état de chaque porte. Ex : ["N","S"] ---> [1,0] si la porte Nord est verrouillée et la porte Sud déverrouillée.  
        """
        self.locked_door = None

    def contenu_piece(self):
        """Fonction à implémenter : renvoie le contenu de la pièce (pièces, nourriture, clés) à partir des données du catalogue (self.loot)
        """
        self.contenu = None

