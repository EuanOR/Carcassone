from TileV1 import Tile

#Subclass to represent a specific tile type. This is the starting tile for the game.
#This piece has a straight road and a city cap and a grassy area either side of
#There 1 tile of this type
class IntialTile(Tile):
    def __init__(self):
        #Inherits from 'Tile' super class
        super(Tile, self).__init__()
        self.landmark = [['C', 'C', 'C'], ['R', 'R', 'R'], [None, None, None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a city
#City tiles are entirely city pieces
#There 1 tile of this type (which is crested)
class CityTile(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","C","C"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a city cap 
#City cap tiles have one side as a city pieces, and the rest grass
#There are 5 tiles of this type
class CityCapTile(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],[None, None, None],[None, None, None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a city cap with a road bending to the left
#It has a city cap on one side, and an L road leading to the left
#There are 3 tiles of this type
class CapLeftBend(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["R", "R", None],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a city cap with a road bending to the left
#It has a city cap on one side, and an L road leading to the right
#There are 3 tiles of this type
class CapRightBend(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],[None, "R", "R"],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Identical to the InitialTile class
#There are 3 tiles of this type
class CapStraightRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],['R', 'R', 'R'], [None, None, None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a city cap with a T-junction opposite it
#It has a city cap on one side, and an T-junction
#There are 3 tiles of this type
class CapTJunction(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["R","R","R"],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, 2 city caps opposite each other
#It has 2 city cap parallel to each other
#There are 3 tiles of this type
class OppositeCaps(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C",None,"C"],["C",None,"C"],["C",None,"C"]]

    def getTile(self):
        super(Tile, self).getTile()
        
#Subclass to represent a specific tile type, 2 city caps adjacent to each other
#It has 2 city cap perpendicular to each other
#There are 2 tiles of this type
class AdjacentTile(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],[None,None,"C"],[None,None,"C"]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, one city cap that encompasses 2 sides 
#It has 1 city cap, over on the north and west sides, with the rest being grass
#There are 3 tiles of this type
class DiagonalCap(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C",None],["C",None,None]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as DiagonalCap but has a crest
#There are 2 tiles of this type
class DiagonalCapCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C",None],["C",None,None]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, one city cap that encompasses 2 sides, with a road on the remaining side
#It has 1 city cap, over on the north and west sides, with the rest being grass
#There are 3 tiles of this type
class DiagonalRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","R","R"],["C","R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as DiagonalRoad but has a crest
#There are 2 tiles of this type
class DiagonalRoadCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C",None],["C",None,None]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, one city cap that encompasses 3 sides, with grass on the remaining side
#It has 1 city cap, over on the north, west and east sides, with the rest being grass
#There are 3 tiles of this type
class ThreeSidedCap(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C",None,"C"]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as ThreeSidedCap but has a crest
#There is 1 tile of this type
class ThreeSidedCapCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C",None,"C"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#Same as ThreeSidedCap but has a road space instead of a None space
#There is 1 tile of this type
class ThreeSidedCapRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","R","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as ThreeSidedCapRoad but has a crest
#There are 2 tile of this type
class ThreeSidedCapRoadCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","R","C"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent the Monastery tile
#It has a monastery tile in the center of the piece, and nothing else
#There are 4 tiles of this type
class Monastery(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None, None, None],[None,"C",None],[None,None,None]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as Monastery but has a road leading up to it
#There are 2 tile of this type
class MonasteryRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None, None, None],[None,"C",None],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a town with 4 roads leading out from it
#It has a 4-way crossroad with a town at its center
#There is  tiles of this type
class WayCrossroad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None,"R",None],["R","C","R"],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Same as 4WayCrossroad but doesn't have the northern road
#There are 4 tile of this type
class TJunction(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None,None,None],["R","C","R"],[None,"R",None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a tile with a straight road
#It has a road connecting 2 side parallel to each other
#There are 8 tiles of this type
class StraightRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None, "R", None],[None, "R", None],[None, "R", None]]

    def getTile(self):
        super(Tile, self).getTile()

#Subclass to represent a specific tile type, a tile with an L road
#It has a road connecting 2 sides perpendicular to each other
#There are 9 tiles of this type
class LRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [[None,"R",None],["R","R",None],[None,None,None]]

    def getTile(self):
        super(Tile, self).getTile()

class TemplateTile(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","C","C"]]

    def getTile(self):
        super(Tile, self).getTile()
