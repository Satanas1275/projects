import tkinter as tk
import random

bleu = "#064789"
blancBleu = '#D1FAFF'
greyBleu ="#9BD1E5"
doré = "#FFF07C"
listecouleur = [bleu, blancBleu, greyBleu, doré , "red" , "black"]

window = tk.Tk()
window.geometry('500x500')
window.title("Interface Tkinter")
window.config(bg=greyBleu)



titrePrincipale = tk.Label(window, text="Bonjour Tkinter !", font=("Arial", 25) , bg=bleu , fg=doré)
titrePrincipale.pack(padx=50 , pady=50)
# titrePrincipale2 = tk.Label(window, text="Bonjour Tkinter !", font=("Arial", 25))
# titrePrincipale2.pack(padx=50 , pady=10)

# cette focntion doit changer le le titre pricnipale en fonction du contenue
# de l'ENTRY
def clique():
    réponse = entry.get()
    titrePrincipale.config(text=réponse)
    chiffreCouleur = random.randint(0,listecouleur.__len__()-1)
    chiffreCouleur2 = random.randint(0,listecouleur.__len__()-1)
    titrePrincipale.config(text=réponse , bg=listecouleur[chiffreCouleur] , fg=listecouleur[chiffreCouleur2])
    chiffreCouleurWindows = random.randint(0,listecouleur.__len__()-1)
    window.config(bg=listecouleur[chiffreCouleurWindows])
    # else:
    #     titrePrincipale2.config(text=réponse)
    


## ENTRY

entry = tk.Entry(window, font=("Arial", 20) , bg=blancBleu)
entry.pack(pady=75)

# text = tk.Text(window, height=5, width=40, font=("Arial", 12))
# text.pack(pady=10)

premierBoutton = tk.Button(window  , text="tu peux cliquer ! " , command=clique ,font=("Arial", 20)  , bg = blancBleu )
premierBoutton.pack(pady=60)

window.mainloop()