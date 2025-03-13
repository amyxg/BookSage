import sqlite3

def init_db():
    # is_new_user is to Check if the user is new
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_new_user BOOLEAN DEFAULT 1 
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

