def est_dans_la_liste(parfum, liste_parfums):
    if parfum in liste_parfums:
        return f"Le parfum '{parfum}' est dans la liste."
    else:
        return f"Le parfum '{parfum}' n'est pas dans la liste."

def est_pair_ou_impair(nombre):
    if nombre % 2 == 0:
        return f"Le nombre {nombre} est pair."
    else:
        return f"Le nombre {nombre} est impair."

parfums = ['vanille', 'fraise', 'chocolat', 'menthe', 'citron']

choix = input("Voulez-vous vérifier un parfum ou un nombre ? (Entrez '1' pour parfum ou '2' pour nombre) : ")

if choix == '1':
    parfum_utilisateur = input("Entrez un parfum : ")
    print(est_dans_la_liste(parfum_utilisateur, parfums))
elif choix == '2':
    nombre_utilisateur = int(input("Entrez un nombre : "))
    print(est_pair_ou_impair(nombre_utilisateur))
else:
    print("Choix invalide. Veuillez entrer '1' ou '2'.")
