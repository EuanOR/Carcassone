"""
Purpose: Builds deck of tiles for GameController
Author: Brendan
"""

from TileTypes import *
from landmark import *
from random import randint

# Uses a stack as the underlying data structure for the Deck
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

#Object to represent the deck in Carcassonne
#Uses an implementation of Stack to mimic a copy
class DeckOfTiles():
    def __init__(self):
        self._tileList = []
        self._deck = Stack()
        self._nextTile = None
        self.generateTiles()
        self.buildDeck()

    #Creates a randomized version of the tileList, then casts it to the Stack
    #object
    #
    #Uses randint to choose a random list index, then pushes the item to
    #the Stack before removing it from the list
    def buildDeck(self):
        for i in range(len(self._tileList)):
            rand = len(self._tileList) - 1
            while rand > -1:
                point = randint(0, rand)
                self._deck.push(self._tileList[point])
                del self._tileList[point]
                rand -= 1
        self._nextTile = self._deck.top()

    #Adds the tile to the bottom of the list
    def moveToBottom(self, tile):
        self._deck._alist = [tile] + self._deck._alist

    #Creates a list containing every tile in TileTypes.py (excluding the
    #FreeTile and the InitialTile classes)
    def generateTiles(self):
        
        ct = CityTile()
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

    #Draws a tile using Stack.pop()
    def drawTile(self):
        return self._deck.pop()

