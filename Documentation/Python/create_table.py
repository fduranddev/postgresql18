#!/usr/bin/env python3

import psycopg2

conn = psycopg2.connect(database="HR", user = "postgres", password = "Tamerlan2026", host = "127.0.0.1", port = "5433")

print ("Connexion à la base OK")

cur = conn.cursor()
cur.execute('''CREATE TABLE commercial.COMPANY
      (ID INT PRIMARY KEY     NOT NULL,
      NAME           TEXT    NOT NULL,
      AGE            INT     NOT NULL,
      ADDRESS        CHAR(50),
      SALARY         REAL);''')

print ("Table créée")

conn.commit()
conn.close()
