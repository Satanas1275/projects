import tkinter as tk
from tkinter import Label, Entry, Button
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random  

rotation_angle = 0  
rotating = False  

def fetch_pokemon():
    global rotation_angle, rotating

    nom_id = entry.get().lower()  
    url = f"https://pokeapi.co/api/v2/pokemon/{nom_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()

        is_shiny = random.random() < 0.10  

        if is_shiny and data['sprites']['front_shiny']:
            image_url = data['sprites']['front_shiny']
            pokedex_label.config(text=f"Nom : {name} (✨ Shiny ✨)", fg="gold")
            shiny_flash_effect()  
        else:
            image_url = data['sprites']['front_default']
            pokedex_label.config(text=f"Nom : {name}", fg="black")
            root.config(bg="white")  

        img_response = requests.get(image_url)
        img_data = Image.open(BytesIO(img_response.content))
        img_data = img_data.resize((150, 150), Image.Resampling.LANCZOS)
        
        img = ImageTk.PhotoImage(img_data)
        pokemon_img_label.config(image=img)
        pokemon_img_label.image = img

        # Démarrer la rotation avec 10% de chance
        if random.random() < 0.10:
            rotation_angle = 0
            rotating = True
            rotate_image(img_data)

    else:
        pokedex_label.config(text="Pokémon introuvable !", fg="red")
        root.config(bg="white")  

def rotate_image(img_data):
    global rotation_angle, rotating

    if not rotating:
        return  

    rotation_angle += 10  
    img_rotated = img_data.rotate(rotation_angle, expand=True)
    img = ImageTk.PhotoImage(img_rotated)

    pokemon_img_label.config(image=img)
    pokemon_img_label.image = img

    if rotation_angle < 360:  
        root.after(50, lambda: rotate_image(img_data))  
    else:
        rotating = False  

def shiny_flash_effect():
    root.config(bg="#FFD700")
    root.after(200, lambda: root.config(bg="white"))
    root.after(400, lambda: root.config(bg="#FFD700"))
    root.after(600, lambda: root.config(bg="white"))
    root.after(800, lambda: root.config(bg="#FFA600"))

root = tk.Tk()
root.title("Pokédex")
root.geometry("300x400")
root.config(bg="white")  

title_label = Label(root, text="Pokédex", font=("Arial", 18, "bold"), bg="white")
title_label.pack(pady=10)

entry = Entry(root, font=("Arial", 14))
entry.pack(pady=5)

search_btn = Button(root, text="Rechercher", font=("Arial", 12), command=fetch_pokemon)
search_btn.pack(pady=5)

pokedex_label = Label(root, text="", font=("Arial", 14), bg="white")
pokedex_label.pack(pady=10)

pokemon_img_label = Label(root, bg="white")
pokemon_img_label.pack(pady=10)

root.mainloop()
