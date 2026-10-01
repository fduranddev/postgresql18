#---------
# main.py
#---------

import csv
from database import engine, SessionLocal
from models import Base, User

# Créer les tables si elles n'existent pas
Base.metadata.create_all(engine)

# ------------------- Fonctions CRUD -------------------

def create_user():
    name = input("Nom: ")
    email = input("Email: ")
    session = SessionLocal()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    print(f"Utilisateur créé : {user}")
    session.close()

def list_users(users=None):
    session = SessionLocal()
    if users is None:
        users = session.query(User).all()
    if users:
        print("\n--- Liste des utilisateurs ---")
        for u in users:
            print(u)
    else:
        print("Aucun utilisateur trouvé")
    session.close()

def update_user():
    try:
        user_id = int(input("ID de l'utilisateur à mettre à jour: "))
        new_email = input("Nouvel email: ")
    except ValueError:
        print("ID invalide")
        return
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if user:
        user.email = new_email
        session.commit()
        print(f"Utilisateur mis à jour : {user}")
    else:
        print("Utilisateur non trouvé")
    session.close()

def delete_user():
    try:
        user_id = int(input("ID de l'utilisateur à supprimer: "))
    except ValueError:
        print("ID invalide")
        return
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        print(f"Utilisateur supprimé : {user}")
    else:
        print("Utilisateur non trouvé")
    session.close()

# ------------------- Recherche -------------------

def search_user():
    keyword = input("Nom ou email à rechercher: ")
    session = SessionLocal()
    users = session.query(User).filter(
        (User.name.ilike(f"%{keyword}%")) | (User.email.ilike(f"%{keyword}%"))
    ).all()
    list_users(users)
    session.close()

# ------------------- Export CSV -------------------

def export_csv():
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        print("Aucun utilisateur à exporter")
        session.close()
        return
    filename = input("Nom du fichier CSV (ex: users.csv): ")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "email"])
        for u in users:
            writer.writerow([u.id, u.name, u.email])
    print(f"Export terminé : {filename}")
    session.close()

# ------------------- Menu CLI -------------------

def menu():
    while True:
        print("\n--- Menu Utilisateur Avancé ---")
        print("1. Créer un utilisateur")
        print("2. Lister tous les utilisateurs")
        print("3. Mettre à jour un utilisateur")
        print("4. Supprimer un utilisateur")
        print("5. Rechercher un utilisateur")
        print("6. Export CSV")
        print("7. Quitter")
        choice = input("Choix: ")
        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            search_user()
        elif choice == "6":
            export_csv()
        elif choice == "7":
            print("Au revoir !")
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    menu()
