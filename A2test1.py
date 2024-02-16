import math
import Physics  # Assuming Physics module is correctly defined

# Call the Physics.Table constructor and store the result in a variable table.
table = Physics.Table()

# Compute the x and y values for the initial position of StillBall and RollingBall.
pos_still_ball = Physics.Coordinate(Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0),
                                    Physics.PHYLIB_TABLE_WIDTH / 2.0 - math.sqrt(Physics.PHYLIB_BALL_DIAMETER * Physics.PHYLIB_BALL_DIAMETER / 2.0))

pos_rolling_ball = Physics.Coordinate(Physics.PHYLIB_TABLE_WIDTH / 2.0,
                                       Physics.PHYLIB_TABLE_LENGTH - Physics.PHYLIB_TABLE_WIDTH / 2.0)

vel = Physics.Coordinate(0.0, -1000.0)  # 1m/s (medium speed)
acc = Physics.Coordinate(0.0, 180.0)

# Call the StillBall constructor and store the result in a variable sb.
sb = Physics.StillBall(1, pos_still_ball)

# Call the RollingBall constructor and store the result in a variable rb.
rb = Physics.RollingBall(0, pos_rolling_ball, vel, acc)

# Add the StillBall to the table using “table += sb”.
table += sb

# Add the RollingBall to the table using “table += rb”.
table += rb

# Print the table.
print(table)

# Start a while loop to iterate through the segments of the table.
while True:
    # Call the segment method of the table.
    table = table.segment()

    # Check if table is None.
    if table is None:
        break

    # Print the table.
    print(table)
