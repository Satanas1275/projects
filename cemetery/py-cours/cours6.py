def calcul_interet_compose(Moisrestant, somme):
    # Condition de base : Si aucun mois restant, retourner la somme actuelle
    if Moisrestant == 0:
        return somme
    else:
        # Intérêts ajoutés pour ce mois, appel récursif pour les mois restants
        print("Pour les mois restant ", Moisrestant, ", la somme est de ", somme, "€")
        return calcul_interet_compose(Moisrestant - 1, somme * 1.10)

# Exemple d'utilisation
somme_initiale = 1000  # Capital initial
duree = 3  # Nombre de mois

resultat = calcul_interet_compose(duree, somme_initiale)
print(f"Montant total après {duree} mois : {resultat}")
