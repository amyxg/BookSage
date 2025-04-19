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
    # Create survey table
    c.execute('''CREATE TABLE IF NOT EXISTS survey (
        user_id INTEGER PRIMARY KEY,
        favorite_genres TEXT,
        favorite_authors TEXT,
        fiction_or_nonfiction TEXT,
        other_preferences TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )''')
    conn.commit()
    conn.close()

# Initialize the database

if __name__ == "__main__":
    init_db()