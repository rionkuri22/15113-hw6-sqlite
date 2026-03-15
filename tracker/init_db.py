import sqlite3

# Connect to (or create) a database file
con = sqlite3.connect('my_tracker.db')
cur = con.cursor()

# Create table (if it doesn't already exist)
cur.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT,
        rating INTEGER,
        date_finished TEXT,
        notes TEXT
    )
''')
con.commit()
