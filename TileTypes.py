from TileV1 import Tile

#1
#Subclass to represent a specific tile type. This is the starting tile for the game.
#This piece has a straight road and a city cap and a grassy area either side of
#There 1 tile of this type
class IntialTile(Tile):
    def __init__(self):
        #Inherits from 'Tile' super class
        super(Tile, self).__init__()
        self.landmark = [['C', 'C', 'C'], ['R', 'R', 'R'], ["G", "G", "G"]]

    def getTile(self):
        super(Tile, self).getTile()

#2
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

#3
#Subclass to represent a specific tile type, a city cap 
#City cap tiles have one side as a city pieces, and the rest grass
#There are 5 tiles of this type
class CityCapTile(Tile):s
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["G", "G", "G"],["G", "G", "G"]]

    def getTile(self):
        super(Tile, self).getTile()

#4
#Subclass to represent a specific tile type, a city cap with a road bending to the left
#It has a city cap on one side, and an L road leading to the left
#There are 3 tiles of this type
class CapLeftBend(Tile):s
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["R", "R", "G"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#5
#Subclass to represent a specific tile type, a city cap with a road bending to the left
#It has a city cap on one side, and an L road leading to the right
#There are 3 tiles of this type
class CapRightBend(Tile):s
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["G", "R", "R"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#6
#Identical to the InitialTile class
#There are 3 tiles of this type
class CapStraightRoad(Tile):s
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],['R', 'R', 'R'], ["G", "G", "G"]]

    def getTile(self):
        super(Tile, self).getTile()

#7
#Subclass to represent a specific tile type, a city cap with a T-junction opposite it
#It has a city cap on one side, and an T-junction
#There are 3 tiles of this type
class CapTJunction(Tile):s
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["R","R","R"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#8
#Subclass to represent a specific tile type, 2 city caps opposite each other
#It has 2 city cap parallel to each other
#There are 3 tiles of this type
class OppositeCaps(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","G","C"],["C","G","C"],["C","G","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#9        
#Subclass to represent a specific tile type, 2 city caps adjacent to each other
#It has 2 city cap perpendicular to each other
#There are 2 tiles of this type
class AdjacentCaps(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["G","G","C"],["G","G","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#10
#Subclass to represent a specific tile type, one city cap that encompasses 2 sides 
#It has 1 city cap, over on the north and west sides, with the rest being grass
#There are 3 tiles of this type
class DiagonalCap(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","G"],["C","G","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#11
#Same as DiagonalCap but has a crest
#There are 2 tiles of this type
class DiagonalCapCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","G"],["C","G","G"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#12
#Subclass to represent a specific tile type, one city cap that encompasses 2 sides, with a road on the remaining side
#It has 1 city cap, over on the north and west sides, with the rest being grass
#There are 3 tiles of this type
class DiagonalRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","R","R"],["C","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#13
#Same as DiagonalRoad but has a crest
#There are 2 tiles of this type
class DiagonalRoadCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","G"],["C","G","G"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#14
#Subclass to represent a specific tile type, one city cap that encompasses 3 sides, with grass on the remaining side
#It has 1 city cap, over on the north, west and east sides, with the rest being grass
#There are 3 tiles of this type
class ThreeSidedCap(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","G","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#15
#Same as ThreeSidedCap but has a crest
#There is 1 tile of this type
class ThreeSidedCapCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","G","C"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#16
#Same as ThreeSidedCap but has a road space instead of a "G" space
#There is 1 tile of this type
class ThreeSidedCapRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","R","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#17
#Same as ThreeSidedCapRoad but has a crest
#There are 2 tile of this type
class ThreeSidedCapRoadCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","R","C"]]
        self.crest = True

    def getTile(self):
        super(Tile, self).getTile()

#18
#Subclass to represent the Monastery tile
#It has a monastery tile in the center of the piece, and nothing else
#There are 4 tiles of this type
class Monastery(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G", "G", "G"],["G","C","G"],["G","G","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#19
#Same as Monastery but has a road leading up to it
#There are 2 tile of this type
class MonasteryRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G", "G", "G"],["G","C","G"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#20
#Subclass to represent a specific tile type, a town with 4 roads leading out from it
#It has a 4-way crossroad with a town at its center
#There is 1 tiles of this type
class FourWayCrossroad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G","R","G"],["R","C","R"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#21
#Same as 4WayCrossroad but doesn't have the northern road
#There are 4 tile of this type
class TownTJunction(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G","G","G"],["R","C","R"],["G","R","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#22
#Subclass to represent a specific tile type, a tile with a straight road
#It has a road connecting 2 side parallel to each other
#There are 8 tiles of this type
class StraightRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G", "R", "G"],["doesn't have the northern roadG", "R", "G"],["G", "R", "G"]]

    def getTile(self):
        super(Tile, self).getTile()

#23
#Subclass to represent a specific tile type, a tile with an L road
#It has a road connecting 2 sides perpendicular to each other
#There are 9 tiles of this type
class LRoad(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["G","R","G"],["R","R","G"],["G","G","G"]]

    def getTile(self):
        super(Tile, self).getTile()

#24
#Subclass t#21
#Same as 4WayCrossroad but doesn't have the northern road
#There are 4 tile of this typeo represent a specific tile type, a city tile connecting 2 opposite sides
#It has a city connecting 2 sides perpendicular to each other, with the rest being grass
#There is 1 tile of this type
class CityCone(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","G","C"],["C","C","C"],["C","G","C"]]

    def getTile(self):
        super(Tile, self).getTile()

#21
#Same as CityCone but crested
#There are 2 tiles of this type
class CityConeCrest(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","G","C"],["C","C","C"],["C","G","C"]]
        self._crest = True

    def getTile(self):
        super(Tile, self).getTile()

class TemplateTile(Tile):
    def __init__(self):
        super(Tile, self).__init__()
        self.landmark = [["C","C","C"],["C","C","C"],["C","C","C"]]

    def getTile(self):
        super(Tile, self).getTile()
