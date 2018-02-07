from grid import *
from Meeple import *
from TileTypes import *
from DeckOfTiles import *
from landmark import *

class GameController:

    def __init__(self):
        #Note: Only added in the functionality I needed for the isLandmarkComplete
	self._grid = Grid()
        self._players = []
        self._playing = 0 #This is an index pointing to current player in self._playing not a counter of players in game
        self._gameOver = False
        self._deck = DeckOfTiles()
        self._turns = 0
        self._maxTurns = 10*len(self._players)
    
    #Just the bones of how the game could go through each turn
    #Each player has a turn and places a tile and a meeple until the game is over
    #def play(self):
        #while not self._gameOver:
            #for p in self._players:
                #self._playing = player

    """def turn(self):
        turnsTile = self._deck.pop()
        #send the tile to the player
        #send the available locations to the player
        #receive the information when the player rotates the tile
        #receive the selected location from the player
        #validate the selected location
        #if valid, place the tile
        #check the sides to join landmarks
        #if meeples to place, place meeples
        self._turns += 1
        self._playing = self._players[self._turns%len(self._players)]"""


    def start_game(self):
        self._playing = self._players[0]
        while self._turns < self._maxTurns:
            self.turn()
        
    def joinGame(self,player):
        if len(self._players) < 4:
            self._players.append(player)
            self._max_turns = len(self._players)*10
	
    def isLandmarkComplete(self, landmark):
        """Returns True if the landmark 'landmark' is complete."""
    	if isinstance(landmark, City):
            return self.isCityComplete(landmark)
    	elif isinstance(landmark, Road):
            return self.isRoadComplete(landmark)
    	else:
            raise NotImplementedError("Unknown landmark type")

    def isRoadComplete(self, road):
        """Returns True if the road 'road' is complete."""
    	return road.getEndCount == 2

    def isCityComplete(self, city):
        """Returns True if the city 'city' is complete."""
    	tiles = city.getTiles()
    	for tile in tiles:
    	    if tile._left == city:
                neighbour = self._grid.getTile(tile._xPos-1, tile._yPos)
                if neighbour not in tiles:
                    return False
	    if tile._right == city:
                neighbour = self._grid.getTile(tile._xPos+1, tile._yPos)
                if neighbour not in tiles:
                    return False
            if tile._top == city:
                neighbour = self._grid.getTile(tile._xPos, tile._yPos-1)
                if neighbour not in tiles:
                    return False
            if tile._bottom == city:
    		neighbour = self._grid.getTile(tile._xPos, tile._yPos+1)
    		if neighbour not in tiles:
                    return False
	return True
    
    def placeTile(self,tile,x,y):
        self._grid.insertTile(x,y,tile)

    def placeMeeple(self,tile,user_choice):
        #This function places a Meeple on a landmark
        #Assuming user choice is a side (i.e tile._top)
        player=self._players[self._playing]
        if not isinstance(user_choice, Grass):
            if player.meeplesAvailable() > 0:
                meeple=player.getMeeple()
                tile._meeple=meeple
                tile._meeple_placement=user_choice
                user_choice.placeMeeple(meeple)
            else:
                print("No available Meeples")
        else:
            print("Cannot place on grass")
