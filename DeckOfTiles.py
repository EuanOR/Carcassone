# List structure to hold all tiles to be played in game
# Needs to generate tiles randomly!!!
from Tile import *
class DeckOfTiles():
    def __init__(self, size):
        self._tileList = []
        self._firstTile = None
        self._size = size
        self.buildTiles()
        self.getTileList()
    # Adds starting tile and other remaining tiles to the list
    # Needs to start by adding an initial tile which has not been done here
    # ATTENTION: Brendan/Eimear/Cathy, the subclasses of the tile 
    # need to be generated here and ID's are needed to allow randomisation
    # Sorry, didn't know what I was doing and feel free to change this to make it work better
    def buildTiles(self):
        tile = Tile()
        self._tileList += [tile]
        self._firstTile = self._tileList[0]
        for i in range(1, self._size):
            tile = Tile()
            self._tileList += [tile]
    # Return tile list 
    def getTileList(self):
        return self._tileList
