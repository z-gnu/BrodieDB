import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE parts (
                id INTEGER PRIMARY KEY,
                supplier TEXT,
                part_number TEXT,
                date TEXT,
                inspector TEXT)''')

# Commit and close connection
conn.commit()
conn.close()