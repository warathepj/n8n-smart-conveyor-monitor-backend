import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "backend/chart"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.getcwd(), DIRECTORY), **kwargs)

try:
    # Create the server with a specific directory
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT} from directory '{DIRECTORY}'")
        print(f"Chart can be viewed at http://localhost:{PORT}/chart.png")
        httpd.serve_forever()
except OSError as e:
    print(f"Error: Could not bind to port {PORT}. Another process may be using it.")
    print(f"Details: {e}")
