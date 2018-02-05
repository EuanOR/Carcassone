from grid import *
from tile import *
from tileTypes import *
from landmark import *


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

