import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = self.path.split("?")[0]
        if parsed_path == '/':
            self.send_response(302)
            self.send_header('Location', '/shoot.html')
            self.end_headers()                
        elif parsed_path == "/shoot.html":
            self._serve_html_file("shoot.html")
        elif parsed_path.startswith("/table-"):
            self._serve_svg_file(parsed_path)
        elif parsed_path.endswith(".svg"):
            self._serve_static_file(parsed_path, 'image/svg+xml')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        # Process the velocity data if it's being sent
        if self.path == '/send_velocity':
            velocity_x = float(parsed_post_data['velocityX'][0])
            velocity_y = float(parsed_post_data['velocityY'][0])
            self.process_velocity(velocity_x, velocity_y)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Initial velocity received and processed successfully.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def _serve_html_file(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def _serve_svg_file(self, file_path):
        try:
            with open(file_path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def _serve_static_file(self, file_path, content_type):
        try:
            with open(file_path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def process_velocity(self, velocity_x, velocity_y):
        print('Received initial velocity X:', velocity_x)
        print('Received initial velocity Y:', velocity_y)
        with open('velocity_data.txt', 'a') as file:
            file.write(f"Velocity X: {velocity_x}, Velocity Y: {velocity_y}\n")

def run_server(port):
    httpd = HTTPServer(('localhost', port), MyHandler)
    print("Server listening on port:", port)
    httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    run_server(int(sys.argv[1]))
