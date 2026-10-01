import psycopg2

conn = psycopg2.connect(database="HR", user = "postgres", password = "admin", host = "127.0.0.1", port = "5436")

print ("Connexion à la base OK")

cur = conn.cursor()

cur.execute("SELECT job_id, job_title, min_salary, max_salary from public.jobs LIMIT 10")
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("JOB_TITLE = ", row[1])
   print ("MIN_SALARY = ", row[2])
   print ("MAX_SALARY = ", row[3], "\n")