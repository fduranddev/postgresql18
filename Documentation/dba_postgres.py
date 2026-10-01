#!/usr/bin/env python3
import psycopg2
import subprocess
import csv
import os

# --- Configuration PostgreSQL ---
HOST = "localhost"
PORT = 5433
USER = "postgres"
PASSWORD = "Tamerlan2026"
DB = "postgres"  # base par défaut pour connexion initiale

# --- Connexion ---
def connect_db(database=DB):
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        dbname=database
    )
    return conn

# --- Exécuter requête SQL ---
def execute_query():
    query = input("SQL> ")
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        try:
            rows = cur.fetchall()
            for r in rows:
                print(r)
        except psycopg2.ProgrammingError:
            print("Requête exécutée avec succès.")
        conn.commit()
    except Exception as e:
        print("Erreur SQL :", e)
    finally:
        cur.close()
        conn.close()

# --- Lister bases ---
def list_databases():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
    print("Bases disponibles :")
    for db in cur.fetchall():
        print("-", db[0])
    cur.close()
    conn.close()

# --- Lister utilisateurs ---
def list_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin FROM pg_roles")
    print("Utilisateurs / Rôles :")
    for r in cur.fetchall():
        print(r)
    cur.close()
    conn.close()

# --- Créer ou modifier utilisateur ---
def create_user():
    username = input("Nom utilisateur: ")
    password = input("Mot de passe: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (username,))
    if cur.fetchone():
        cur.execute("ALTER USER {} WITH PASSWORD %s".format(username), (password,))
        print(f"Utilisateur '{username}' existe déjà. Mot de passe mis à jour.")
    else:
        cur.execute("CREATE USER {} WITH PASSWORD %s".format(username), (password,))
        print(f"Utilisateur '{username}' créé.")
    conn.commit()
    cur.close()
    conn.close()

# --- Supprimer utilisateur ---
def drop_user():
    username = input("Utilisateur à supprimer: ")
    confirm = input(f"Confirmer suppression de '{username}' ? (oui/non): ")
    if confirm.lower() != "oui":
        print("Suppression annulée.")
        return
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DROP USER {}".format(username))
        conn.commit()
        print(f"Utilisateur '{username}' supprimé.")
    except Exception as e:
        print("Erreur :", e)
    finally:
        cur.close()
        conn.close()

# --- Voir sessions actives ---
def list_sessions():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT pid, usename, datname, state FROM pg_stat_activity")
    print("Sessions actives :")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

# --- Sauvegarde base ---
def backup_database():
    db = input("Base à sauvegarder: ")
    file = f"{db}_backup.sql"

    # Chemin complet pg_dump pour WSL2
    pg_dump_path = "/usr/lib/postgresql/18/bin/pg_dump"

    # Exporter mot de passe pour pg_dump
    os.environ["PGPASSWORD"] = PASSWORD

    cmd = [
        pg_dump_path,
        "-h", HOST,
        "-p", str(PORT),
        "-U", USER,
        "-d", db,
        "-f", file
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Sauvegarde créée :", file)
    except FileNotFoundError:
        print("pg_dump introuvable. Installez postgresql-client sous WSL2.")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la sauvegarde :", e)

# --- Export CSV d’une requête ---
def export_csv():
    query = input("Requête SQL : ")
    file = "export.csv"
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("Export CSV terminé :", file)
    except Exception as e:
        print("Erreur :", e)
    finally:
        cur.close()
        conn.close()

# --- Menu principal ---
def menu():
    while True:
        print("\n--- Console DBA PostgreSQL ---")
        print("1 - Exécuter requête SQL")
        print("2 - Lister bases")
        print("3 - Créer / Modifier utilisateur")
        print("4 - Supprimer utilisateur")
        print("5 - Lister utilisateurs")
        print("6 - Voir sessions actives")
        print("7 - Sauvegarde base")
        print("8 - Export CSV")
        print("0 - Quitter")

        choice = input("Choix : ")
        if choice == "1":
            execute_query()
        elif choice == "2":
            list_databases()
        elif choice == "3":
            create_user()
        elif choice == "4":
            drop_user()
        elif choice == "5":
            list_users()
        elif choice == "6":
            list_sessions()
        elif choice == "7":
            backup_database()
        elif choice == "8":
            export_csv()
        elif choice == "0":
            break
        else:
            print("Choix invalide.")

# --- Exécution ---
if __name__ == "__main__":
    menu()