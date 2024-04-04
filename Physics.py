import phylib
import sqlite3
import os
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
FRAME_INTERVAL=0.01

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


def compute_acceleration(self , XVEL, vel_y,VEL_EPSILON, DRAG):
    """
    Computes the acceleration of a rolling ball based on its velocity components (XVEL, vel_y).

    Parameters:
        XVEL (float): The x-component of the velocity.
        vel_y (float): The y-component of the velocity.

    Returns:
        tuple: A tuple containing the x and y components of the acceleration.
    """
    
    # Compute the speed of the rolling ball
    speed_rb = math.sqrt(XVEL ** 2 + vel_y ** 2)

        # Compute acceleration with drag
    if speed_rb > VEL_EPSILON:
        acc_x = -XVEL / speed_rb * DRAG
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
        new = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number, Coordinate(0,0), Coordinate(0,0), Coordinate(ball.obj.rolling_ball.acc.x, ball.obj.rolling_ball.acc.y) )
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )
                # add ball to table
                new += new_ball
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number, Coordinate( ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
                # return table
        return new
    
    def cueBall(self):
        for obj in self:
            if isinstance(obj, RollingBall) and obj.obj.rolling_ball.number == 0:
                return obj  # Return the cue ball if found
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                return obj  # Return the cue ball if found

        print("Cue ball not found in the table.")
        return None  # Return None if the cue ball is not found

    
"""A3"""  

class Database:
    def __init__(self, reset=False):
        if reset:
            try:
                os.remove("phylib.db")
            except FileNotFoundError:
                    pass

        self.conn = sqlite3.connect("phylib.db")
        
        self.cursor = self.conn.cursor()
        self.cursor.fetchall()
        self.createDB()

    def createDB(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Ball (
                                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                BALLNO INTEGER NOT NULL,
                                XPOS FLOAT NOT NULL,
                                YPOS FLOAT NOT NULL,
                                XVEL FLOAT,
                                YVEL FLOAT
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TTable (
                                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                TIME FLOAT NOT NULL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BallTable (
                                BALLID INTEGER NOT NULL,
                                TABLEID INTEGER NOT NULL,
                                FOREIGN KEY (BALLID) REFERENCES Ball (BALLID),
                                FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Shot (
                                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                PLAYERID INTEGER NOT NULL,
                                GAMEID INTEGER NOT NULL,
                                FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
                                FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TableShot (
                                TABLEID INTEGER NOT NULL,
                                SHOTID INTEGER NOT NULL,
                                FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID),
                                FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Game (
                                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAMENAME VARCHAR(64) NOT NULL
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player (
                                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAMEID INTEGER NOT NULL,
                                PLAYERNAME VARCHAR(64) NOT NULL,
                                FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
                            )''')

        self.conn.commit()
    
    

    def readTable(self, tableID):
   
        self.cursor.execute('''SELECT Ball.BALLID, BALLNO, XPOS, YPOS, XVEL, YVEL
                           FROM Ball
                           JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                           WHERE TABLEID = ?''', (tableID + 1,))
        balls_data = self.cursor.fetchall()

        if not balls_data:
            return None

        self.cursor.execute('''SELECT TIME FROM TTable WHERE TABLEID = ?''', (tableID + 1,))
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
        #self.conn.commit()
        return table



    def writeTable(self, table):
        # Check if the table already exists in the database
        existing_tables = self.cursor.execute('''SELECT TABLEID, TIME FROM TTable''').fetchall()
        for existing_table in existing_tables:
            #print("Existing table time:", existing_table[1])
            if existing_table[1] == table.time:
                print("Table already exists in the database.")
                return existing_table[0]  # Return the existing table ID

        # If the table doesn't exist, insert it into the database
        self.cursor.execute('''INSERT INTO TTable (TIME) VALUES (?)''', (table.time,))
        TABLEID = self.cursor.lastrowid - 1

        for obj in table:
            # Check if the object is not None and is a ball
            if obj and (isinstance(obj, StillBall) or isinstance(obj, RollingBall)):
                if isinstance(obj, StillBall):
                    BALLID = self.cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS) 
                                      VALUES (?, ?, ?)''', (obj.obj.still_ball.number, obj.obj.still_ball.pos.x, obj.obj.still_ball.pos.y)).lastrowid
                elif isinstance(obj, RollingBall):
                    BALLID = self.cursor.execute('''INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                      VALUES (?, ?, ?, ?, ?)''', (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x, obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x, obj.obj.rolling_ball.vel.y)).lastrowid

                self.cursor.execute('''INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)''', (BALLID, TABLEID + 1))

        self.conn.commit()
        return TABLEID

    
    
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
        cursor.execute('''INSERT INTO Game (GAMENAME ) VALUES (?)''', (gameName,))
        gameID = cursor.lastrowid

        # Insert the player records into the database
        cursor.execute('''INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)''', (gameID, player1Name))
        cursor.execute('''INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)''', (gameID, player2Name))

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
        cursor.execute('''SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?''', (playerName,))
        playerID = cursor.fetchone()

        # Close the connection
        conn.close()

        # Return the player ID if found, otherwise return None
        return playerID[0] if playerID else None
    
    def getGameID(self, gameName):
    
    # Open a connection to the database
        conn = sqlite3.connect("phylib.db")
        cursor = conn.cursor()

    # Query the database to retrieve the game ID
        cursor.execute('''SELECT GAMEID FROM Game WHERE GAMENAME = ?''', (gameName,))
        gameID = cursor.fetchone()

    # Close the connection
        conn.close()

    # Return the game ID if found, otherwise return None
        return gameID[0] if gameID else None

    
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
        cursor.execute('''INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)''', (playerID, gameID))
        SHOTID = cursor.lastrowid

        # Close the connection
        conn.commit()
        conn.close()

        # Return the ID of the newly added shot
        return SHOTID
    
    def recordTableShot(self, tableID, shotID):
        """
        Record the association between a table and a shot in the database.

        Parameters:
            tableID (int): The ID of the table.
            shotID (int): The ID of the shot.
        """
        # Open a connection to the database
        conn = sqlite3.connect("phylib.db")
        cursor = conn.cursor()

        # Insert a new entry into the TableShot table
        cursor.execute('''INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)''', (tableID, shotID))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
        
    def getGame(self, game_id):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT G.GAMEID, G.GAMENAME, P1.PLAYERNAME AS PLAYER1NAME, P2.PLAYERNAME AS PLAYER2NAME
            FROM Game G
            JOIN Player P1 ON G.PLAYERID = P1.PLAYERID
            JOIN Player P2 ON G.PLAYERID = P2.PLAYERID
            WHERE G.GAMEID = ?
        """, (game_id,))
        game_info = cursor.fetchone()
        cursor.close()
        if game_info:
            return {
                'game_id': game_info[0],
                'game_name': game_info[1],
                'player1_name': game_info[2],
                'player2_name': game_info[3]
            }
        else:
            raise ValueError(f"No game found with gameID {game_id}.")
    
    
    
    


class Game:
    
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.database = Database()
        self.database.createDB()

        if gameID is not None and (gameName is not None or player1Name is not None or player2Name is not None):
            raise TypeError("If gameID is provided, other arguments must be None")
        elif gameID is None and (gameName is None or player1Name is None or player2Name is None):
            raise TypeError("If gameID is not provided, all Name arguments must be provided")

        if gameID is not None:
            game_data = self.database.getGame(gameID)
            if game_data is None:
                raise ValueError("Invalid gameID")
            self.gameID = game_data[0] + 1
            self.gameName = game_data[1]
            self.player1Name = game_data[2]
            self.player2Name = game_data[3]
        else:
            self.gameID = None
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.database.setGame(gameName, player1Name, player2Name)

    
    def shoot(self,gameName, playerName, table, xvel, yvel):
        gameID = self.database.getGameID(self.gameName)
        
        
        if gameID is None:
            raise ValueError("Invalid gameName")


        shotID = self.database.newShot(gameName, playerName)
        if shotID is None:
            return

        cue_ball = table.cueBall()
        if cue_ball is None:
            return

        posex, posey = cue_ball.obj.rolling_ball.pos.x, cue_ball.obj.rolling_ball.pos.y
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL
        cue_ball.obj.rolling_ball.number = 0
        cue_ball.obj.rolling_ball.pos.x = posex
        cue_ball.obj.rolling_ball.pos.y = posey
        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        acc_x, acc_y = compute_acceleration(self,xvel, yvel, VEL_EPSILON, DRAG)
        cue_ball.obj.rolling_ball.acc.x = acc_x
        cue_ball.obj.rolling_ball.acc.y = acc_y

        total_segment_length = 0
        while True:
            
            time_start = table.time
            newtable = table.segment()
            if newtable is None:
                break
            total_segment_length = int((newtable.time - time_start) / FRAME_INTERVAL)

            num_frames = total_segment_length
        
            for i in range(num_frames):
            
                frame_time = i * FRAME_INTERVAL
                next_frame_table = table.roll(frame_time)

                next_frame_table.time = time_start + frame_time
            
                print(next_frame_table)

                ntableID = self.database.writeTable(next_frame_table)
            
                if ntableID is None:
                    return

                self.database.recordTableShot(ntableID,shotID)
                
                #return shotID
            
                #self.database.conn.commit()
            table = newtable
            

        