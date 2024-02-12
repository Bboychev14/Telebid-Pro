import sqlite3


# Creates a "users" table in the SQLite database
def create_users_table():
    conn = sqlite3.connect('db/users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        email TEXT UNIQUE,
                        name TEXT,
                        password TEXT,
                        verified BOOLEAN)''')

    conn.commit()
    conn.close()