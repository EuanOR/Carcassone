#Super class to represent 'Tile' object
#Author: Eimear , Stephen
#Version: 3


class Tile:
    def __init__(self, id, top, left, right, bottom, image=None):
        #Corresponding ID in database of tile graphics
        self._id = id
        #Represents the meeple object placed on tile or None if no meeple on this tile
        self._meeple = None
        #Represents where on tile the meeple object has been placed i.e. side
        self._meeple_placement = None
        #Reference to image src
        self._image = image
        #Orientation attributes for tile rotation
        self._top = top #Landmark object
        self._right = right #Landmark object
        self._bottom = bottom #Landmark object
        self._left = left #Landmark object
        self._xPos = None #x-position on grid
        self._yPos = None #y-position on grid
        self._degreeRotated = 0 #to show how the image should be displayed
       
    def setPosition(self, x, y):
        #Sets the x and y position of the tile on the grid
        self._xPos = x
        self._yPos = y

    def rotateTile(self):
        #Rotates tile clockwise as user desires it
        self._degreeRotated = (self._degreeRotated + 90) % 360
        l = self._left
        self._left = self._bottom
        self._bottom = self._right
        self._right = self._top
        self._top = l 
        #print("Tile rotation: T:%s, R:%s, B:%s, L:%s" % (self._top, self._right, self._bottom, self._left))

    def getTile(self):
        return self
    
def main():
    tile = Tile(1, "City", "City", "City", "Grass")
    tile.rotateTile()
    tile.rotateTile()

if __name__ == "__main__":
    main()
