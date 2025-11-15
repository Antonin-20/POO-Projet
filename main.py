from frontend import Jeu
import json
import os


def charger_catalogue():
    """Cette fonction a pour but d'accéder au catalogue de pièces stocké dans le fichier .json, pour le mettre sous la forme d'un dictionnaire 
    et le rendre accessible au reste  du programme, notamment à la classe Manoir qui en a besoin pour générer ses pièces selon les propriétés de chaque type de pièce. 

    Returns:
        dict: dictionnaire contenant en clé l'id de chaque pièce et en valeur les propriétés de ladite pièce.
    """
    base_path = os.path.dirname(os.path.abspath(__file__)) #chemin abs main.py
    catalogue_path = os.path.join(base_path, "assets", "Data", "room_catalog.json")
    with open(catalogue_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {room["id"]: room for room in data["rooms"]}


if __name__ == "__main__":       #lance la boucle de jeu quand on démarre le programme
    Jeu(charger_catalogue()).boucle_principale()