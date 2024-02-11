import sqlite3
from http.server import HTTPServer
from request_handler import RequestHandler

# Създаване на таблицата "users" в базата данни SQLite
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

# Стартиране на HTTP сървър
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8014):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    create_users_table()
    run()
