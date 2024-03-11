import phylib
import sqlite3

import math

# Define the header and footer for SVG files
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

MAX_OBJECTS = 1000
FRAME_RATE=0.01

# Import constants from phylib to global variables
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

# Define standard colours of pool balls
BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",
    "MEDIUMPURPLE",
    "LIGHTSALMON",
    "LIGHTGREEN",
    "SANDYBROWN"
]


def compute_acceleration(self , vel_x, vel_y,VEL_EPSILON, DRAG):
    """
    Computes the acceleration of a rolling ball based on its velocity components (vel_x, vel_y).

    Parameters:
        vel_x (float): The x-component of the velocity.
        vel_y (float): The y-component of the velocity.

    Returns:
        tuple: A tuple containing the x and y components of the acceleration.
    """
    
    # Compute the speed of the rolling ball
    speed_rb = math.sqrt(vel_x ** 2 + vel_y ** 2)

        # Compute acceleration with drag
    if speed_rb > VEL_EPSILON:
        acc_x = -vel_x / speed_rb * DRAG
        acc_y = -vel_y / speed_rb * DRAG
    else:
        acc_x = 0.0
        acc_y = 0.0
        
    return acc_x, acc_y

class Coordinate(phylib.phylib_coord):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass

class StillBall(phylib.phylib_object):
    """
    Python StillBall class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires ball number and position (x,y) as arguments.
        """

        # Create a generic phylib_object
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_STILL_BALL,
            number,
            pos,
            None,
            None,
            0.0,
            0.0
        )

        # Convert the phylib_object into a StillBall class
        self.__class__ = StillBall
        self.number = number  # Assign the 'number' attribute here

    def svg(self):
        """
        Returns SVG representation of the still ball.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x , self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])


class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y), velocity (vx, vy), and acceleration (ax, ay) as arguments.
        """

        # Create a generic phylib_object
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_ROLLING_BALL,
            number,
            pos,
            vel,
            acc,
            0.0,
            0.0
        )

        # Convert the phylib_object into a RollingBall class
        self.__class__ = RollingBall
        self.number = number

    def svg(self):
        """
        Returns SVG representation of the rolling ball.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x , self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])


class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires hole number and position (x,y) as arguments.
        """

        # Create a generic phylib_object
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_HOLE,
            number,
            pos,
            None,
            None,
            0.0,
            0.0
        )

        # Convert the phylib_object into a Hole class
        self.__class__ = Hole

    def svg(self):
        """
        Returns SVG representation of the hole.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x , self.obj.hole.pos.y, HOLE_RADIUS)


class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires cushion number and position (x,y) as arguments.
        """

        # Create a generic phylib_object
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_HCUSHION,
            number,
            pos,
            None,
            None,
            0.0,
            0.0
        )

        # Convert the phylib_object into a HCushion class
        self.__class__ = HCushion

    def svg(self):
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (self.obj.hcushion.y)      


class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires cushion number and position (x,y) as arguments.
        """

        # Create a generic phylib_object
        phylib.phylib_object.__init__(
            self,
            phylib.PHYLIB_VCUSHION,
            number,
            pos,
            None,
            None,
            0.0,
            0.0
        )

        # Convert the phylib_object into a VCushion class
        self.__class__ = VCushion

    def svg(self):
        """
        Returns SVG representation of the vertical cushion.
        """
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (self.obj.vcushion.x)

class Table(phylib.phylib_table):
    """
    Pool table class.
    """

    def __init__(self):
        """
        Table constructor method.
        This method calls the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__(self)
        self.current = -1

    def __iadd__(self, other):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object(other)
        return self

    def __iter__(self):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__(self):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1
        if self.current < MAX_OBJECTS:
            return self[self.current]

        self.current = -1
        raise StopIteration

    def __getitem__(self, index):
        """
        This method adds item retrieval support using square brackets [ ].
        It calls get_object to retrieve a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object(index)
        if result is None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__(self):
        """
        Returns a string representation of the table.
        """
        result = ""
        result += "time = %6.1f;\n" % self.time
        for i, obj in enumerate(self):
            result += "  [%02d] = %s\n" % (i, obj)
        return result

    def segment(self):
        """
        Calls the segment method from phylib.i.
        Sets the __class__ of the returned phylib_table object to Table.
        """

        result = phylib.phylib_table.segment(self)
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    def svg(self):
        """
        Returns SVG representation of the table.
        """
        svg_str = ""
        svg_str += HEADER
        for obj in self:
            if obj is not None:
                svg_str += obj.svg()
        svg_str += FOOTER
        return svg_str






    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number, Coordinate(0,0), Coordinate(0,0), Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number, Coordinate( ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
                # return table
        return new;
    
    def cueBall(self, xpos, ypos, xvel, yvel):
        for obj in self:
            print(obj)  # Debugging print to check all objects in the table
            if isinstance(obj, RollingBall) and obj.number == 0:
            # Store the cue ball's position in temporary variables
                obj_type = obj.type
                obj_pos_x = obj.obj.rolling_ball.pos.x
                obj_pos_y = obj.obj.rolling_ball.pos.y
                obj_vel_x = obj.obj.rolling_ball.vel.x
                obj_vel_y = obj.obj.rolling_ball.vel.y

            # Update the attributes of the cue ball
                obj.type = phylib.PHYLIB_ROLLING_BALL
                obj.obj.rolling_ball.pos.x = xpos
                obj.obj.rolling_ball.pos.y = ypos
                obj.obj.rolling_ball.vel.x = xvel
                obj.obj.rolling_ball.vel.y = yvel
                obj.compute_acceleration()

            # Set the number of the cue ball to 0
                obj.number = 0

            # Restore the original type and position if needed
                obj.type = obj_type
                obj.obj.rolling_ball.pos.x = obj_pos_x
                obj.obj.rolling_ball.pos.y = obj_pos_y
                obj.obj.rolling_ball.vel.x = obj_vel_x
                obj.obj.rolling_ball.vel.y = obj_vel_y

                return obj  # Return the cue ball if found

        print("Cue ball not found in the table.")
        return None  # Return None if the cue ball is not found

    
"""A3"""  

class Database:
    def __init__(self, reset=False):
        if reset:
            import os
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")

        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

    def createDB(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Ball (
                                BALL_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                BALL_NO INTEGER NOT NULL,
                                POS_X FLOAT NOT NULL,
                                POS_Y FLOAT NOT NULL,
                                VEL_X FLOAT,
                                VEL_Y FLOAT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TTable (
                                TABLE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                TIME FLOAT NOT NULL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BallTable (
                                BALL_ID INTEGER NOT NULL,
                                TABLE_ID INTEGER NOT NULL,
                                FOREIGN KEY (BALL_ID) REFERENCES Ball (BALL_ID),
                                FOREIGN KEY (TABLE_ID) REFERENCES TTable (TABLE_ID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Shot (
                                SHOT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                PLAYER_ID INTEGER NOT NULL,
                                GAME_ID INTEGER NOT NULL,
                                FOREIGN KEY (PLAYER_ID) REFERENCES Player (PLAYER_ID),
                                FOREIGN KEY (GAME_ID) REFERENCES Game (GAME_ID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TableShot (
                                TABLE_ID INTEGER NOT NULL,
                                SHOT_ID INTEGER NOT NULL,
                                FOREIGN KEY (TABLE_ID) REFERENCES TTable (TABLE_ID),
                                FOREIGN KEY (SHOT_ID) REFERENCES Shot (SHOT_ID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Game (
                                GAME_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAME_NAME VARCHAR(64) NOT NULL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player (
                                PLAYER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAME_ID INTEGER NOT NULL,
                                PLAYER_NAME VARCHAR(64) NOT NULL,
                                FOREIGN KEY (GAME_ID) REFERENCES Game (GAME_ID)
                            )''')

        self.conn.commit()
    
    

    def readTable(self, tableID):
   
        self.cursor.execute('''SELECT Ball.BALL_ID, BALL_NO, POS_X, POS_Y, VEL_X, VEL_Y
                           FROM Ball
                           JOIN BallTable ON Ball.BALL_ID = BallTable.BALL_ID
                           WHERE TABLE_ID = ?''', (tableID + 1,))
        balls_data = self.cursor.fetchall()

        if not balls_data:
            return None

        self.cursor.execute('''SELECT TIME FROM TTable WHERE TABLE_ID = ?''', (tableID + 1,))
        table_time = self.cursor.fetchone()[0]

        table = Table()
        for ball_data in balls_data:
            ball_id, ball_no, pos_x, pos_y, vel_x, vel_y = ball_data
            if vel_x is None and vel_y is None:
                table += StillBall(ball_no, Coordinate(pos_x, pos_y))
            else:
                acceleration = compute_acceleration(ball_data,vel_x, vel_y,VEL_EPSILON, DRAG)  # Calculate acceleration
                table += RollingBall(ball_no, Coordinate(pos_x, pos_y), Coordinate(vel_x, vel_y), Coordinate(acceleration[0], acceleration[1]))

        table.time = table_time
        return table



    def writeTable(self, table):
    
        self.cursor.execute('''INSERT INTO TTable (TIME) VALUES (?)''', (table.time,))
        table_id = self.cursor.lastrowid - 1

        for obj in table:
        # Check if the object is a ball
            if isinstance(obj, StillBall):
                ball_id = self.cursor.execute('''INSERT INTO Ball (BALL_NO, POS_X, POS_Y) 
                                      VALUES (?, ?, ?)''', (obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y)).lastrowid

                self.cursor.execute('''INSERT INTO BallTable (BALL_ID, TABLE_ID) VALUES (?, ?)''', (ball_id, table_id))
            elif isinstance(obj, RollingBall):
                ball_id = self.cursor.execute('''INSERT INTO Ball (BALL_NO, POS_X, POS_Y, VEL_X, VEL_Y) 
                                      VALUES (?, ?, ?, ?, ?)''', (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y)).lastrowid

                self.cursor.execute('''INSERT INTO BallTable (BALL_ID, TABLE_ID) VALUES (?, ?)''', (ball_id, table_id))

        self.conn.commit()
        return table_id
    
    
    def close(self):
        self.conn.commit()
        self.conn.close()


    def setGame(self, gameName, player1Name, player2Name):
        """
        Insert a new game record into the database.

        Parameters:
            gameName (str): The name of the game.
            player1Name (str): The name of the first player.
            player2Name (str): The name of the second player.
        """
        # Open a connection to the database
        conn = sqlite3.connect("phylib.db")
        cursor = conn.cursor()

        # Insert the game record into the database
        cursor.execute('''INSERT INTO Game (GAME_NAME) VALUES (?)''', (gameName,))
        gameID = cursor.lastrowid

        # Insert the player records into the database
        cursor.execute('''INSERT INTO Player (GAME_ID, PLAYER_NAME) VALUES (?, ?)''', (gameID, player1Name))
        cursor.execute('''INSERT INTO Player (GAME_ID, PLAYER_NAME) VALUES (?, ?)''', (gameID, player2Name))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return gameID
    
    def getPlayerID(self, playerName):
        """
        Retrieve the player ID based on the player's name.

        Parameters:
            playerName (str): The name of the player.

        Returns:
            int or None: The player ID if found, None otherwise.
        """
        # Open a connection to the database
        conn = sqlite3.connect("phylib.db")
        cursor = conn.cursor()

        # Query the database to retrieve the player ID
        cursor.execute('''SELECT PLAYER_ID FROM Player WHERE PLAYER_NAME = ?''', (playerName,))
        player_id = cursor.fetchone()

        # Close the connection
        conn.close()

        # Return the player ID if found, otherwise return None
        return player_id[0] if player_id else None
    
    def newShot(self, gameID, playerID):
        """
        Add a new entry to the Shot table for the current game and the given player ID.

        Parameters:
            gameID (int): The ID of the game.
            playerID (int): The ID of the player.

        Returns:
            int: The ID of the newly added shot.
        """
        # Open a connection to the database
        conn = sqlite3.connect("phylib.db")
        cursor = conn.cursor()

        # Insert a new entry into the Shot table
        cursor.execute('''INSERT INTO Shot (PLAYER_ID, GAME_ID) VALUES (?, ?)''', (playerID, gameID))
        shot_id = cursor.lastrowid

        # Close the connection
        conn.commit()
        conn.close()

        # Return the ID of the newly added shot
        return shot_id
    


class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        # Retrieve game details from database
        database = Database()
        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("If gameID is provided, other arguments must be None")
        elif gameID is None and (gameName is None or player1Name is None or player2Name is None):
            raise TypeError("If gameID is not provided, all Name arguments must be provided")

        if gameID is not None:
            
            game_data = database.getGame(gameID)
            if game_data is None:
                raise ValueError("Invalid gameID")
            
            self.gameID = game_data[0]
            self.gameName = game_data[1]
            self.player1Name = game_data[2]
            self.player2Name = game_data[3]
        else:
            # Add game details to the database
            database.setGame(gameName, player1Name, player2Name)
            self.gameID = None
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            
    def shoot(self, gameName, playerName, table, xvel, yvel):
        database = Database()
        playerID = database.getPlayerID(playerName)
        if playerID is None:
            raise ValueError("Invalid playerName")

        shotID = database.newShot(gameName, playerID)

    # Retrieve the position of the cue ball
        xpos = 100  # Define xpos with appropriate value
        ypos = 100  # Define ypos with appropriate value

    # Retrieve the cue ball from the table and update its attributes
        cue_ball = table.cueBall(xpos, ypos, xvel, yvel)

        if cue_ball is None:
            raise ValueError("Cue ball not found in the table")

    # Set the type attribute of the cue ball to ROLLING_BALL
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

    # Set the attributes of the cue ball
        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

    # Recalculate the acceleration parameters
        cue_ball.compute_acceleration()

    # Set the number of the cue ball to 0
        cue_ball.number = 0

        while True:
            segment = table.segment()
            if segment is None:
                break

            segment_length = segment.endTime - segment.startTime
            num_frames = int(segment_length / self.FRAME_INTERVAL)

            for i in range(num_frames):
                next_table = table.roll(segment.startTime + i * self.FRAME_INTERVAL)
                next_table.time = segment.startTime + i * self.FRAME_INTERVAL
                tableID = database.writeTable(next_table)
                database.recordTableShot(tableID, shotID)

        database.close()
        return shotID
