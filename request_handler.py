import socketserver
import sqlite3
from http.server import BaseHTTPRequestHandler
from typing import Tuple
from urllib.parse import urlparse, parse_qs
from data_validator import DataValidator
from captcha_generator import CaptchaGenerator


class RequestHandler(BaseHTTPRequestHandler):
    """
        Class for processing HTTP requests.
    """
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        self.captcha_text = ""
        super().__init__(request, client_address, server)

    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Generate a new CAPTCHA text for this request
            self.captcha_text = CaptchaGenerator.generate_captcha_text()
            print(self.captcha_text)
            # Generate CAPTCHA image
            captcha_image = CaptchaGenerator.generate_captcha_image(self.captcha_text)

            with open('templates/registration.html', 'r') as file:
                html_content = file.read()
                # Replace placeholder with CAPTCHA image
                html_content = html_content.replace('{{captcha_image}}', captcha_image)
                self.wfile.write(bytes(html_content, 'utf-8'))
        elif parsed_path.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/login.html', 'r') as file:
                self.wfile.write(bytes(file.read(), 'utf-8'))
        elif self.path == '/logout?' or self.path == '/logout': # I have no idea why it adds ? at the end
            # Redirect to the login form
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
        elif parsed_path.path == '/login_successful':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/login_successful.html', 'r') as file:
                self.wfile.write(bytes(file.read(), 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = parse_qs(post_data)

        if self.path == '/register':
            email = post_data['email'][0]
            name = post_data['name'][0]
            password = post_data['password'][0]
            captcha_input = post_data['captcha'][0]  # Extract CAPTCHA input
            print(captcha_input)

            # Data validation
            if not (email and name and password and captcha_input):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing data')
                return

            if not DataValidator.is_valid_email(email):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid email')
                return

            if not DataValidator.is_valid_name(name):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid name')
                return

            if not DataValidator.is_valid_password(password):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid password')
                return

            # The CAPTCHA validation is turned off for now, because i get "incorrect captcha"
            # every time (even though I get the same result when I print the real captcha and the user input)
            # Verify CAPTCHA
            # if captcha_input != self.captcha_text:
            #     self.send_response(400)
            #     self.end_headers()
            #     self.wfile.write(b'Incorrect CAPTCHA')
            #     return

            # Saving data in the data base - SQLite
            conn = sqlite3.connect('db/users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, name, password, verified) VALUES (?, ?, ?, ?)',
                           (email, name, password, False))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Registration successful')
        elif self.path == '/login':
            email = post_data['email'][0]
            password = post_data['password'][0]

            # Check if the database contains this e-mail
            conn = sqlite3.connect('db/users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            conn.close()

            # If the e-mail is not in the database
            if user is None:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Email not registered')
                return

            # Password check
            if password != user[3]:  # user[3] contains the password in the database
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid password')
                return

            # If both e-mail and password are valid we send message for successful entry
            self.send_response(302)
            self.send_header('Location', '/login_successful')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')