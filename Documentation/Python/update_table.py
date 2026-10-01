import psycopg2

conn = psycopg2.connect(database="HR", user = "postgres", password = "Tamerlan2026", host = "127.0.0.1", port = "5433")

print ("Connexion à la base OK")

cur = conn.cursor()

cur.execute("UPDATE COMMERCIAL.COMPANY set SALARY = 25000.00 where ID = 1")
conn.commit()
print ("Total number of rows updated :", cur.rowcount)

cur.execute("SELECT id, name, address, salary  from COMMERCIAL.COMPANY")
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3], "\n")

print ("Operation done successfully");
conn.close()