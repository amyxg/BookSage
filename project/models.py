import sqlite3

def init_db():
    # is_new_user is to Check if the user is new
    conn = sqlite3.connect('bookSage.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            has_completed_survey INTEGER DEFAULT 0  
        )
    ''')
    # Create survey table
    c.execute('''CREATE TABLE IF NOT EXISTS survey_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reading_frequency TEXT,
    book_preference TEXT,
    discover_method TEXT,
    genres TEXT,  -- Multiple genres, stored as a comma-separated string
    fiction_non_fiction TEXT,
    explore_genres TEXT,
    tone TEXT,
    themes TEXT,  -- Stored as comma-separated values
    book_length TEXT,
    book_era TEXT,
    narrative_perspective TEXT,
    favorite_authors TEXT,
    top_books TEXT,
    reading_purpose TEXT,
    thought_provoking TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    c.execute('''CREATE TABLE user_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    isbn TEXT,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP

    )''')

    conn.commit()
    conn.close()

# Initialize the database

if __name__ == "__main__":
    init_db()