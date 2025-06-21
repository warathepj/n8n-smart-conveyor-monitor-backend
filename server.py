import http.server
import socketserver
import os
import json  # Import the json module

PORT = 8000
DIRECTORY = "backend/chart"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.getcwd(), DIRECTORY), **kwargs)

    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                print("Received data:", data)  # Process the data here

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'message': 'Data received successfully'}
                self.wfile.write(json.dumps(response).encode('utf-8'))

                # Check if the received message is {'text': '/chart'}
                if data.get('text') == '/chart':
                    print("Received '/chart' command. Creating chart...")
                    os.system('python3 chart.py')  # Execute chart.py
                    print("Chart creation initiated.")

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': 'Invalid JSON format'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            super().do_POST()

try:
    # Create the server with a specific directory
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT} from directory '{DIRECTORY}'")
        print(f"Chart can be viewed at http://localhost:{PORT}/chart.png")
        httpd.serve_forever()
except OSError as e:
    print(f"Error: Could not bind to port {PORT}. Another process may be using it.")
    print(f"Details: {e}")
