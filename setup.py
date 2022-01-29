"""
RUN ONLY ONCE!
This script will create the database and the tables.
"""

import os
import sqlite3

# If there is a database, check to make sure the user wants to overwrite it.
if os.path.isfile('database.db'):
    overwrite = input('Database already exists. Overwrite? (y/n) ')
    if overwrite == 'y':
        os.remove('database.db')
    else:
        print('Exiting...')
        exit()

# Create the database and connect to it.
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the tables.
c.execute('''CREATE TABLE guilds (
    guild_id INTEGER PRIMARY KEY,
    settings TEXT
    peermissions TEXT DEFAULT '[]'
    )''')
conn.commit()

c.execute('''CREATE TABLE emojis (
    name TEXT PRIMARY KEY,
    id INTEGER,
    embedded BOOLEAN
    )''')
conn.commit()

c.execute('''CREATE TABLE admins (
    id INTEGER PRIMARY KEY,
    name TEXT
    level INTEGER DEFAULT 0
    )''')
conn.commit()

