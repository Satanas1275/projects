def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Erreur: Division par zéro."
    return x / y

def calculator():
    print("Sélectionnez l'opération :")
    print("1. Addition")
    print("2. Soustraction")
    print("3. Multiplication")
    print("4. Division")

    while True:
        choice = input("Entrez le numéro de l'opération (1/2/3/4) : ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Entrez le premier nombre : "))
            num2 = float(input("Entrez le deuxième nombre : "))

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"{num1} / {num2} = {divide(num1, num2)}")
        else:
            print("Choix invalide.")

        next_calculation = input("Voulez-vous faire un autre calcul ? (oui/non) : ")
        if next_calculation.lower() != 'oui':
            break

if __name__ == "__main__":
    calculator()
