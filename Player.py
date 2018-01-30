class Player(object):

    #initialises the player object, only name can be set via this method
    #all other attributes will have default values across all players.
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._activeMeeples = []
        self._inactiveMeeples = []
        self._tiles = []

    #returns the players name
    def getName(self):
        return self._name

    #This method will calculate the score of a finished set of tiles and
    #increment the players score accordingly
    def increaseScore(self):
        pass

    #returns the players current score
    def getScore(self):
        return self._score

    #adds a tile to the list of active tiles a player has
    def addTile(self, tile):
        self._tiles.append(tile)

    #Prompts user to enter colour of their meeples and spawns 9 meeples
    #of that colour and places them in the inactive meeple list
    def createMeeples(self):
        user_colour = input("Please select a colour for your meeples:")
        for _ in range(0,8):
            m = Meeple(user_colour,None,self)
            self._inactiveMeeples.append(m)

    #returns the amount of meeples available
    def meeplesAvailable(self):
        return len(self._inactiveMeeples)

    #returns a meeple for placement if one is available
    def placeMeeple(self):
        if self.meeplesAvailable > 0:
            return self._inactiveMeeples.pop()

        else:
            print("No meeples available for placement; all on board.")
        

    
    
    
