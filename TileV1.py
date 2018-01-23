#Super class to represent 'Tile' object
#Author: Eimear
#Version: 2

from copy import deepcopy

class Tile:
    def __init__(self):
        #Represents the meeple object placed on tile or None if no meeple on this tile
        self.meeple = None
        #Represents where on tile the meeple object has been placed i.e. self.landmark[0][1] or None if no meeple on this tile
        self.meeple_placement = None
        #Treats tile as a 9-block grid in order to match placement of meeple to correct landmark
        #E.g. where 'C' = city, 'R' = road etc.
        self.landmark = [[None, None, None],[None, None, None],[None, None, None]]
        #Orientation attributes for tile rotation
        self.top = 'top'
        self.right = 'right'
        self.bottom = 'bottom'
        self.left = 'left'

    def rotateMatrix(self, matrix):
        #Rotates matrix of landmarks as the tile is rotated
        n = len(matrix)
        res = deepcopy(matrix)
        for x in range(0,n):
            for y in range(n-1, -1, -1):
                res[x][n-y-1] = matrix[y][x]
        return res

    def rotateTile(self):
        #Rotates tile clockwise as user desires it
        l = self.left
        self.left = self.top
        self.top = self.right
        self.right = self.bottom
        self.bottom = l 
        self.landmark = self.rotateMatrix(self.landmark)
        print(self.landmark)
        print("Tile rotation: T:%s, R:%s, B:%s, L:%s" % (self.top, self.right, self. bottom,self.left))

    def getTile(self):
        return self

#Sub class to represent the intial tile to start the game
class IntialTile(Tile):
    def __init__(self):
        #Inherits from 'Tile' super class
        super(Tile, self).__init__()
        self.landmark = [['C', 'C', 'C'], ['R', 'R', 'R'], [None, None, None]]

    def getTile(self):
        super(Tile, self).getTile()
    
def main():
    tile = Tile()
    tile.rotateTile()
    tile.rotateTile()
    start_tile = IntialTile()
    print(start_tile.landmark)

if __name__ == "__main__":
    main()
