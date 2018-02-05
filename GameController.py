from grid import *
from tile import *
from tileTypes import *
from landmark import *


# list of changes made:
# 1) Made cities and landmarks joinable
# 2) Started on GameController class
# 3) Added _xPos and _yPos attributes back into Tile class + tile.setPosition(x, y)
# 4) Added getTile method to Grid (give xPos and yPos, it returns tile there or None)
# 5) Had to alter the city/road initialisers in tileTypes for the new landmark._tiles to work

class GameController:

	def __init__(self):
		#Note: Only added in the functionality I needed for the isLandmarkComplete
		self._grid = Grid(InitialTile())
	
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

