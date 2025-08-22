import random

# Fonction pour afficher le plateau de jeu
def afficher_plateau(plateau):
    for ligne in plateau:
        print(" | ".join(ligne))
        print("-" * 9)

# Fonction pour vérifier si un joueur a gagné
def verifier_victoire(plateau, joueur):
    # Vérifier les lignes, colonnes et diagonales
    for i in range(3):
        if all([case == joueur for case in plateau[i]]):  # Vérifie les lignes
            return True
        if all([plateau[j][i] == joueur for j in range(3)]):  # Vérifie les colonnes
            return True
    if plateau[0][0] == plateau[1][1] == plateau[2][2] == joueur:  # Diagonale 1
        return True
    if plateau[0][2] == plateau[1][1] == plateau[2][0] == joueur:  # Diagonale 2
        return True
    return False

# Fonction pour vérifier si le plateau est plein
def plateau_plein(plateau):
    return all([case != " " for ligne in plateau for case in ligne])

# Fonction pour demander le coup d'un joueur humain
def demander_coup(joueur):
    while True:
        try:
            ligne = int(input(f"Joueur {joueur}, entrez la ligne (1-3) : ")) - 1
            colonne = int(input(f"Joueur {joueur}, entrez la colonne (1-3) : ")) - 1
            if ligne in range(3) and colonne in range(3):
                return ligne, colonne
            else:
                print("Veuillez entrer un numéro de ligne et de colonne valide (1 à 3).")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

# Fonction pour faire jouer l'IA
def coup_ia(plateau):
    while True:
        ligne = random.randint(0, 2)
        colonne = random.randint(0, 2)
        if plateau[ligne][colonne] == " ":
            return ligne, colonne

# Fonction principale du jeu
def morpion():
    # Initialiser le plateau
    plateau = [[" " for _ in range(3)] for _ in range(3)]
    
    # Choisir le mode de jeu
    mode = input("Voulez-vous jouer à 2 joueurs (tapez '2') ou contre l'IA (tapez '1') ? ")
    
    joueurs = ["X", "O"]
    joueur_actuel = 0
    
    while True:
        afficher_plateau(plateau)
        
        # Choisir le coup selon le mode de jeu
        if mode == "2" or (mode == "1" and joueur_actuel == 0):
            ligne, colonne = demander_coup(joueurs[joueur_actuel])
        elif mode == "1" and joueur_actuel == 1:
            print("L'IA est en train de jouer...")
            ligne, colonne = coup_ia(plateau)
        
        # Vérifier si la case est libre
        if plateau[ligne][colonne] == " ":
            plateau[ligne][colonne] = joueurs[joueur_actuel]
            
            # Vérifier si le joueur a gagné
            if verifier_victoire(plateau, joueurs[joueur_actuel]):
                afficher_plateau(plateau)
                print(f"Le joueur {joueurs[joueur_actuel]} a gagné !")
                break
            
            # Vérifier si le plateau est plein
            if plateau_plein(plateau):
                afficher_plateau(plateau)
                print("Match nul !")
                break
            
            # Changer de joueur
            joueur_actuel = 1 - joueur_actuel
        else:
            print("Cette case est déjà occupée. Essayez de nouveau.")

# Lancer le jeu
morpion()
