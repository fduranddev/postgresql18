import dearpygui.dearpygui as dpg
from db import fetch_contacts, add_contact, update_contact, delete_contact

selected_id = None  # id du contact actuellement sélectionné pour modification

def rafraichir_table():
    """Vide et recharge le tableau des contacts depuis la base."""
    dpg.delete_item("table_contacts", children_only=True, slot=1)
    for contact_id, nom, email, telephone in fetch_contacts():
        with dpg.table_row(parent="table_contacts"):
            dpg.add_text(str(contact_id))
            dpg.add_text(nom)
            dpg.add_text(email)
            dpg.add_text(telephone or "")
            dpg.add_button(
                label="Sélectionner",
                user_data=(contact_id, nom, email, telephone),
                callback=selectionner_contact
            )

def selectionner_contact(sender, app_data, user_data):
    """Remplit le formulaire avec les données du contact cliqué."""
    global selected_id
    contact_id, nom, email, telephone = user_data
    selected_id = contact_id
    dpg.set_value("input_nom", nom)
    dpg.set_value("input_email", email)
    dpg.set_value("input_telephone", telephone or "")

def ajouter_callback():
    nom = dpg.get_value("input_nom")
    email = dpg.get_value("input_email")
    telephone = dpg.get_value("input_telephone")
    if not nom or not email:
        dpg.set_value("status_text", "Le nom et l'email sont obligatoires.")
        return
    add_contact(nom, email, telephone)
    dpg.set_value("status_text", f"Contact '{nom}' ajouté.")
    vider_formulaire()
    rafraichir_table()

def modifier_callback():
    global selected_id
    if selected_id is None:
        dpg.set_value("status_text", "Sélectionnez d'abord un contact.")
        return
    nom = dpg.get_value("input_nom")
    email = dpg.get_value("input_email")
    telephone = dpg.get_value("input_telephone")
    update_contact(selected_id, nom, email, telephone)
    dpg.set_value("status_text", f"Contact #{selected_id} mis à jour.")
    vider_formulaire()
    rafraichir_table()

def supprimer_callback():
    global selected_id
    if selected_id is None:
        dpg.set_value("status_text", "Sélectionnez d'abord un contact.")
        return
    delete_contact(selected_id)
    dpg.set_value("status_text", f"Contact #{selected_id} supprimé.")
    vider_formulaire()
    rafraichir_table()

def vider_formulaire():
    global selected_id
    selected_id = None
    dpg.set_value("input_nom", "")
    dpg.set_value("input_email", "")
    dpg.set_value("input_telephone", "")

def exporter_csv_callback():
    """Exporte les contacts affichés dans un fichier CSV."""
    import csv
    contacts = fetch_contacts()
    with open("contacts_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nom", "email", "telephone"])
        writer.writerows(contacts)
    dpg.set_value("status_text", "Export réalisé : contacts_export.csv")

def quitter_callback():
    dpg.stop_dearpygui()

def a_propos_callback():
    if dpg.does_item_exist("popup_a_propos"):
        dpg.delete_item("popup_a_propos")
    with dpg.window(label="À propos", tag="popup_a_propos", modal=True,
                     width=300, height=120, pos=(200, 200)):
        dpg.add_text("CRUD DearPyGui + PostgreSQL")
        dpg.add_text("Tutoriel de démonstration")
        dpg.add_button(label="Fermer",
                        callback=lambda: dpg.delete_item("popup_a_propos"))

def basculer_theme_callback(sender, app_data):
    """Bascule entre thème clair et thème sombre."""
    if app_data:
        dpg.bind_theme(theme_sombre)
    else:
        dpg.bind_theme(theme_clair)

# --- Construction de l'interface ---

dpg.create_context()

# Chargement d'une police personnalisée (taille 24)
with dpg.font_registry():
    default_font = dpg.add_font("/mnt/c/Windows/Fonts/arial.ttf", 24)

dpg.bind_font(default_font)

# Thèmes simples pour l'exemple de bascule clair/sombre
with dpg.theme() as theme_sombre:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 25))

with dpg.theme() as theme_clair:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240))

with dpg.window(label="Gestion des contacts (PostgreSQL)", tag="main_window",
                 width=700, height=550):

    with dpg.menu_bar():

        with dpg.menu(label="Fichier"):
            dpg.add_menu_item(label="Actualiser", callback=lambda: rafraichir_table())
            dpg.add_menu_item(label="Exporter en CSV", callback=exporter_csv_callback)
            dpg.add_separator()
            dpg.add_menu_item(label="Quitter", callback=quitter_callback)

        with dpg.menu(label="Édition"):
            dpg.add_menu_item(label="Ajouter", callback=ajouter_callback)
            dpg.add_menu_item(label="Modifier", callback=modifier_callback)
            dpg.add_menu_item(label="Supprimer", callback=supprimer_callback)
            dpg.add_menu_item(label="Vider le formulaire", callback=vider_formulaire)

        with dpg.menu(label="Affichage"):
            dpg.add_checkbox(label="Thème sombre", callback=basculer_theme_callback)

        with dpg.menu(label="Aide"):
            dpg.add_menu_item(label="À propos", callback=a_propos_callback)

    dpg.add_text("Formulaire contact")
    dpg.add_input_text(label="Nom", tag="input_nom")
    dpg.add_input_text(label="Email", tag="input_email")
    dpg.add_input_text(label="Téléphone", tag="input_telephone")

    with dpg.group(horizontal=True):
        dpg.add_button(label="Ajouter", callback=ajouter_callback)
        dpg.add_button(label="Modifier", callback=modifier_callback)
        dpg.add_button(label="Supprimer", callback=supprimer_callback)
        dpg.add_button(label="Vider le formulaire", callback=vider_formulaire)

    dpg.add_text("", tag="status_text", color=(0, 200, 0))
    dpg.add_separator()

    with dpg.table(tag="table_contacts", header_row=True,
                    borders_innerH=True, borders_outerH=True,
                    borders_innerV=True, borders_outerV=True):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Nom")
        dpg.add_table_column(label="Email")
        dpg.add_table_column(label="Téléphone")
        dpg.add_table_column(label="Action")

    rafraichir_table()  # chargement initial des données

dpg.create_viewport(title="CRUD DearPyGui + PostgreSQL", width=750, height=550)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()