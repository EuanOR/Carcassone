class Tile:
    #class to represent a tile from the game Carcassonne
    #V.01 designed for tiles with only roads and towns
    #V.01 can correctly generate 10 types of tiles
    #Current version: V.01


    def __init__(self, north, south, east, west):
        self._north = north
        self._south = south
        self._east = east
        self._west = west
        self._x = 0
        self._y = 0
        self._order = 0

    #Rotates the positions clockwise
    def rotate_left(self):
        n = self._north
        self._north = self._west
        self._west = self._south
        self._south = self._east
        self._east = n

    #Rotates the positions anti-clockwise
    def rotate_right(self):
        n = self._north
        self._north = self._east
        self._east = self._south
        self._south = self._west
        self._west = n

    #When the pieces are added to the board, records the current x and
    #y positions        
    def add_to_board(self, xpos, ypos):
        self._xpos = xpos
        self._ypos = ypos

    #String representation of the tile's sides
    def __str__(self):
        return("North: %s West: %s %s South: East: %s" % (self._north,
                                                         self._south,
                                                         self._west,
                                                         self._east))

    
    
