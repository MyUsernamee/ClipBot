# Takes a id, name, and permission level and adds it to the admins table
import sqlite3
import sys

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Get CLI arguments
id = sys.argv[1]
name = sys.argv[2]
permission = sys.argv[3]

# Add user
c.execute("INSERT INTO admins VALUES (?, ?, ?)", (id, name, permission))
conn.commit()

print("User added " + name)