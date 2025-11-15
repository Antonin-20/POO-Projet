import json, random, os

"""chaque niveau de rareté divise par 3 la proba de tirer une pièce
On décide de tirer une rareté de pièce (tirage pondéré), puis de tirer une pièce au hasard avec la même proba parmis toutes les pièces de même rareté
la fonction choix_pièce() permet de retourner le nom de la pièce à ajouter
"""


BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")

with open(json_path, encoding="utf-8") as f: #on charge le .json
    data = json.load(f)

rooms = data["rooms"]

def tirer_rarete():            #pour tirer l'indice de rareté de la pièce
    valeurs = [0, 1, 2, 3]
    poids = [1, 1/3, 1/9, 1/27]
    return random.choices(valeurs, weights=poids, k=1)[0]

rooms_zeros = []
rooms_one = []
rooms_two = []
rooms_three = []

for r in rooms:
    if r['rarity'] == 0 :
        rooms_zeros += [r['id']]
    if r['rarity'] == 1:
        rooms_one += [r['id']]
    if r['rarity'] == 2:
        rooms_two += [r['id']]
    if r['rarity'] == 3:
        rooms_three += [r['id']]

def choix_pièce():
    r = tirer_rarete()
    if r == 0:
        pièce_choisie = random.choice(rooms_zeros)
    if r == 1:
        pièce_choisie = random.choice(rooms_one)
    if r == 2:
        pièce_choisie = random.choice(rooms_two)
    if r == 3:
        pièce_choisie = random.choice(rooms_three)
    return pièce_choisie

POOL = []  #on le place ici pour pouvoir appeler la fonciton depuis ailleurs, inventaire.py par exemple

def pool():
    """création du 'Pool' (pioche) de pièces pour le manoir à l'initialisation du jeu. Ne s'exécute qu'une fois par partie.

    Returns:
        list: liste des pièces de la pioche
    """

    n = 43             #nombre de pièces totales dans le pool pour le manoir, fixe a priori
    for i in range(n):
        POOL.append(choix_pièce())
    return POOL

def initialiser_pool():
    """Crée la pioche initiale, stockée dans la variable globale POOL au sein de aleatoire_generation_pieces.py"""
    global POOL
    POOL = pool()  
    print(POOL)

def extrait_pool():
    """sert à obtenir les 3 pièces aléatires du pool lors du choix du joueur. Contient toutes les contraites possibles 
    (pour l'instant, juste que les pièces soient différentes entre elles).
    """
    global POOL
    choix = random.sample(list(set(POOL)), 3) #on s'assure que les 3 pièces soient différentes

    return choix

def retirer_piece_du_pool(piece_id):
    """Retirer la pièce choisie du pool."""
    global POOL
    if piece_id in POOL:
        POOL.remove(piece_id)

def remettre_pieces_dans_pool(pieces):
    """Remettre les pièces non choisies dans le pool."""
    global POOL
    POOL += pieces
