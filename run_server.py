from http.server import HTTPServer
from request_handler import RequestHandler


# Starts a HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8014):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()