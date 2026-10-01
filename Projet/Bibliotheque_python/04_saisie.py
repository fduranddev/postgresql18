fenetre = tk.Tk()
fenetre.title("Ma bibliothèque")
fenetre.geometry("800x600")

recherche = tk.Entry(fenetre)
texte = recherche.get()
recherche.pack()

fenetre.mainloop()