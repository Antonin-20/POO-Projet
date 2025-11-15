import json
import os

def charger_catalogue():
    """permet de récupérer les données contenues dans le catalogue de pièces en .json afin de l'exploiter dans le reste du programme, sans passer par main.py
    Returns:
        dict: catalogue des pièces
    """
    backend_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(backend_dir)

    path_json = os.path.join(project_root, "assets", "Data", "room_catalog.json")

    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {room["id"]: room for room in data["rooms"]}
