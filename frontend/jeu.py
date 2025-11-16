import pygame 
import sys
import os
from .constantes import *
from .joueur import Joueur
from .inventaire import Inventaire
from .popup import Popup
from backend.piece import Piece
from backend.manoir import Manoir
from backend.aleatoire_generation_pieces import *



class Jeu:
    """
    Gère le déroulement global dune partie de Blue Prince.

    Cette classe :
      - initialise la fenêtre, les ressources et les principales entités du jeu
        (joueur, manoir, inventaire, popup),
      - gère les différents états (menu, partie en cours, phase de choix de salle,
        écran de fin),
      - orchestre la boucle principale : gestion des événements, mise à jour
        de létat de jeu et affichage.
    """
    def __init__(self,room_catalog):
        """
        Initialise le jeu, la fenêtre et les entités principales.

            room_catalog : dict ou similaire
            Catalogue des pièces utilisé pour la génération aléatoire et
            l'instanciation du Manoir et de l'inventaire.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Manoir Magique")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)

        # instanciation des classes principales
        self.joueur = Joueur() # objet joueur
        self.inventaire = Inventaire(room_catalog) # objet inventaire
        self.manoir = Manoir(room_catalog) # objet manoir
        self.popup = Popup(self.joueur) # objet popup
       
        self.plein_ecran = False
        self.phase_choix = False  # True quand on choisit une salle dans le popup

        self.message_fin = ""
        self.fin_jeu = False
        self.victoire = False
        #self.room_catalog = room_catalog #on donne cet attribut à la classe simplement pour pouvoir le passer dans creer_nouvelle_pièce
        self.menu_actif = True

        # Index de l'objet sélectionné dans le loot
        self.loot_index = 0

        # Création de la pioche initiale au chargement du jeu
        initialiser_pool() 


    def afficher_menu(self):
        """
        Affiche le menu principal du jeu.

        Comprend :
          - le titre du jeu,
          - un message de bienvenue,
          - les instructions de base,
          - la consigne de démarrage (ESPACE).
        """
        self.screen.fill(COUL_MENU)

        # Titre
        font_titre = pygame.font.SysFont("arial", 70, bold=True)
        titre = font_titre.render("BLUE PRINCE", True, COUL_TEXTE_CYAN)
        self.screen.blit(titre, titre.get_rect(center=(self.screen.get_width()//2, 140)))

        # Sous-titre
        font_texte = pygame.font.SysFont("arial", 28)
        bienvenue = font_texte.render("Bienvenue", True, COUL_TEXTE)
        self.screen.blit(bienvenue, bienvenue.get_rect(center=(self.screen.get_width()//2, 210)))

        # Instructions
        font_instr = pygame.font.SysFont("arial", 22)
        instructions = [
            "Déplacements : Z Q S D",
            "Choisir une porte : Q / D",
            "Valider : ESPACE",
            "But : Atteindre l'Antichambre avant de manquer de pas"
        ]

        for i, texte in enumerate(instructions):
            ligne = font_instr.render(texte, True, COUL_TEXTE_FAIBLE)
            self.screen.blit(ligne, (100, 320 + i * 40))

        # Lancement
        font_start = pygame.font.SysFont("arial", 26, bold=True)
        start = font_start.render("Appuie sur [ESPACE] pour commencer", True, COUL_DORE)
        self.screen.blit(start, start.get_rect(center=(self.screen.get_width()//2, 600)))

        pygame.display.flip()


    
    def verification_fin(self):
        """
        Vérifie si la partie est terminée (victoire ou défaite).

        Conditions :
          - Victoire : le joueur atteint la case de l'Antichambre.
          - Défaite : le joueur n'a plus de pas disponibles (`footprint <= 0`).
        Met à jour les attributs `fin_jeu`, `victoire` et `message_fin`.
        """

        if self.joueur.ligne == NB_LIGNES - 1 and self.joueur.colonne == 2: # Position de l'Antichambre
            self.victoire = True
            self.fin_jeu = True
            self.message_fin = "bravo"

        elif self.joueur.footprint <= 0:
            self.victoire = False
            self.fin_jeu = True
            self.message_fin = "perdu, tu n'as plus de pas"

    def reinitialiser_jeu(self, room_catalog):
        """ A METTRE A JOUR : pas fonctionnel pour le momment : il faut remettre à zéro le pool, le manoir et retirer un pool, un manoir, etc...
        Réinitialise les variables du jeu pour une nouvelle partie.

        room_catalog : dict ou similaire
            Catalogue des pièces utilisé pour réinstancier le Manoir
            et l'Inventaire.

        """
        self.joueur = Joueur()
        self.inventaire = Inventaire(room_catalog)
        self.manoir = Manoir(room_catalog)
        self.popup = Popup(self.joueur)
        initialiser_pool()
        self.menu_actif = True
        self.phase_choix = False
        self.message_fin = ""
        self.fin_jeu = False
        self.victoire = False

    def afficher_message_fin(self):
        """
        Affiche un écran de fin de partie.

        Un overlay semi-transparent est dessiné, puis :
          - le message de fin (`self.message_fin`) est affiché en vert
            (victoire) ou en rouge (défaite),
          - une instruction pour recommencer avec [ESPACE] est affichée.
        """
        # on défini une surface semi-transparente de taille de l'écran (self.screen.get_size() )
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA) # pygame.SRCALPHA pour la transparence

        overlay.fill((0, 0, 0, 180)) # 180 pour l'opacité, plus c'est grand

        # on place la surface semi transparente dans l'écran
        self.screen.blit(overlay, (0, 0))

        font_titre = pygame.font.SysFont("arial", 48, bold=True)
        font_instr = pygame.font.SysFont("arial", 24)

        couleur = (100, 255, 100) if self.victoire else (255, 100, 100)
        texte1 = font_titre.render(self.message_fin, True, couleur)
        texte2 = font_instr.render("Appuyez sur [ESPACE] pour recommencer", True, (255, 255, 255))

        # placement des textes
        rect1 = texte1.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 30))
        rect2 = texte2.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 40))

        self.screen.blit(texte1, rect1)
        self.screen.blit(texte2, rect2)

    def afficher_fenetre_choix(self):
        """
        Affiche une petite fenêtre centrale de choix de salle.

        Affiche :
          - une fenêtre modale centrée,
          - un titre "Choisis une salle",
          - trois cases correspondant aux choix possibles, avec mise en
            évidence de la sélection via `self.inventaire.room_choice_index`.
        """
        largeur, hauteur = self.screen.get_size()
        
        # Taille de la fenêtre
        fenetre_largeur = 400
        fenetre_hauteur = 150
        x_fen = (largeur - fenetre_largeur) // 2
        y_fen = (hauteur - fenetre_hauteur) // 2

        # Fond semi-transparent derrière la fenêtre
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # Fenêtre principale
        fenetre_rect = pygame.Rect(x_fen, y_fen, fenetre_largeur, fenetre_hauteur)
        pygame.draw.rect(self.screen, COUL_MENU, fenetre_rect, border_radius=10)
        pygame.draw.rect(self.screen, COUL_TEXTE, fenetre_rect, 3, border_radius=10)

        # Titre
        font_titre = pygame.font.SysFont("arial", 26, bold=True)
        titre = font_titre.render("Choisis une salle", True, COUL_TEXTE)
        self.screen.blit(titre, (x_fen + 20, y_fen + 10))

        # Les 3 cases
        taille_case = 80
        espace = 25
        base_x = x_fen + 30
        base_y = y_fen + 50

        for i in range(3):
            rect = pygame.Rect(base_x + i*(taille_case + espace), base_y, taille_case, taille_case)
            # couleur selon sélection
            if i == self.inventaire.room_choice_index:
                couleur = COUL_SELECTION
            else:
                couleur = COUL_CHOIX
            pygame.draw.rect(self.screen, couleur, rect, 3, border_radius=8)
            pygame.draw.rect(self.screen, (255,255,255), rect, 2)

    def creer_nouvelle_piece(self,room_catalog,cible_ligne,cible_colonne):
        """
        Tire de nouvelles pièces pour une case cible et active le popup.

        room_catalog : dict ou similaire
            Catalogue des pièces utilisé pour le tirage.
        cible_ligne : int
            Ligne de la case cible où la nouvelle pièce pourra être placée.
        cible_colonne : int
            Colonne de la case cible où la nouvelle pièce pourra être placée.
        """
        # On tire 3 pièces du pool selon les contraintes
        choix = extrait_pool(room_catalog,cible_ligne,cible_colonne)

        # Stockage des 3 pièces tirées dans le popup
        self.popup.room_choices = choix # stocke les 3 pièces
        self.popup.room_choice_index = 0
        self.popup.afficher = True # Pour afficher le popup
        self.phase_choix = True


    def boucle_principale(self, room_catalog):
        """
        Boucle principale du jeu.

        Gère en continu :
          - les événements (clavier, souris, redimensionnement),
          - le menu principal,
          - les déplacements du joueur et la phase de choix de salle,
          - la gestion du loot et du bouton « Redraw »,
          - la vérification des conditions de fin,
          - l'affichage global (manoir, inventaire, popup, écran de fin).
        """
        while True:

            piece_actuelle = self.manoir.grille[self.joueur.ligne][self.joueur.colonne]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # -----------------------------------------
                #                MENU PRINCIPAL
                # -----------------------------------------
                if self.menu_actif:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.menu_actif = False
                    continue

                # -----------------------------------------
                #                FIN DE PARTIE
                # -----------------------------------------
                if self.fin_jeu:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reinitialiser_jeu(room_catalog)
                    continue

                # -----------------------------------------
                #           FULLSCREEN / RESIZE
                # -----------------------------------------
                if event.type == pygame.KEYDOWN: #si il y a un appui sur une touche
                    # Sortie du plein écran
                    if event.key == pygame.K_ESCAPE and self.plein_ecran:
                        self.plein_ecran = False
                        self.screen = pygame.display.set_mode((900, 720), pygame.RESIZABLE)

                    # Passage en plein écran
                    elif event.key == pygame.K_f:
                        self.plein_ecran = True
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

                    # -----------------------------------------
                    #           PHASE NORMALE (déplacement)
                    # -----------------------------------------
                    elif not self.phase_choix:

                        # orientation du joueur
                        #sert pour direction_regard par la suite (dans manoir.py))
                        if event.key == pygame.K_z:
                            self.joueur.orienter("haut")
                        elif event.key == pygame.K_s:
                            self.joueur.orienter("bas")
                        elif event.key == pygame.K_q:
                            self.joueur.orienter("gauche")
                        elif event.key == pygame.K_d:
                            self.joueur.orienter("droite")

                        # entrée en mode CHOIX DE SALLE
                        elif event.key == pygame.K_SPACE:
                            # 1) Calcul de la case cible en fonction de l’orientation
                            cible_ligne = self.joueur.ligne
                            cible_colonne = self.joueur.colonne

                            if self.joueur.orientation == "haut" and self.joueur.ligne < NB_LIGNES - 1:
                                cible_ligne += 1
                            elif self.joueur.orientation == "bas" and self.joueur.ligne > 0:
                                cible_ligne -= 1
                            elif self.joueur.orientation == "gauche" and self.joueur.colonne > 0:
                                cible_colonne -= 1
                            elif self.joueur.orientation == "droite" and self.joueur.colonne < NB_COLONNES - 1:
                                cible_colonne += 1
                            else:
                                # bord de grille
                                self.inventaire.message = "Pas de porte dans cette direction"
                                self.inventaire.message_timer = pygame.time.get_ticks()
                                continue

                            # 2) Vérification de la présence d’une porte dans cette orientation
                            piece_depart = self.manoir.grille[self.joueur.ligne][self.joueur.colonne]
                            if piece_depart is not None:
                                portes_depart = piece_depart.doors
                            else:
                                portes_depart = []

                            # Pièce cible (si elle existe)
                            piece_cible = self.manoir.grille[cible_ligne][cible_colonne]
                            portes_cible = piece_cible.doors if piece_cible else []

                            # Vérification cohérence double porte (porte face à porte opposée)
                            porte_depart = self.joueur.ORIENTATION_TO_DOOR[self.joueur.orientation]
                            opposite = {"N":"S", "S":"N", "E":"W", "W":"E"}
                            porte_arrivee = opposite[porte_depart]

                            # Vérification porte verrouillée
                            if piece_depart.locked_doors.get(porte_depart, 0) == 1:
                                self.inventaire.message = "La porte est verrouillée !"
                                self.inventaire.message_timer = pygame.time.get_ticks()

                                piece_depart.utiliser_cle(porte_depart)
                                joueur.keys -= 1
                                continue

                            # Vérification de la présence des deux portes
                            if porte_depart not in portes_depart or (piece_cible and porte_arrivee not in portes_cible):
                                self.inventaire.message = "Pas de porte dans cette direction !"
                                self.inventaire.message_timer = pygame.time.get_ticks()
                                continue

                            # 3) Traitement de la case cible (occupée ou vide)
                            if piece_cible is not None:
                                # case déjà occupée → déplacement direct
                                self.joueur.deplacer(self.manoir, self.inventaire)
                                self.verification_fin()
                            else:
                                # case vide → créer la nouvelle pièce avec pop-up
                                self.creer_nouvelle_piece(self.manoir.catalog,cible_ligne,cible_colonne)
                                self.verification_fin()


                    # -----------------------------------------
                    #           PHASE CHOIX DE SALLE (popup)
                    # -----------------------------------------
                    else:
                        if event.key == pygame.K_q:
                            self.popup.changer_selection("gauche")

                        elif event.key == pygame.K_d:
                            self.popup.changer_selection("droite")


                        elif event.key == pygame.K_SPACE:
                            # quitter la fenêtre de choix
                            self.phase_choix = False
                            self.popup.afficher = False

                            # mémoriser l’ancienne position (si besoin)
                            ancienne_ligne = self.joueur.ligne
                            ancienne_colonne = self.joueur.colonne

                            # déplacement réel du joueur
                            self.joueur.deplacer(self.manoir, self.inventaire)

                            # --- PLACER LA PIÈCE DANS LA GRILLE COMME INSTANCE ---
                            room_id = self.popup.room_choices[self.popup.room_choice_index]
                            if room_id is not None:
                                #vérifier qu'on n'écrase pas entrée/antichambre
                                if self.manoir.grille[self.joueur.ligne][self.joueur.colonne] is None:
                                    # créer l'instance Piece
                                    pos = (self.joueur.ligne, self.joueur.colonne)
                                    direction = self.joueur.orientation
                                    nouvelle_piece = Piece(room_id, pos, direction,self.joueur.objets_speciaux)

                                    # stocker dans la grille
                                    self.manoir.grille[self.joueur.ligne][self.joueur.colonne] = nouvelle_piece



                            # test de fin
                            self.verification_fin()

                # ----------------- souris -----------------
                if self.phase_choix and self.popup.afficher and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # clic gauche
                        if hasattr(self.popup, "redraw_button_rect"):
                            if self.popup.redraw_button_rect.collidepoint(event.pos):
                                print("Clic souris detecté")
                                if self.joueur.dice > 0:
                                    self.joueur.dice -= 1
                                    # juste mettre à jour les pièces
                                    self.popup.room_choices = extrait_pool(room_catalog,cible_ligne,cible_colonne)
                                    print("Nouvelles pièces :", self.popup.room_choices)
                                    self.popup.room_choice_index = 0
                                else:
                                    self.popup.message_dé = "Pas assez de dés !"
                                    self.popup.message_timer = pygame.time.get_ticks()

                
                # -----------------------------------------
                #       RÉCUPÉRATION D’OBJETS (loot) DE LA PIECE ACTUELLE
                # -----------------------------------------

                if piece_actuelle and piece_actuelle.loot:
            
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_click = pygame.mouse.get_pressed()[0]  # clic gauche

                    zones_loot = self.inventaire.affichage_objet_piece(
                        loot=piece_actuelle.loot,
                        surface=self.screen,
                        joueur=self.joueur,
                        largeur_fenetre=largeur,
                        hauteur_fenetre=hauteur
                    )
                    
                    if mouse_click:
                    
                        for i, rect in enumerate(zones_loot):
                            if rect.collidepoint(mouse_pos):
                                objet = piece_actuelle.loot[i]

                                if objet in ["metal_detector", "lucky_paw", "lockpick"]:
                                    self.joueur.objets_speciaux.append(objet)
                                    print(f"ajout : {self.joueur.objets_speciaux}")
                                elif objet in ["food", "banana", "apple", "cupcake"]:

                                    self.joueur.footprint += 5
                                elif objet in ["gem"]:
                                    self.joueur.gems += 1
                                elif objet in ["die"]:
                                    self.joueur.dice += 1
                                elif objet in ["coin"]:
                                    self.joueur.coins += 1
                                elif objet == "key":
                                    self.joueur.keys += 1

                                piece_actuelle.loot.pop(i)
                                self.loot_index = 0
                                break


                # -----------------------------------------
                #         REDIMENSIONNEMENT DE FENÊTRE
                # -----------------------------------------
                if event.type == pygame.VIDEORESIZE and not self.plein_ecran:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # -----------------------------------------
            #              AFFICHAGE GLOBAL
            # -----------------------------------------

            if self.menu_actif:
                self.afficher_menu()
            else:#on est plus dans le menu
                largeur, hauteur = self.screen.get_size()
                self.screen.fill(COUL_FOND)

                # manoir centré verticalement
                self.manoir.ajout_piece(self.screen, self.joueur, 0, 0)

                # inventaire à droite
                self.inventaire.affichage(self.screen, self.joueur, largeur, hauteur, self.font, self.manoir)

                # Affichage des objets contenus dans la pièce actuelle du joueur
                piece_actuelle = self.manoir.grille[self.joueur.ligne][self.joueur.colonne]
                if piece_actuelle: # On vérifie si on est dans une pièce au cas ou
                    self.inventaire.affichage_objet_piece(
                        loot=piece_actuelle.loot,
                        surface=self.screen,
                        joueur=self.joueur,
                        largeur_fenetre=largeur,
                        hauteur_fenetre=hauteur
                    
                    )
        
                # --- Affichage du popup si actif ---
                if self.popup.afficher:
                    self.popup.affichage_popup(self.screen, largeur, hauteur)
                
                # fenêtre de fin
                if self.fin_jeu:
                    self.afficher_message_fin()

                pygame.display.flip()

            self.clock.tick(30)
