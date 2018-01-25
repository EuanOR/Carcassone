#Super class to represent 'Tile' object
#Author: Eimear , Stephen
#Version: 2.1

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
        self.crest = False
        self._xpos=None
        self._ypos=None

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
    
    #Places a tile on the grid and asks the user if they would like to play their meeple.
    def placeTile(self,x,y,grid):
        self._xpos=x
        self._ypos=y
        grid.insertTile(self, x, y, tile)
        if self._landmark[0][0]!=None or self._landmark[0][1]!=None or self._landmark[0][2] != None:
            userIn=input("Do you want to place your Meeple on top of this tile?") # Can edit this to display what is on the tile using string formatting i.e do you want to place on the road.
            if UserIn=="yes":
                if len(self._player._meeples)!=0:
                    self._Meeple=self._player._meeple[0] #Assuming player has a meeple list
                    for i in self._landmark[0]:
                        if i != None: #Only one can be a landmark?
                            self.meeple_placement=i
                            return self
                else:
                    print("Sorry no more Meeples available")
                    return self
            else:
                if self._landmark[1][0]!=None or self._landmark[1][1]!=None or self._landmark[1][2] != None:
                userIn=input("Do you want to place your Meeple in the middle of this tile?") # Can edit this to display what is on the tile using string formatting i.e do you want to place on the road.
                if UserIn=="yes":
                    if len(self._player._meeples)!=0:
                        self._Meeple=self._player._meeple[0] #Assuming player has a meeple list
                        for i in self._landmark[1]:
                            if i != None: #Only one can be a landmark?
                                self.meeple_placement=i
                                return self
                    else:
                        print("Sorry no more Meeples available")
                        return self
            if self._landmark[2][0]!=None or self._landmark[2][1]!=None or self._landmark[2][2] != None:
            userIn=input("Do you want to place your Meeple on top of this tile?") # Can edit this to display what is on the tile using string formatting i.e do you want to place on the road.
            if UserIn=="yes":
                if len(self._player._meeples)!=0:
                    self._Meeple=self._player._meeple[0] #Assuming player has a meeple list
                    for i in self._landmark[0]:
                        if i != None: #Only one can be a landmark?
                            self.meeple_placement=i
                            return self
                else:
                    print("Sorry no more Meeples available")
                    return self
        return grid
    
    #Return the owner of the meeple which occupies the tile
    def getMeepleOwner(self):
        if self._meeple_placement!=None:
            return self._meeple__placement._player
    
           
                  
     
    
def main():
    tile = Tile()
    tile.rotateTile()
    tile.rotateTile()
    start_tile = IntialTile()
    print(start_tile.landmark)

if __name__ == "__main__":
    main()
