import os
import subprocess
import sys
import tkinter as tk

from tkinter import ttk, messagebox

from database.connection import get_connection
from database import queries


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(
            "Bibliothèque personnelle"
        )
        self.geometry(
            "1250x760"
        )
        self.minsize(
            1000,
            650
        )
        self._build_ui()
        self.refresh_books()


    # ========================================================
    # INTERFACE PRINCIPALE
    # ========================================================

    def _build_ui(self)
    
        top = ttk.Frame(
            self,
            padding=10
        )

        top.pack(
            fill="x"
        )


        ttk.Label(
            top,
            text="Recherche :"
        ).pack(
            side="left"
        )


        self.search_var = tk.StringVar()


        search = ttk.Entry(
            top,
            textvariable=self.search_var,
            width=45
        )

        search.pack(
            side="left",
            padx=8
        )


        search.bind(
            "<Return>",
            lambda event: self.refresh_books()
        )


        ttk.Button(
            top,
            text="Rechercher",
            command=self.refresh_books
        ).pack(
            side="left"
        )


        ttk.Button(
            top,
            text="Tous les livres",
            command=self.clear_search
        ).pack(
            side="left",
            padx=6
        )


        ttk.Button(
            top,
            text="Tester la connexion",
            command=self.test_connection
        ).pack(
            side="right"
        )


        # ----------------------------------------------------
        # TABLE DES LIVRES
        # ----------------------------------------------------

        columns = (
            "id",
            "titre",
            "auteurs",
            "categories",
            "editeurs",
            "annee",
            "pages",
            "exemplaires",
            "emplacements"
        )


        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse"
        )


        headings = {

            "id": "ID",
            "titre": "Titre",
            "auteurs": "Auteurs",
            "categories": "Catégories",
            "editeurs": "Éditeurs",
            "annee": "Parution",
            "pages": "Pages",
            "exemplaires": "Ex.",
            "emplacements": "Emplacement(s)"
        }


        widths = {

            "id": 55,
            "titre": 220,
            "auteurs": 180,
            "categories": 210,
            "editeurs": 150,
            "annee": 80,
            "pages": 70,
            "exemplaires": 55,
            "emplacements": 180
        }


        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="w"
            )


        self.tree.pack(
            fill="both",
            expand=True,
            padx=10
        )


        self.tree.bind(
            "<Double-1>",
            lambda event: self.show_selected()
        )


        # ----------------------------------------------------
        # BOUTONS
        # ----------------------------------------------------

        bottom = ttk.Frame(
            self,
            padding=10
        )

        bottom.pack(
            fill="x"
        )


        ttk.Button(
            bottom,
            text="Voir la fiche",
            command=self.show_selected
        ).pack(
            side="left"
        )


        ttk.Button(
            bottom,
            text="Ouvrir le PDF",
            command=self.open_pdf
        ).pack(
            side="left",
            padx=6
        )


        self.status = tk.StringVar(
            value="Prêt"
        )


        ttk.Label(
            bottom,
            textvariable=self.status
        ).pack(
            side="right"
        )


    # ========================================================
    # RECHERCHE
    # ========================================================

    def clear_search(self):

        self.search_var.set("")

        self.refresh_books()


    def get_rows(self):

        search = self.search_var.get().strip()


        with get_connection() as conn:

            with conn.cursor() as cur:

                if search:

                    cur.execute(
                        queries.SEARCH_BOOKS,
                        {
                            "search": f"%{search}%"
                        }
                    )

                else:

                    cur.execute(
                        queries.LIST_BOOKS
                    )


                return cur.fetchall()


    def refresh_books(self):

        try:

            rows = self.get_rows()


            for item in self.tree.get_children():

                self.tree.delete(item)


            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=row
                )


            self.status.set(
                f"{len(rows)} livre(s)"
            )


        except Exception as exc:

            messagebox.showerror(
                "Erreur PostgreSQL",
                str(exc)
            )

            self.status.set(
                "Erreur"
            )


    # ========================================================
    # LIVRE SELECTIONNE
    # ========================================================

    def selected_id(self):

        selection = self.tree.selection()


        if not selection:

            messagebox.showinfo(
                "Sélection",
                "Sélectionnez un livre."
            )

            return None


        values = self.tree.item(
            selection[0],
            "values"
        )


        return int(values[0])


    # ========================================================
    # FICHE DU LIVRE
    # ========================================================

    def show_selected(self):

        book_id = self.selected_id()


        if book_id is None:

            return


        try:

            with get_connection() as conn:

                with conn.cursor() as cur:

                    cur.execute(
                        queries.BOOK_DETAIL,
                        {
                            "id_livre": book_id
                        }
                    )

                    book = cur.fetchone()


                    cur.execute(
                        queries.EDITIONS,
                        {
                            "id_livre": book_id
                        }
                    )

                    editions = cur.fetchall()


                    cur.execute(
                        queries.COPIES,
                        {
                            "id_livre": book_id
                        }
                    )

                    copies = cur.fetchall()


                    cur.execute(
                        queries.READINGS,
                        {
                            "id_livre": book_id
                        }
                    )

                    readings = cur.fetchall()


                    cur.execute(
                        queries.NOTES,
                        {
                            "id_livre": book_id
                        }
                    )

                    notes = cur.fetchall()


                    documents = []

                    try:

                        cur.execute(
                            queries.DOCUMENTS,
                            {
                                "id_livre": book_id
                            }
                        )

                        documents = cur.fetchall()

                    except Exception:

                        conn.rollback()


            self.show_detail(
                book,
                editions,
                copies,
                readings,
                notes,
                documents
            )


        except Exception as exc:

            messagebox.showerror(
                "Erreur PostgreSQL",
                str(exc)
            )


    # ========================================================
    # AFFICHAGE DE LA FICHE
    # ========================================================

    def show_detail(
        self,
        book,
        editions,
        copies,
        readings,
        notes,
        documents
    ):

        win = tk.Toplevel(self)

        win.title(
            f"Fiche - {book[1]}"
        )

        win.geometry(
            "1000x700"
        )


        text = tk.Text(
            win,
            wrap="word",
            font=("Segoe UI", 10)
        )

        text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        text.insert(
            "end",
            "LIVRE\n",
            "title"
        )


        text.insert(
            "end",
            f"Titre : {book[1]}\n"
        )

        text.insert(
            "end",
            f"Sous-titre : {book[2] or ''}\n"
        )

        text.insert(
            "end",
            f"Année de parution : {book[3] or ''}\n"
        )

        text.insert(
            "end",
            f"Nombre de pages : {book[5] or ''}\n"
        )

        text.insert(
            "end",
            f"Auteur(s) : {book[6] or ''}\n"
        )

        text.insert(
            "end",
            f"Catégorie(s) : {book[7] or ''}\n"
        )


        text.insert(
            "end",
            "\nRésumé :\n"
        )

        text.insert(
            "end",
            f"{book[4] or ''}\n"
        )


        # ----------------------------------------------------
        # EDITIONS
        # ----------------------------------------------------

        text.insert(
            "end",
            "\nÉDITIONS\n",
            "title"
        )


        for row in editions:

            text.insert(
                "end",
                f"ID {row[0]} | "
                f"{row[1] or ''} | "
                f"{row[2] or ''} | "
                f"ISBN {row[3] or ''} | "
                f"{row[4] or ''}\n"
            )


        # ----------------------------------------------------
        # EXEMPLAIRES
        # ----------------------------------------------------

        text.insert(
            "end",
            "\nEXEMPLAIRES\n",
            "title"
        )


        if copies:

            for row in copies:

                text.insert(
                    "end",
                    f"Exemplaire {row[0]} | "
                    f"Éditeur : {row[1] or ''} | "
                    f"ISBN : {row[2] or ''} | "
                    f"État : {row[3] or ''} | "
                    f"Emplacement : {row[4] or ''} | "
                    f"Achat : {row[5] or ''} | "
                    f"Prix : {row[6] or ''}\n"
                )

        else:

            text.insert(
                "end",
                "Aucun exemplaire.\n"
            )


        # ----------------------------------------------------
        # LECTURES
        # ----------------------------------------------------

        text.insert(
            "end",
            "\nLECTURES\n",
            "title"
        )


        if readings:

            for row in readings:

                text.insert(
                    "end",
                    f"Lecture {row[0]} | "
                    f"Exemplaire {row[1]} | "
                    f"{row[2] or ''} -> "
                    f"{row[3] or ''} | "
                    f"Statut : {row[4] or ''} | "
                    f"Note : {row[5] or ''}\n"
                )

        else:

            text.insert(
                "end",
                "Aucune lecture.\n"
            )


        # ----------------------------------------------------
        # NOTES
        # ----------------------------------------------------

        text.insert(
            "end",
            "\nNOTES\n",
            "title"
        )


        if notes:

            for row in notes:

                text.insert(
                    "end",
                    f"[{row[2] or 'Sans titre'}] "
                    f"{row[3] or ''}\n"
                )

        else:

            text.insert(
                "end",
                "Aucune note.\n"
            )


        # ----------------------------------------------------
        # DOCUMENTS
        # ----------------------------------------------------

        text.insert(
            "end",
            "\nDOCUMENTS / PDF\n",
            "title"
        )


        if documents:

            for row in documents:

                text.insert(
                    "end",
                    f"{row[1]} -> {row[2]}\n"
                )

        else:

            text.insert(
                "end",
                "Aucun document associé.\n"
            )


        text.config(
            state="disabled"
        )


        text.tag_configure(
            "title",
            font=("Segoe UI", 11, "bold")
        )


    # ========================================================
    # OUVRIR UN PDF
    # ========================================================

    def open_pdf(self):

        book_id = self.selected_id()


        if book_id is None:

            return


        try:

            with get_connection() as conn:

                with conn.cursor() as cur:

                    cur.execute(
                        queries.DOCUMENTS,
                        {
                            "id_livre": book_id
                        }
                    )

                    documents = cur.fetchall()


            pdfs = [

                row for row in documents

                if (
                    (row[3] or "").lower() == "pdf"
                    or row[2].lower().endswith(".pdf")
                )

            ]


            if not pdfs:

                messagebox.showinfo(
                    "PDF",
                    "Aucun PDF associé à ce livre."
                )

                return


            path = pdfs[0][2]


            if not os.path.exists(path):

                messagebox.showerror(
                    "PDF",
                    f"Fichier introuvable :\n{path}"
                )

                return


            if sys.platform.startswith("win"):

                os.startfile(path)

            elif sys.platform == "darwin":

                subprocess.Popen(
                    ["open", path]
                )

            else:

                subprocess.Popen(
                    ["xdg-open", path]
                )


        except Exception as exc:

            messagebox.showerror(
                "Erreur",
                str(exc)
            )


    # ========================================================
    # TEST CONNEXION
    # ========================================================

    def test_connection(self):

        try:

            with get_connection() as conn:

                with conn.cursor() as cur:

                    cur.execute(
                        "SELECT version();"
                    )

                    version = cur.fetchone()[0]


            messagebox.showinfo(
                "Connexion PostgreSQL",
                f"Connexion réussie.\n\n{version}"
            )


        except Exception as exc:

            messagebox.showerror(
                "Connexion PostgreSQL",
                str(exc)
            )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    app = MainWindow()

    app.mainloop()
