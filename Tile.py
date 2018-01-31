#Super class to represent 'Tile' object
#Author: Eimear , Stephen
#Version: 3


class Tile:
    def __init__(self, id, top, right, left, bottom):
        #Corresponding ID in database of tile graphics
        self._id = id
        #Represents the meeple object placed on tile or None if no meeple on this tile
        self._meeple = None
        #Represents where on tile the meeple object has been placed i.e. [landmark, side]
        self._meeple_placement = [None, None]
        #Orientation attributes for tile rotation
        self._top = top #Landmark object
        self._right = right #Landmark object
        self._bottom = bottom #Landmark object
        self._left = left #Landmark object

    def rotateTile(self):
        #Rotates tile clockwise as user desires it
        l = self._left
        self._left = self._top
        self._top = self._right
        self._right = self._bottom
        self._bottom = l 
        print("Tile rotation: T:%s, R:%s, B:%s, L:%s" % (self._top, self._right, self._bottom, self._left))

    def getTile(self):
        return self
    
def main():
    tile = Tile(1, "City", "City", "City", "Grass")
    tile.rotateTile()
    tile.rotateTile()

if __name__ == "__main__":
    main()
