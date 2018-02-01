class Meeple(object):
    colours = ["red","blue","green","yellow"]

    def __init__(self,colour,tile,player):
        self._colour = colour
        self._player =  player
        self._placed = False

    def __str__(self):
        outstr = ""
        outstr += ("Colour:%s\nTile:%s\nPlayer:%s\nPlaced:%r"%(self._colour,self._tile,self._player,self._placed))
        return outstr

    #Set the colour of the meeple
    def setColour(self,colour):
        self._colour = self._player._colour

    #Returns the colour of the meeple
    def getColour(self):
        return self._colour

    #Associates the meeple with a player
    def setPlayer(self,player):
        self._player = player

    #Retunrs the player using the meeple.
    def getPlayer(self):
        return self._player

    #If a meeple is placed on a tile this sets placed to True
    def place(self):
        self._placed = True

    def take_back(self):
        self._placed = False

if __name__ == "__main__":
    m = Meeple("Blue","34,21","John")
    print(m)
    print("\n")
    m.place()
    print(m)
