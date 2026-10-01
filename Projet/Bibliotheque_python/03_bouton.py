import tkinter as tk


fenetre = tk.Tk()
fenetre.title("Ma bibliothèque")
fenetre.geometry("800x600")

bouton = tk.Button(
    fenetre,
    text="Bonjour"
)

bouton.pack()

fenetre.mainloop()