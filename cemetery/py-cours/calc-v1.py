import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculatrice")

        self.result = tk.StringVar()

        # Champ d'entrée pour le résultat
        self.entry = tk.Entry(master, textvariable=self.result, font=('Arial', 16), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=4)

        # Boutons de la calculatrice
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ]

        for (text, row, column) in buttons:
            self.create_button(text, row, column)

        clear_button = tk.Button(master, text='C', padx=39, pady=20, command=self.clear)
        clear_button.grid(row=5, column=0, columnspan=2)

    def create_button(self, text, row, column):
        button = tk.Button(self.master, text=text, padx=20, pady=20, command=lambda: self.on_button_click(text))
        button.grid(row=row, column=column)

    def on_button_click(self, char):
        if char == '=':
            try:
                self.result.set(eval(self.result.get()))
            except Exception as e:
                self.result.set("Erreur")
        else:
            current_text = self.result.get()
            self.result.set(current_text + char)

    def clear(self):
        self.result.set("")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
