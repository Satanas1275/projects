import random

class Voiture:
    def __init__(self, nom, marque, modele):
        self.nom = nom  # exemple : "Voiture 1"
        self.marque = marque
        self.modele = modele
        self.vitesse = 0
        self.pv = 100  # points de vie

    def accelerer(self, valeur):
        self.vitesse += valeur
        print(f"{self.nom} accélère à {self.vitesse} km/h.")

    def freiner(self):
        if self.vitesse > 0:
            self.vitesse -= 10
            print(f"{self.nom} freine à {self.vitesse} km/h.")
        else:
            print(f"{self.nom} est déjà à l'arrêt.")

    def info(self):
        print(f"{self.nom} - {self.marque} {self.modele}, vitesse: {self.vitesse} km/h, PV: {self.pv}")

    def accident(self, autre_voiture):
        if self.vitesse > 20 and autre_voiture.vitesse > 20:
            degats = random.randint(10, 50)
            self.pv -= degats
            autre_voiture.pv -= degats
            print(f"💥 ACCIDENT entre {self.nom} et {autre_voiture.nom} !")
            print(f"Chacune perd {degats} PV.")
        else:
            print("Pas assez de vitesse pour un accident grave.")

        # Vérification de l’état des voitures
        if self.pv <= 0:
            print(f"❌ {self.nom} est détruite !")
        if autre_voiture.pv <= 0:
            print(f"❌ {autre_voiture.nom} est détruite !")
