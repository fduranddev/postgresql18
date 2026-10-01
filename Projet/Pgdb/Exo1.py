import pgdb
 
# Connect to the database
conn = pgdb.connect(database='HR', host='localhost', user='postgres', password='admin', port='5436')
 
# Create a cursor
cursor = conn.cursor()
 
# Execute a SELECT query
cursor.execute('select * from public.countries')
 
# Fetch all rows
rows = cursor.fetchall()
 
# Print the rows
for row in rows:
    print(row)
 
# Close the cursor and connection
cursor.close()
conn.close()