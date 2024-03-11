import math

import Physics



def main():

    table = Physics.Table()



    pos_x = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)

    pos_y = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)

    pos = Physics.Coordinate(pos_x, pos_y)

    sb = Physics.StillBall(1, pos)



    pos_rb = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)

    vel = Physics.Coordinate(0.0, -1000.0)

    acc = Physics.Coordinate(0.0, 180.0)

    rb = Physics.RollingBall(0, pos_rb, vel, acc)



    table += sb

    table += rb



    print(table)



    while table is not None:

        table = table.segment()

        if table:

            print(table)

        else:

            break



if __name__ == "__main__":

    main()


