class Meeple(object):
    colours = ["red","blue","green","yellow"]

    def __init__(self,colour,tile,player):
        self._colour = colour
        self._tile = tile
        self._player =  player
        self._placed = False

    def __str__(self):
        outstr = ""
        outstr += ("Colour:%s,Tile:%s,Player:%s,Placed:%r"\
                       (self._colour,self._tile,self._player,self._placed))

    #Set the colour of the meeple
    def setColour(self,colour):
        self._colour = colour

    #Returns the colour of the meeple
    def getColour(self):
        return self._colour

    #Puts the meeple on a tile
    def setTile(self,tile):
        self._tile = tile

    #Returns the tile that the meeple is on
    def getTile(self):
        return self._tile

    #Associates the meeple with a player
    def setPlayer(self,player):
        self._player = player

    #Retunrs the player using the meeple.
    def getPlayer(self):
        return self._player

    #If a meeple is placed on a tile this sets placed to True
    def place(self):
        self.placed = True

    def take_back(self):
        self.placed = False