import sys
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import Physics
from Physics import Game



shoot_game = Physics.Game(gameName="Poll", player1Name="Kit", player2Name="Kat")

# Define the necessary classes and functions

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        parsed_path = self.path.split("?")[0]
        if parsed_path == '/':
            self.send_response(302)
            self.send_header('Location', '/shoot.html')
            self.end_headers()
                
        elif parsed_path == "/shoot.html":
            # Serve shoot.html
            self._serve_html_file("shoot.html")
        elif parsed_path.startswith("/table-"):
            # Serve table-?.svg files
            self._serve_svg_file(parsed_path)
        else:
            # Return 404 for other requests
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        # Extract parameters from the parsed POST data
        sb_number = int(parsed_post_data['sb_number'][0])
        sb_x = float(parsed_post_data['sb_x'][0])
        sb_y = float(parsed_post_data['sb_y'][0])
        rb_x = float(parsed_post_data['rb_x'][0])
        rb_y = float(parsed_post_data['rb_y'][0])
        rb_dx = float(parsed_post_data['rb_dx'][0])
        rb_dy = float(parsed_post_data['rb_dy'][0])

        form_data = {
            'still_ball': {
                'pos_x': sb_x,
                'pos_y': sb_y
            },
            'rolling_ball': {
                'pos_x': rb_x,
                'pos_y': rb_y,
                'vel_x': rb_dx,
                'vel_y': rb_dy
            }
        }

        # Compute acceleration
        acceleration = compute_acceleration(form_data)

        # Construct table
        table = construct_table(form_data, acceleration)

        # Save SVG files
        save_svg_files(table)

        # Generate HTML content
        html_content = generate_html_content(form_data, table)
        
        if self.path == '/send_velocity':
        # Extract velocity data from the parsed POST data
            velocity_x = float(parsed_post_data['velocityX'][0])
            velocity_y = float(parsed_post_data['velocityY'][0])

        # Process the velocity data as needed
            self.process_velocity(velocity_x, velocity_y)

        # Send a simple response indicating success
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Initial velocity received and processed successfully.")

        # Send HTML response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

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
            
    def process_velocity(self,velocity_x, velocity_y):
    # Process the received velocity data here
        print('Received initial velocity X:', velocity_x)
        print('Received initial velocity Y:', velocity_y)
        with open('velocity_data.txt', 'a') as file:
            file.write(f"Velocity X: {velocity_x}, Velocity Y: {velocity_y}\n")

def compute_acceleration(form_data):
    # Extract still ball and rolling ball data from form_data
    still_ball_data = form_data.get('still_ball', {})
    rolling_ball_data = form_data.get('rolling_ball', {})

    # Extract position and velocity data from form data for still ball
    pos_x_sb = float(still_ball_data.get('pos_x', 0))
    pos_y_sb = float(still_ball_data.get('pos_y', 0))

    # Extract position, velocity, and delta values from form data for rolling ball
    pos_x_rb = float(rolling_ball_data.get('pos_x', 0))
    pos_y_rb = float(rolling_ball_data.get('pos_y', 0))
    delta_x_rb = float(rolling_ball_data.get('delta_x', 0))
    delta_y_rb = float(rolling_ball_data.get('delta_y', 0))

    # Calculate acceleration
    # In this example, we're simply returning the delta values as acceleration
    acceleration = {'x': delta_x_rb, 'y': delta_y_rb}

    return acceleration


def construct_table(form_data, acceleration):
    # Create the table
    table = Physics.Table()  # Assuming Physics module contains Table class

    # Construct StillBall and RollingBall
    # Assuming form data contains information about StillBall and RollingBall
    still_ball_data = form_data.get('still_ball', {})
    rolling_ball_data = form_data.get('rolling_ball', {})

    # Extract position for the StillBall
    pos_x = float(still_ball_data.get('pos_x', 0))
    pos_y = float(still_ball_data.get('pos_y', 0))
    pos = Physics.Coordinate(pos_x, pos_y)  # Assuming Coordinate class exists

    # Create and store the StillBall
    sb = Physics.StillBall(1, pos)  # Assuming StillBall class exists

    # Extract position, velocity, and acceleration for RollingBall
    pos_x_rb = float(rolling_ball_data.get('pos_x', 0))
    pos_y_rb = float(rolling_ball_data.get('pos_y', 0))
    vel_x_rb = float(rolling_ball_data.get('vel_x', 0))
    vel_y_rb = float(rolling_ball_data.get('vel_y', 0))
    acc_x_rb = float(acceleration['x'])  # Corrected access
    acc_y_rb = float(acceleration['y'])  # Corrected access

    pos_rb = Physics.Coordinate(pos_x_rb, pos_y_rb)  # Assuming Coordinate class exists
    vel_rb = Physics.Coordinate(vel_x_rb, vel_y_rb)  # Assuming Coordinate class exists
    acc_rb = Physics.Coordinate(acc_x_rb, acc_y_rb)  # Assuming Coordinate class exists

    # Create and store the RollingBall
    rb = Physics.RollingBall(0, pos_rb, vel_rb, acc_rb)  # Assuming RollingBall class exists

    # Add the StillBall to the table
    table += sb

    # Add the RollingBall to the table
    table += rb

    return table

def save_svg_files(table):
    # Initialize file index
    file_index = 0

    # Iterate through table segments
    while table is not None:
        # Generate SVG representation for the current segment
        svg_content = table.svg()

        # Write the SVG representation to a file
        with open(f"table-{file_index}.svg", "w") as svg_file:
            svg_file.write(svg_content)

        # Move to the next segment
        table = table.segment()

        # Increment file index
        file_index += 1

def generate_html_content(form_data, table):
    file_index = 4
    still_ball_data = form_data.get('still_ball', {})
    rolling_ball_data = form_data.get('rolling_ball', {})
    
    pos_x = float(still_ball_data.get('pos_x', 0))
    pos_y = float(still_ball_data.get('pos_y', 0))
    
    pos_x_rb = float(rolling_ball_data.get('pos_x', 0))
    pos_y_rb = float(rolling_ball_data.get('pos_y', 0))
    vel_x_rb = float(rolling_ball_data.get('vel_x', 0))
    vel_y_rb = float(rolling_ball_data.get('vel_y', 0))
    # Initialize HTML content
    html_content = "<!DOCTYPE html>\n<html>\n<head>\n<title>Ball Positions and Velocities</title>\n</head>\n<body>\n"

    # Add descriptions of original Ball positions and velocities
    html_content += "<h2>Original Ball Positions and Velocities</h2>\n"
    html_content += "<ul>\n"
    
    html_content += f"<li>Still Ball Position:( {pos_x},{pos_y})</li>\n"
    html_content += f"<li>Rolling Ball Position:( {pos_x_rb},{pos_y_rb}) Velocity: ( {vel_x_rb},{vel_y_rb})</li>\n"
    
    html_content += "</ul>\n"

    # Add SVG representation of the table
    html_content += "<h2>SVG Table Representation</h2>\n"
    for file_index in range(file_index):
                with open(f"table-{file_index}.svg", "rb") as svg_file:
                    svg_content = svg_file.read().decode('utf-8')
                    html_content += f"<div>{svg_content}</div>"

    # Add Back link
    html_content += '<a href="/shoot.html">Back</a>\n'

    # Close HTML body and document
    html_content += "</body>\n</html>"

    return html_content

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
        
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
    print("Server listening on port:", int(sys.argv[1]))
    httpd.serve_forever()
