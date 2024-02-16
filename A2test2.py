import math
import Physics

# Call the Physics.Table constructor and store the result in a variable table.
table = Physics.Table()

# Call the Physics.Coordinate constructor and store the result in a variable pos.
# Compute the x and y values like we did in A1Test1.c.
# Use math.sqrt to compute the square root.
pos = Physics.Coordinate()
pos.x = Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0)
pos.y = Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0)

# Call the StillBall constructor and store the result in a variable sb.
sb = Physics.StillBall(1, pos)

# Call the Coordinate constructor 3 times to set the variables, pos, vel, and acc for the RollingBall.
pos = Physics.Coordinate()
pos.x = Physics.PHYLIB_TABLE_WIDTH / 2.0
pos.y = Physics.PHYLIB_TABLE_LENGTH - Physics.PHYLIB_TABLE_WIDTH / 2.0

vel = Physics.Coordinate()
vel.x = 0.0
vel.y = -1000.0  # 1m/s (medium speed)

acc = Physics.Coordinate()
acc.x = 0.0
acc.y = 180.0

# Call the RollingBall constructor and store the result in a variable rb.
rb = Physics.RollingBall(0, pos, vel, acc)

# Add the StillBall to the table using “table += sb”.
table += sb

# Add the RollingBall to the table using “table += rb”.
table += rb

# Open a file called "table-%d.svg" with an index that starts at 0 and increments by 1 substituted for %d.
index = 0
filename = "table-{}.svg".format(index)
with open(filename, "w") as f:
    # Write the string returned by the svg method of the table to the file.
    f.write(table.svg())

# Start a while loop conditioned on the value of table (it will run until table is None).
while table:
    # Inside the while loop set the value of table to be the return value of calling the segment method of table.
    table = table.segment()

    # Increment the index for the filename.
    index += 1
    filename = "table-{}.svg".format(index)
    with open(filename, "w") as f:
        # Write the string returned by the svg method of the table to the file.
        f.write(table.svg())
