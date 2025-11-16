from frontend import Jeu
from backend.loader import charger_catalogue

room_catalog = charger_catalogue()
if __name__ == "__main__":
    Jeu(room_catalog).boucle_principale(room_catalog)