
# List structure to hold all tiles to be played in game
# Needs to generate tiles randomly!!!
from TileTypes import *
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

    def buildDeck(self):
        for i in range(1):
            ct = CityTile()1
            self._tileList += [ct]
            tscc = ThreeSidedCapCrest()2
            self._tileList += [tscc]
            tscr = ThreeSidedCapRoad()3
            self._tileList += [tscr]
            fwc = FourWayCrossroad()15
            self._tile += [fwc]
            cc = CityCone()
            self._tileList += [cc]
        for i in range(2):
            ccc = CityConeCrest()
            self._tileList += [ccc]
            mr = MonasteryRoad()4
            self._tileList += [mr]
            ac = AdjacentCaps()
            self._tileList += [ac]
            dcc = DiagonalCapCrest()
            self._tileList += [dc]
            drc = DiagonalRoadCrest()
            self._tileList += [drc]
            tscrc = ThreeSidedCapRoadCrest()
            self._tileList += [tscrc]
        for i in range(3):
            clb = CapLeftBend()5
            self._tileList += [clb]
            crb = CapRightBend()6
            self._tileList += [crb]
            csr = CapStraightRoad()7
            self._titleList += [csr]
            ctj = CapTJunction()8
            self._tileList += [ctj]
            oc = OppositeCaps()9
            self._tileList += [oc]
            dc = DiagonalCap()10
            self._tileList += [dc]
            dr = DiagonalRoad()11
            self._tileList += [dr]
            tsc = ThreeSidedCap()12
            self._tileList += [tsc]
        for i in range(4):
            m = Monastery()14
            self._tileList += [m]
            ttj = TownTJunction()16
            self._tileList += [ttj]
        for i in range(5):
            cct = CityCapTile()13
            self._tileList += [cct]
        for i in range(8):
            sr = StraightRoad()
            self._tileList += [sr]
        for i in range(9):
            lr = LRoad()
            self._tileList += [lr]




    
    # Return tile list 
    def getTileList(self):
        return self._tileList
