class Meeple(object):

    def __init__(self,player):
        self._colour = self._player.getColour()
        self._player =  player
        self._placed = False

    def __str__(self):
        outstr = ""
        outstr += ("Meeple Colour :%s\n Meeple Player :%s\nMeeple Placed :%b",(self._colour,self._player._name,self._placed))
        return outstr

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
