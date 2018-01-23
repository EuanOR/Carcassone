class Meeple(object):
    colours = ["red","blue","green","yellow"]

    def __init__(self,colour,tile,player,):
        self._colour = colour
        self._tile = tile
        self._player =  player

    def setColour(self,colour):
        self._colour = colour

    def getColour(self):
        return self._colour

    def setTile(self,tile):
        self._tile = tile

    def getTile(self):
        return self._tile

    def setPlayer(self,player):
        self._player = player

    def getPlayer(self):
        return self._player
