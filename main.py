from frontend import Jeu
from backend.loader import charger_catalogue

if __name__ == "__main__":
    Jeu(charger_catalogue()).boucle_principale()
