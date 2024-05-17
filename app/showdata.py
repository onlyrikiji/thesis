import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

# Execute a SQL query to fetch data
cursor.execute("SELECT * FROM post")
rows = cursor.fetchall()

# Print or process the fetched data
for row in rows:
    print(row)

# Close the connection
conn.close()