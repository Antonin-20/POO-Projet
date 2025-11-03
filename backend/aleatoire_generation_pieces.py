import json, random, os

"""chaque niveau de rareté divise par 3 la proba de tirer une pièce
On décide de tirer une rareté de pièce (tirage pondéré), puis de tirer une pièce au hasard avec la même proba parmis toutes les pièces de même rareté
"""


BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
json_path = os.path.join(BASE_DIR, "assets", "Data", "room_catalog.json")

with open(json_path, encoding="utf-8") as f: #on charge le .json
    data = json.load(f)

rooms = data["rooms"]


def tirer_rarete(p):            #pour tirer l'indice de rareté de la pièce
    valeurs = [0, 1, 2, 3]
    poids = [p, p/3, p/9, p/27]
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

print(rooms_zeros)
print(rooms_one)
print(rooms_two)
print(rooms_three)


# degre_rarete_choisi = random.choice(raretes)
