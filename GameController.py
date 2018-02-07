import gridv2
import Meeple
import Tile
import TileTypes
from grid import *
from tile import *
from tileTypes import *
from landmark import *

class GameController:

	def __init__(self):
		#Note: Only added in the functionality I needed for the isLandmarkComplete
		self._grid = Grid(InitialTile())
        self._players = []
        self._playing = player
        self._gameOver = False
    
    #Just the bones of how the game could go through each turn
    #Each player has a turn and places a tile and a meeple until the game is over
    #def play(self):
        #while not self._gameOver:
            #for p in self._players:
                #self._playing = player

    def joinGame(self,player):
        self._players.append(player)
	
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
