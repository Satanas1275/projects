from PIL import Image

glaces_liste = ["chocolat", "pistache", "phraise", "vanille"]

def first():
    while True:
        choice = input("Choisissez un parfum ou tapez 'help' : ").lower()
        if choice == 'quitter':
            print("Fin du programme.")
            break

        elif choice == 'liste' :
            for parfum in glaces_liste:
                print(parfum)

        elif choice == 'help' :
                print("liste = affiche la liste \n<nom d'un parfum> affichez le nom du parfum choisie (ci le parfum n'exsite pas... tkt) et ne choisicez SURTOUT PAS PISTACHE !!!")

        elif choice not in glaces_liste:
            print("Ce parfum n'existe pas...")

        elif choice =='pistache':
            print("nan mais serieux ?!")
            print("Ne revien jamais !!!!!!!!!!!!!")
            Image.open("tkt.jpeg").show()
            break

        else:
            print(f"Vous avez choisi : {choice}")

if __name__ == "__main__":
    first()
