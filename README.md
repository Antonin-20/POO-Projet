# README.md

# Projet Blue Prince

Le projet Blue Prince est une reproduction simplifiée en 2 dimensions du jeu vidéo Blue Prince, développé par Dogubomb et publié en avir 2025.

## Prérequis

- Python 3.11.9
- [Pygame](https://www.pygame.org/news)

## Installation

1. Créer un environnement virtuel (optionnel mais recommandé) :  
   ```bash
   python3 -m venv env
   source env/bin/activate   # Linux / macOS
   env\Scripts\activate      # Windows
   ```

2. Installe les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```

## Lancer le jeu

```bash
python main.py
```

## Commandes

- Déplacer le personnage : Z/Q/S/D
- Interagir avec les objets : touche E (ou autre)
- Ramasser un objet dans une pièce et reroll : clic souris

## Structure du projet

- `main.py` : point d’entrée du jeu  
- `frontend/` : classes Jeu, Joueur, Inventaire et Popup  
- `backend/` : classes Manoir, Piece, mécanique de génération aléatoire de pièces et loader pour accéder à la base de données
- `assets/` : images et base de donnée du jeu  
- `requirements.txt` : dépendances Python

## Auteur

Zeno Amann, Jordan Reyes et Antonin Pelletier
