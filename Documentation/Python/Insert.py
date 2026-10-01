import psycopg2

conn = psycopg2.connect(database="HR", user = "postgres", password = "Tamerlan2026", host = "127.0.0.1", port = "5433")

print ("Connexion à la base OK")

cur = conn.cursor()

cur.execute("INSERT INTO COMMERCIAL.COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )");

cur.execute("INSERT INTO COMMERCIAL.COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

cur.execute("INSERT INTO COMMERCIAL.COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

cur.execute("INSERT INTO COMMERCIAL.COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

conn.commit()
print ("Enregistrements créés");
conn.close()