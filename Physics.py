import phylib

# Import constants from phylib to global variables
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS
PHYLIB_TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
PHYLIB_TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
# Add more constants here as needed

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
        Constructor function. Requires ball number and position (x,y) as
        arguments.
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

    # Add an svg method here
    def svg(self):
        """
        Returns SVG representation of the still ball.
        """
        return f'<circle cx="{self.pos.x}" cy="{self.pos.y}" r="{BALL_RADIUS}" fill="{BALL_COLOURS[self.number]}" />\n'


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
        if result == None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        # Add more conditions for other types if necessary
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

    # Add svg method here

