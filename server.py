import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

shoot_game = None  # Assuming `shoot_game` is initialized elsewhere

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

        # Parse the path and handle different endpoints
        parsed_path = self.path
        if parsed_path == '/send_data':
            self.process_data(post_data.decode('utf-8'))
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Data received and processed successfully.")
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

    def process_data(self, data):
        try:
            data_json = json.loads(data)
            svg_data = data_json['svg']
            velocity_x = data_json['velocityX']
            velocity_y = data_json['velocityY']
            self.process_svg(svg_data)
            self.process_velocity(velocity_x, velocity_y)
        except json.JSONDecodeError:
            print("Error decoding JSON data")
        except KeyError:
            print("Missing required keys in JSON data")

    def process_svg(self, svg_data):
        print('Received SVG data:')
        print(svg_data)
        # You can use `shoot_game` to process the received SVG data

    def process_velocity(self, velocity_x, velocity_y):
        print('Received initial velocity X:', velocity_x)
        print('Received initial velocity Y:', velocity_y)
        # You can use `shoot_game` to process the received velocities

def run_server(port):
    httpd = HTTPServer(('localhost', port), MyHandler)
    print("Server listening on port:", port)
    httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    run_server(int(sys.argv[1]))
