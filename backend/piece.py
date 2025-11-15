from backend.loader import charger_catalogue

ROOM_CATALOG = charger_catalogue() #on récupère le catalogue des pièces depuis le loader

# Exemple d’accès
print(ROOM_CATALOG["kitchen"]["doors"])



class Piece :
    def __init__(self, id_piece: str, position: tuple[int, int], direction_regard: str):
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
        self.placement = ROOM_CATALOG[self.id]["placement"]
        self.loot = ROOM_CATALOG[self.id]["loot"]
    
    def which_locked_door(self):
        """Fonction à implémenter : prend en entrée la liste des portes de la pièce et la position de la pièce, renvoie une liste de taille identique à celle de la pièce originale*
        pour indiquer l'état de chaque porte. Ex : ["N","S"] ---> [1,0] si la porte Nord est verrouillée et la porte Sud déverrouillée.  
        """
        self.locked_door = None

