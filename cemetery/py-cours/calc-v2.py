import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculatrice")
        master.configure(bg="#1e1e1e")  # Couleur de fond de la fenêtre

        self.result = tk.StringVar()

        # Champ d'entrée pour le résultat
        self.entry = tk.Entry(master, textvariable=self.result, font=('Arial', 28), bd=10, insertwidth=2, width=14, borderwidth=4, justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.entry.config(bg="#ffffff", fg="#000000")  # Couleur de fond et texte du champ

        # Boutons de la calculatrice avec couleurs et styles
        buttons = [
            ('7', '#ffa500'), ('8', '#ffa500'), ('9', '#ffa500'), ('/', '#ff4500'),
            ('4', '#ffa500'), ('5', '#ffa500'), ('6', '#ffa500'), ('*', '#ff4500'),
            ('1', '#ffa500'), ('2', '#ffa500'), ('3', '#ffa500'), ('-', '#ff4500'),
            ('0', '#ffa500'), ('.', '#ffa500'), ('+', '#ff4500'), ('=', '#32cd32'),
        ]

        row_val = 1
        column_val = 0
        for (text, color) in buttons:
            self.create_button(text, color, row_val, column_val)
            column_val += 1
            if column_val > 3:
                column_val = 0
                row_val += 1

        clear_button = tk.Button(master, text='C', padx=87, pady=20, command=self.clear, bg='#ff6347', fg='white', font=('Arial', 20, 'bold'))
        clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_button(self, text, color, row, column):
        button = tk.Button(self.master, text=text, padx=20, pady=20, command=lambda: self.on_button_click(text), bg=color, fg='black', font=('Arial', 20, 'bold'), relief='raised', bd=3)
        button.grid(row=row, column=column, padx=5, pady=5)
        button.config(activebackground="#ffeb3b")  # Couleur de fond lors du survol

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
    root.geometry("430x600")  # Dimension de la fenêtre
    calculator = Calculator(root)
    root.mainloop()
