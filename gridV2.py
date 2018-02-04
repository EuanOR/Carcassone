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

        # A list where it holds all the placed tiles. 
        self._placedTiles = []
        self.createGrid()

        

    def __str__(self):
        return str(self._grid)

    # Creates grid and places initial tile in center of grid
    def createGrid(self):
        self._grid += [[[self._center,self._center], self._initialTile]]
        self._placedTiles += [[self._center,self._center]]
        self.checkAvailability()
        return self._grid

    # Places tile at grid location x, y
    def insertTile(self, x, y, tile):

        if [x,y] in self._openLocation:
            if (self.isValidLocation([x,y], tile)):
                self._grid += [[[x,y], tile]]
                self._placedTiles += [[x,y]]
                self.checkAvailability()

                # After placing the tile remove it from open location array
                if [x,y] in self._openLocation:
                    self._openLocation.remove([x,y])
                return True
        return False

        # Returns a list of open location valid locations on the grid
    def checkAvailability(self):

        tempResultArray = []
        for placedTile in self._placedTiles:

            # placeTileX contains the x value, these variable is used so the code looks neater
            placedTileX = placedTile[0]
            placedTileY = placedTile[1]

            # Calculating the top, right, bottom, left tile co-ordinates
            top = [placedTileX, placedTileY + 1]
            right = [placedTileX + 1, placedTileY]
            bottom = [placedTileX, placedTileY - 1]
            left = [placedTileX - 1, placedTileY]

            # Checking if it is free tile, if it is free tile then add it to resultArray.
            if top != placedTile and top not in self._placedTiles and top not in tempResultArray:
                tempResultArray += [top]
            if right != placedTile and right not in self._placedTiles and right not in tempResultArray:
                tempResultArray += [right]
            if bottom != placedTile and bottom not in self._placedTiles and bottom not in tempResultArray:
                tempResultArray += [bottom]
            if left != placedTile and left not in self._placedTiles and left not in tempResultArray:
                tempResultArray += [left]

        self._openLocation = tempResultArray
        return(self._openLocation)


    # Returns a Boolean if the location given is valid.
    # If valid, meaning the surrounding tiles matches landmark with the tile. EG road matches road, city matches city.
    def isValidLocation(self, XYList, newTile):

        x = XYList[0]
        y = XYList[1]

        # Calculating the x, y coordiantes of the surrounding new tile.
        topTile = [x, y + 1]
        rightTile = [x + 1, y]
        bottomTile = [x, y - 1]
        leftTile = [x - 1, y]

        for placedTile in self._grid:
            placedTileObject = placedTile[1]

            if topTile == placedTile[0]:
                if type(newTile._top) != type(placedTileObject._bottom):
                    return False

            if rightTile == placedTile[0]:
                if type(newTile._right) != type(placedTileObject._left):
                    return False

            if bottomTile == placedTile[0]:
                if type(newTile._bottom) != type(placedTileObject._top):
                    return False

            if leftTile == placedTile[0]:
                if type(newTile._left) != type(placedTileObject._right):
                    return False
        return True
            

def main():
    initialTile = IntialTile()
    fourWayRoad = FourWayCrossroad()

    grid = Grid(initialTile)

    print(grid.insertTile(1,0,fourWayRoad)) #Adding four way road to the right of initial tile, should return True -> valid location and inside openLocation

    print(grid.insertTile(0,1, fourWayRoad)) # Adding four way road to the top of initial tile, should return False -> incorrect valid location but inside openlocation

    print(grid.insertTile(-1, 0, fourWayRoad)) # Adding four way road to the left of initial tile, should return True -> valid location but inside openLocation

    print(grid.insertTile(0, -1, fourWayRoad)) # Adding four way road to the bottom of initial tile, should return False -> invalid location but inside openLocation

    print(grid.insertTile(10, 10, fourWayRoad)) # Adding four way road to (10,10), should return False -> Not inside openlocation

main()

