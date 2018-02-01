class Meeple(object):
 """Creates a meeple Object
    01/02/18 - Stephen and Euan
 """
    
  
    """Initiates a Meeple Object.
       player points to the player object which "owns" the Meeple
       placed is a boolean which represents if the Meeple is placed on the board or not
       colour is a string which represents the Meeple's colour, this is found using the Player's getColour method"""
    def __init__(self,player):
        self._player =  player
        self._placed = False
        self._colour = self._player.getColour()
    
    #Creates a string representation for a Meeple
    def __str__(self):
        outstr = ""
        outstr += ("Meeple Colour :%s\nMeeple Player :%s\nMeeple Placed :%r"%(self._colour,self._player._name,self._placed))
        return outstr

    #Returns the colour of the meeple
    def getColour(self):
        return self._colour

    #Retunrs the player using the meeple.
    def getPlayer(self):
        return self._player

    #If a meeple is placed on a tile this sets placed to True
    def place(self):
        self._placed = True
        
    #If a meeple is removed from a tile this sets placed to False
    def take_back(self):
        self._placed = False

"""Meeple needs to be tested within the Player class, as a Meeple cannot be created without a player object
   The following is the Meeples test suite.
   
   if __name__=="__main__":
    Player1=Player("Brian")
    Player1.setColour("Green")
    Meeple1=Meeple(Player1)
    colourTest=Meeple1.getColour()
    print(colourTest)
    playerTest=Meeple1.getPlayer()
    print(playerTest)
    Meeple1.place()
    print(Meeple1)
    Meeple1.take_back()
    print(Meeple1)
    
 """
