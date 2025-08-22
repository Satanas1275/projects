class Voiture:
     def __init__(self, nbr_portes, vitesse_moteur, type, couleur ):
          self.nbr_Phares = 2
          self.nbrRoue = 4
          self.nbr_portes = nbr_portes
          self.vitesse_moteur = vitesse_moteur
          self.type = type
          self.couleur = couleur
          
vt1 = Voiture("12", "300km/h", "volkswagen", "rouge")
print(vt1.nbr_portes)