# List structure to hold all tiles to be played in game
# Needs to generate tiles randomly!!!
from TileTypes import *
from landmark import *
from random import randint

class Stack:

    def __init__(self):
        self._alist = []

    def push(self, element):
        self._alist.append(element)

    def pop(self):
        if self.is_empty():
            return None
        return self._alist.pop()

    def top(self):
        if self.is_empty():
            return None
        return self._alist[-1]

    def length(self):
        return len(self._alist)

    def is_empty(self):
        return self.length() == 0

class DeckOfTiles():
    def __init__(self):
        self._tileList = []
        self._deck = Stack()
        self._nextTile = None
        self.generateTiles()
        self.buildDeck()
    # Adds starting tile and other remaining tiles to the list
    # Needs to start by adding an initial tile which has not been done here
    # ATTENTION: Brendan/Eimear/Cathy, the subclasses of the tile 
    # need to be generated here and ID's are needed to allow randomisation
    # Sorry, didn't know what I was doing and feel free to change this to make it work better
    #
    # It's fine, Claire. Was planning on going home this weekend but that's OK. I'm sure my family doesn't want to see
    # me for the first time in ages anyway.

    def buildDeck(self):
        for i in range(len(self._tileList)):
            rand = len(self._tileList) - 1
            while rand > -1:
                point = randint(0, rand)
                self._deck.push(self._tileList[point])
                del self._tileList[point]
                rand -= 1
        self._nextTile = self._deck.top()
    
    def moveToBottom(self, tile):
        self._deck.alist = [tile] + self._deck.alist

    def generateTiles(self):
        
        ct = CityTile()
        print(ct._top)
        self._tileList += [ct]
        tscc = ThreeSidedCapCrest()
        self._tileList += [tscc]
        tscr = ThreeSidedCapRoad()
        self._tileList += [tscr]
        fwc = FourWayCrossroad()
        self._tileList += [fwc]
        cc = CityCone()
        self._tileList += [cc]
        for i in range(2):
            ccc = CityConeCrest()
            self._tileList += [ccc]
            mr = MonasteryRoad()
            self._tileList += [mr]
            ac = AdjacentCaps()
            self._tileList += [ac]
            dcc = DiagonalCapCrest()
            self._tileList += [dcc]
            drc = DiagonalRoadCrest()
            self._tileList += [drc]
            tscrc = ThreeSidedCapRoadCrest()
            self._tileList += [tscrc]
        for i in range(3):
            clb = CapLeftBend()
            self._tileList += [clb]
            crb = CapRightBend()
            self._tileList += [crb]
            csr = CapStraightRoad()
            self._tileList += [csr]
            ctj = CapTJunction()
            self._tileList += [ctj]
            oc = OppositeCaps()
            self._tileList += [oc]
            dc = DiagonalCap()
            self._tileList += [dc]
            dr = DiagonalRoad()
            self._tileList += [dr]
            tsc = ThreeSidedCap()
            self._tileList += [tsc]
        for i in range(4):
            ttj = TownTJunction()
            self._tileList += [ttj]
        for i in range(5):
            m = MonasteryTile()
            self._tileList += [m]
            cct = CityCapTile()
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

    def drawTile(self):
        return self._deck.pop()

