import math
import Physics

def main():

    # Create the table
    table = Physics.Table()

    # Calculate the position for the StillBall 
    pos_x = Physics.TABLE_WIDTH / 2.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos_y = Physics.TABLE_LENGTH / 4.0 - math.sqrt((Physics.BALL_DIAMETER ** 2 )/ 2.0)
    pos = Physics.Coordinate(pos_x, pos_y)

    # Create and store the StillBall
    sb = Physics.StillBall(1, pos)

    # Calculate position, velocity, and acceleration for RollingBall
    pos_rb = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)
    vel = Physics.Coordinate(0.0, -1000.0)  # moving up along the table's center
    acc = Physics.Coordinate(0.0, 180.0)
    # pos_hole = Physics.Coordinate(0.0,0.0)
    # hl = Physics.Hole(pos_hole)
    # Create and store the RollingBall
    rb = Physics.RollingBall(0, pos_rb, vel, acc)

    # Add the StillBall to the table
    table += sb

    # Add the RollingBall to the table
    table += rb

    # Open a file to write SVG representation
    file_index = 0
    while table is not None:
        # Write the SVG representation to a file
        with open(f"table-{file_index}.svg", "w") as svg_file:
            svg_content = table.svg()
            svg_file.write(svg_content)
        
        # Continue simulation
        table = table.segment()
        file_index += 1

if __name__ == "__main__":
    main()
