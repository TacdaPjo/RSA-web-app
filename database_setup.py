# database_setup.py
import sqlite3

def create_database():
    with sqlite3.connect('user_activity.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_visited TEXT NOT NULL,
                time_spent INTEGER,
                browser_info TEXT,
                timestamp TEXT,
                ip_address TEXT,
                country TEXT
            )
        ''')
        conn.commit()
# Run this script once to create the database and table
if __name__ == "__main__":
    create_database()