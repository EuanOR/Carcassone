from Tile import *
from TileTypes import *

"""
    A new version of Grid, instead of using 2D array we will now use a sparse array. [ [ [x1, y1], TileObject], [ [x2, y2], TileObject] ]

    For example if we have a initial tile on the board, we will have a list
    that will look like this -> [ [ [0, 0], InitialTileObject ] ]. 
    If we place another tile ontop of the initial tile we will have [ [ [0, 0], initialTileObject] , [ [0, -1], Tile2Object] ]

    We have a checkAvailbility function which will return a list with all the open locations on the grid. 
    This function does not valid the tile placement yet, for example checking if the road on Tile1 matches the road on Tile2.
    [[0, -1], [1, 0], [0, 1], [-1, 0]]  is an example of the open locations of the initial tile. Each location is held in a list with x coord and y coord

"""
class Grid:
    def __init__(self, tile):
        self._grid = []

        # Used for center location of the tile -> [0,0]
        self._center = 0
        self._initialTile = tile

        # A list where it holds all the open locations.
        self._openLocation= []
        self.createGrid()

    def __str__(self):
        return str(self._grid)

    # Creates grid and places initial tile in center of grid
    def createGrid(self):
        self.insertTile(self._center, self._center, self._initialTile)
        return self._grid

    # Places tile at grid location x, y
    def insertTile(self, x, y, tile):

        self.checkAvailability()
        self._grid += [[[x,y], tile]]
        self.checkAvailability()

        # After placing the tile remove it from open location array
        if [x,y] in self._openLocation:
            self._openLocation.remove([x,y])

    # Returns a list of open location valid locations on the grid
    def checkAvailability(self):

        tempResultArray = []
        for placedTile in self._grid:

            # placeTileX contains the x value, these variable is used so the code looks neater
            placedTileX = placedTile[0][0]
            placedTileY = placedTile[0][1]

            # Calculating the top, right, bottom, left tile co-ordinates
            top = [placedTileX, placedTileY - 1]
            right = [placedTileX + 1, placedTileY]
            bottom = [placedTileX, placedTileY + 1]
            left = [placedTileX - 1, placedTileY]

            # Checking if it is free tile, if it is free tile then add it to resultArray.
            if top != placedTile and top not in self._openLocation and top not in tempResultArray and top != [0,0]:
                tempResultArray += [top]
            if right != placedTile and right not in self._openLocation and right not in tempResultArray and right != [0,0]:
                tempResultArray += [right]
            if bottom != placedTile and bottom not in self._openLocation and bottom not in tempResultArray and bottom != [0,0]:
                tempResultArray += [bottom]
            if left != placedTile and left not in self._openLocation and left not in tempResultArray and left != [0,0]:
                tempResultArray += [left]

        self._openLocation = tempResultArray
        return(self._openLocation)

def main():
    initialTile = IntialTile()
    grid = Grid(initialTile)

    print(grid._openLocation)
main()
