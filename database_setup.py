# database_setup.py
import sqlite3

def initialize_db():
    conn = sqlite3.connect('images.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            length TEXT NOT NULL,
            species TEXT NOT NULL,
            location TEXT NOT NULL,
            photo_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call initialize_db() at the start of the application
if __name__ == "__main__":
    initialize_db()
