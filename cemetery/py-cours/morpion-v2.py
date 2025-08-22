import tkinter as tk
import random

print("Miaou !")

# Fonction pour vérifier si un joueur a gagné
def verifier_victoire(plateau, joueur):
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

# Fonction pour faire jouer l'IA en fonction du niveau choisi
def coup_ia():
    if niveau_difficulte == "facile":
        return coup_ia_facile()
    elif niveau_difficulte == "moyen":
        return coup_ia_moyen()
    else:  # Difficulté difficile
        return coup_ia_difficile()

# IA facile : joue aléatoirement
def coup_ia_facile():
    coups_possibles = [(i, j) for i in range(3) for j in range(3) if plateau[i][j] == " "]
    return random.choice(coups_possibles)

# IA moyenne : mélange de coups aléatoires et intelligents
def coup_ia_moyen():
    if random.random() < 0.5:  # 50% de chances de jouer intelligemment
        return coup_ia_difficile()
    else:
        return coup_ia_facile()

# IA difficile : utilise l'algorithme Minimax
def coup_ia_difficile():
    meilleur_score = -float('inf')
    meilleur_coup = None
    for i in range(3):
        for j in range(3):
            if plateau[i][j] == " ":
                plateau[i][j] = "O"  # L'IA joue en tant que "O"
                score = minimax(plateau, 0, False)
                plateau[i][j] = " "
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = (i, j)
    return meilleur_coup

# Algorithme Minimax
def minimax(plateau, profondeur, is_maximizing):
    if verifier_victoire(plateau, "O"):  # Si l'IA gagne
        return 1
    elif verifier_victoire(plateau, "X"):  # Si le joueur humain gagne
        return -1
    elif plateau_plein(plateau):  # Match nul
        return 0

    if is_maximizing:
        meilleur_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == " ":
                    plateau[i][j] = "O"
                    score = minimax(plateau, profondeur + 1, False)
                    plateau[i][j] = " "
                    meilleur_score = max(score, meilleur_score)
        return meilleur_score
    else:
        meilleur_score = float('inf')
        for i in range(3):
            for j in range(3):
                if plateau[i][j] == " ":
                    plateau[i][j] = "X"
                    score = minimax(plateau, profondeur + 1, True)
                    plateau[i][j] = " "
                    meilleur_score = min(score, meilleur_score)
        return meilleur_score

# Fonction pour gérer le clic d'une case
def clic(ligne, colonne):
    global joueur_actuel, mode

    if cases[ligne][colonne]["text"] == " ":
        # Jouer le coup du joueur actuel
        cases[ligne][colonne]["text"] = joueur_actuel
        plateau[ligne][colonne] = joueur_actuel
        
        # Ajouter les couleurs pour chaque joueur
        if joueur_actuel == "X":
            cases[ligne][colonne].config(fg="blue")  # Croix en bleu
        else:
            cases[ligne][colonne].config(fg="red")  # Rond en rouge

        # Vérifier victoire ou match nul
        if verifier_victoire(plateau, joueur_actuel):
            afficher_plateau()
            message_label.config(text=f"Le joueur {joueur_actuel} a gagné !")
            return
        elif plateau_plein(plateau):
            afficher_plateau()
            message_label.config(text="Match nul !")
            return

        # Passer au tour de l'autre joueur ou de l'IA
        joueur_actuel = "O" if joueur_actuel == "X" else "X"
        
        if mode == "IA" and joueur_actuel == "O":
            ligne, colonne = coup_ia()
            clic(ligne, colonne)

# Fonction pour réinitialiser le plateau
def reinitialiser_plateau():
    global plateau, joueur_actuel
    plateau = [[" " for _ in range(3)] for _ in range(3)]
    joueur_actuel = "X"
    for i in range(3):
        for j in range(3):
            cases[i][j]["text"] = " "
            cases[i][j].config(fg="black")  # Réinitialise la couleur en noir
    message_label.config(text="C'est au tour de X")

# Fonction pour choisir le mode de jeu
def choisir_mode():
    global mode
    mode = "IA" if mode_var.get() == 1 else "2 joueurs"
    reinitialiser_plateau()
    
# Fonction pour choisir le niveau de difficulté
def choisir_difficulte():
    global niveau_difficulte
    niveau_difficulte = "facile" if difficulty_var.get() == 1 else "moyen" if difficulty_var.get() == 2 else "difficile"
    reinitialiser_plateau()

# Fonction pour afficher le plateau dans le terminal (facultatif)
def afficher_plateau():
    for ligne in plateau:
        print(ligne)

# Initialisation du plateau
plateau = [[" " for _ in range(3)] for _ in range(3)]
joueur_actuel = "X"
mode = "2 joueurs"  # Mode de jeu par défaut
niveau_difficulte = "difficile"  # Difficulté par défaut

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Morpion")

# Création d'une barre de menu
menu_bar = tk.Menu(fenetre)
fenetre.config(menu=menu_bar)

# Menu Mode de jeu
mode_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Mode", menu=mode_menu)
mode_var = tk.IntVar()
mode_menu.add_radiobutton(label="Jouer contre l'IA", variable=mode_var, value=1, command=choisir_mode)
mode_menu.add_radiobutton(label="Deux joueurs", variable=mode_var, value=2, command=choisir_mode)

# Menu Difficulté
difficulty_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Difficulté", menu=difficulty_menu)
difficulty_var = tk.IntVar()
difficulty_menu.add_radiobutton(label="Facile", variable=difficulty_var, value=1, command=choisir_difficulte)
difficulty_menu.add_radiobutton(label="Moyen", variable=difficulty_var, value=2, command=choisir_difficulte)
difficulty_menu.add_radiobutton(label="Difficile", variable=difficulty_var, value=3, command=choisir_difficulte)

# Étiquette pour afficher les messages de victoire ou de match nul
message_label = tk.Label(fenetre, text="C'est au tour de X", font=('Arial', 16))
message_label.grid(row=4, columnspan=3)

# Création des boutons pour représenter les cases du plateau
cases = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        cases[i][j] = tk.Button(fenetre, text=" ", font=('Arial', 40), width=5, height=2,
                                command=lambda i=i, j=j: clic(i, j))
        cases[i][j].grid(row=i, column=j)

# Bouton pour réinitialiser le plateau
reset_button = tk.Button(fenetre, text="Réinitialiser", font=('Arial', 16), command=reinitialiser_plateau)
reset_button.grid(row=5, columnspan=3)

# Lancer la boucle principale de Tkinter
fenetre.mainloop()
