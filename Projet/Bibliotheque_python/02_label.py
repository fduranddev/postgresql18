import tkinter as tk


fenetre = tk.Tk()
fenetre.title("Ma bibliothèque")
fenetre.geometry("800x600")

titre = tk.Label(
    fenetre,
    text="Ma bibliothèque personnelle"
)
titre.pack()

fenetre.mainloop()