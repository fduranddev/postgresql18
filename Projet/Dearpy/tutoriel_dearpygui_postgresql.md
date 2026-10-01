# Tutoriel : Créer une application CRUD avec DearPyGui et PostgreSQL

Ce tutoriel vous guide pas à pas dans la création d'une application de bureau en Python qui utilise **DearPyGui** pour l'interface graphique et **PostgreSQL** comme base de données, avec des opérations CRUD complètes (Create, Read, Update, Delete).

## 1. Prérequis

- Python 3.8 ou supérieur
- Un serveur PostgreSQL installé et démarré (localement ou distant)
- Les bibliothèques suivantes :

```bash
pip install dearpygui psycopg2-binary
```

> `psycopg2-binary` est la version précompilée du connecteur PostgreSQL pour Python, plus simple à installer que `psycopg2` (qui nécessite des dépendances de compilation).

## 2. Préparer la base de données PostgreSQL

Connectez-vous à PostgreSQL (via `psql` ou un outil comme pgAdmin) et créez une base et une table de test :

```sql
CREATE DATABASE tutoriel_db;

\c tutoriel_db

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telephone VARCHAR(20)
);
```

## 3. Structure du projet

```
mon_projet/
│
├── app.py          # Application principale
├── db.py           # Fonctions d'accès à la base de données
└── requirements.txt
```

## 4. Module de connexion à la base de données (`db.py`)

Ce module centralise toutes les interactions avec PostgreSQL.

```python
import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "tutoriel_db",
    "user": "postgres",
    "password": "votre_mot_de_passe"
}

def get_connection():
    """Ouvre une nouvelle connexion à la base de données."""
    return psycopg2.connect(**DB_CONFIG)

def fetch_contacts():
    """Récupère tous les contacts triés par id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, email, telephone FROM contacts ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_contact(nom, email, telephone):
    """Ajoute un nouveau contact."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (nom, email, telephone) VALUES (%s, %s, %s);",
        (nom, email, telephone)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_contact(contact_id, nom, email, telephone):
    """Met à jour un contact existant."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE contacts SET nom=%s, email=%s, telephone=%s WHERE id=%s;",
        (nom, email, telephone, contact_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(contact_id):
    """Supprime un contact."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s;", (contact_id,))
    conn.commit()
    cur.close()
    conn.close()
```

> **Astuce sécurité** : on utilise toujours des requêtes paramétrées (`%s`) plutôt que du formatage de chaînes, pour éviter les injections SQL.

## 5. Interface graphique avec DearPyGui (`app.py`)

DearPyGui fonctionne avec un système de **contexte**, de **fenêtres (windows)** et de **widgets** identifiés par des tags. Voici l'application complète :

```python
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
```

## 6. Intégration d'une barre de menus

DearPyGui permet d'ajouter une véritable barre de menus (comme dans une application de bureau classique) grâce à `dpg.menu_bar()`, placée à l'intérieur d'une fenêtre. Chaque `dpg.menu()` représente une entrée déroulante (« Fichier », « Édition »...), et chaque `dpg.add_menu_item()` est une action cliquable à l'intérieur de ce menu.

Dans l'exemple ci-dessus, quatre menus ont été ajoutés :

- **Fichier** : actualiser le tableau, exporter les contacts en CSV, quitter l'application.
- **Édition** : accès rapide aux actions CRUD (Ajouter, Modifier, Supprimer, Vider le formulaire), sans passer par les boutons.
- **Affichage** : une case à cocher (`dpg.add_checkbox`) permettant de basculer entre thème clair et thème sombre, via `dpg.bind_theme()`.
- **Aide** : ouvre une fenêtre modale « À propos ».

Points clés à retenir :

| Élément | Rôle |
|---|---|
| `dpg.menu_bar()` | Conteneur de la barre de menus, doit être placé directement dans un `dpg.window` |
| `dpg.menu(label=...)` | Un menu déroulant (ex. « Fichier ») |
| `dpg.add_menu_item(label=..., callback=...)` | Une action du menu, avec sa fonction associée |
| `dpg.add_separator()` | Ligne de séparation visuelle entre groupes d'actions dans un menu |
| `dpg.add_checkbox()` dans un menu | Permet d'avoir une option activable/désactivable directement dans le menu |
| `dpg.stop_dearpygui()` | Ferme proprement l'application (utilisé par « Quitter ») |
| `dpg.window(..., modal=True)` | Crée une fenêtre modale, utile pour « À propos » ou des confirmations |

> **Remarque** : `dpg.menu_bar()` doit être déclaré tout en haut du bloc `with dpg.window(...)`, avant les autres widgets, pour s'afficher correctement comme une barre horizontale en haut de la fenêtre.

Vous pouvez aussi attacher une barre de menus directement au **viewport** (la fenêtre du système d'exploitation) plutôt qu'à une fenêtre interne, avec `dpg.set_viewport_menu_bar()` — utile si vous n'avez qu'une seule fenêtre principale en plein écran :

```python
with dpg.viewport_menu_bar():
    with dpg.menu(label="Fichier"):
        dpg.add_menu_item(label="Quitter", callback=quitter_callback)
```

## 7. Explication du fonctionnement

| Élément | Rôle |
|---|---|
| `dpg.window` | Fenêtre principale de l'application |
| `dpg.input_text` | Champs de saisie du formulaire (nom, email, téléphone) |
| `dpg.table` + `dpg.table_row` | Affichage dynamique des contacts issus de PostgreSQL |
| `user_data` sur le bouton | Permet de transmettre les données de la ligne au callback |
| `rafraichir_table()` | Recharge le tableau après chaque opération CRUD |
| `db.py` | Isole toute la logique SQL, ce qui garde `app.py` lisible |

## 8. Lancer l'application

```bash
python app.py
```

Une fenêtre s'ouvre avec :
- un formulaire pour saisir un contact,
- des boutons **Ajouter / Modifier / Supprimer**,
- un tableau qui liste les contacts en base, avec un bouton **Sélectionner** par ligne pour charger une entrée dans le formulaire avant modification.

## 9. Pour aller plus loin

- **Pool de connexions** : pour une application plus lourde, utilisez `psycopg2.pool.SimpleConnectionPool` plutôt que d'ouvrir/fermer une connexion à chaque requête.
- **Gestion des erreurs** : encadrez les appels à `db.py` avec des blocs `try/except psycopg2.Error` et affichez les erreurs dans `status_text`.
- **Thème et style** : DearPyGui permet de personnaliser les couleurs et polices via `dpg.theme` et `dpg.add_theme_color`.
- **Recherche/filtre** : ajoutez un champ de recherche qui filtre les contacts via une clause `WHERE nom ILIKE %s`.
- **Variables d'environnement** : évitez de stocker le mot de passe en clair dans `db.py` ; utilisez plutôt `os.environ` ou un fichier `.env` avec `python-dotenv`.

## 10. Récapitulatif des commandes SQL utilisées

```sql
-- Lecture
SELECT id, nom, email, telephone FROM contacts ORDER BY id;

-- Création
INSERT INTO contacts (nom, email, telephone) VALUES (%s, %s, %s);

-- Mise à jour
UPDATE contacts SET nom=%s, email=%s, telephone=%s WHERE id=%s;

-- Suppression
DELETE FROM contacts WHERE id=%s;
```

Ce tutoriel constitue une base solide que vous pouvez étendre : authentification, plusieurs tables liées, exports, ou intégration avec une API REST.
