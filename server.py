import os
import http.server
import shutil
from urllib.parse import urlparse, parse_qs
import math
import phylib

PORT = 5105  # Adjust the port number according to your student ID

class MyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/shoot.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('shoot.html', 'rb') as file:
                self.wfile.write(file.read())
        elif path.startswith('/table-') and path.endswith('.svg'):
            filename = path[1:]  # Remove leading '/' from filename
            if os.path.exists(filename):
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                with open(filename, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, 'File Not Found: {}'.format(filename))
        else:
            self.send_error(404, 'Resource Not Found: {}'.format(path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)

        # Delete all table-?.svg files in the server's directory
        for filename in os.listdir('.'):
            if filename.startswith('table-') and filename.endswith('.svg'):
                os.remove(filename)

        # Compute the acceleration on the RollingBall
        v = float(form_data['velocity'][0])
        r = float(form_data['radius'][0])
        a = float(form_data['angle'][0])

        # Do the calculation
        g = 9.8  # Gravity acceleration
        acc = g * math.sin(math.radians(a))  # Compute acceleration

        # Construct a Table and add the Balls
        table = phylib.Table()
        pos = phylib.Coordinate()
        pos.x = phylib.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(phylib.PHYLIB_BALL_DIAMETER * phylib.PHYLIB_BALL_DIAMETER / 2.0)
        pos.y = phylib.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(phylib.PHYLIB_BALL_DIAMETER * phylib.PHYLIB_BALL_DIAMETER / 2.0)
        sb = phylib.StillBall(1, pos)
        table += sb

        pos = phylib.Coordinate()
        pos.x = phylib.PHYLIB_TABLE_WIDTH / 2.0
        pos.y = phylib.PHYLIB_TABLE_LENGTH - phylib.PHYLIB_TABLE_WIDTH / 2.0
        vel = phylib.Coordinate()
        vel.x = 0.0
        vel.y = -v
        acc_coord = phylib.Coordinate()
        acc_coord.x = 0.0
        acc_coord.y = acc
        rb = phylib.RollingBall(0, pos, vel, acc_coord)
        table += rb

        # Save the table-?.svg files
        index = 0
        filename = "table-{}.svg".format(index)
        with open(filename, "w") as f:
            f.write(table.svg())

        # Generate HTML response
        html_response = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display</title>
</head>
<body>
    <h1>Original Ball Positions and Velocities:</h1>
    <p>Velocity: {} m/s, Radius: {} m, Angle: {} degrees</p>
    """.format(v, r, a)

        # Add img tags for each svg file
        for filename in os.listdir('.'):
            if filename.startswith('table-') and filename.endswith('.svg'):
                html_response += '<img src="{}" alt="table-{}.svg"><br>'.format(filename, index)
                index += 1

        # Add Back link
        html_response += '<a href="/shoot.html">Back</a>'

        html_response += """</body>
</html>"""

        # Send the HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_response.encode())

if __name__ == '__main__':
    httpd = http.server.HTTPServer(('localhost', PORT), MyServer)
    print("Server running at http://localhost:{}".format(PORT))
    httpd.serve_forever()
