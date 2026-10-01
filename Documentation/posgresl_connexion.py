import psycopg2

try:
    # Connexion à PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="HR",
        user="postgres",
        password="Tamerlan2026"
    )

    print("Connexion réussie à la base HR")

    # Création d'un curseur
    cursor = conn.cursor()

    # Exécution d'une requête
    cursor.execute("SELECT employee_id, first_name, last_name FROM employees LIMIT 3;")

    # Récupération des résultats
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # Fermeture
    cursor.close()
    conn.close()

except Exception as e:
    print("Erreur :", e)
