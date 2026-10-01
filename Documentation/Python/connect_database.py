#!/usr/bin/env python3

import psycopg2

conn = psycopg2.connect(database="HR", user = "postgres", password = "admin", host = "127.0.0.1", port = "5436")

print ("Opened database successfully")