class Landmark:
    """A superclass to represent a landmark such as a road etc
    Each tile can have 4 landmarks - one for each side.
    Mulitple sides can point to the same landmark
    e.g. a diagonal city tile has the top and right both point to the same city"""
    
    def __init__(self, score, tiles=[], meeples=[]):
        """Score represent how many points this landmark is worth.
        meeple is a list of meeples placed on the landmark.
        tiles is a list of tiles the landmark is on."""
        self._score = score
        self._meeples = meeples
        self._tiles = tiles

    def getScore(self):
        """Returns the score of the landmark."""
        return self._score

    def setScore(self, score):
        self._score = score

    def placeMeeple(self, meeple):
        """Places a meeple on the landmark."""
        self._meeples.append(meeple)

    def getTiles(self):
        """Returns the list of tiles the landmark is on."""
        return self._tiles

    @staticmethod
    def join(landmark1, landmark2):
        """Joins this landmark with another landmark of the same type, making a larger landmark.
        This should be called by GameController when a tile is placed."""
        raise NotImplementedError("Should be implemented in subclass.")

    @staticmethod
    def reassignSides(newLandmark, tiles, old1, old2):
        """To be used as part of join in the landmark subclasses.
        Reassigns the sides of tiles in list 'tiles' 
        from landmarks old1 or old2 to newLandmark"""
        for tile in tiles:
            if tile._left == old1 or tile._left == old2:
                tile._left = newLandmark
            if tile._right == old1 or tile._right == old2:
                tile._right = newLandmark
            if tile._top == old1 or tile._top == old2:
                tile._top = newLandmark
            if tile._bottom == old1 or tile._bottom == old2:
                tile._bottom = newLandmark


class Road(Landmark):
    def __init__(self, tiles, endCount=0):
        """A road piece is worth a score of 1
        endCount is an integer to represent how many ends the road has
        e.g if a road  begins in one village and ends in another, endCount = 2 and it's complete"""
        score = 1
        self._endCount = endCount
        Landmark.__init__(self, score, tiles)

    def __str__(self):
        ret_str = "Score=%i, EndCount=%i, Tiles=%s" %(self._score, self._endCount, self._tiles)
        return ret_str

    def getEndCount(self):
        """Returns how many ends the road has."""
        return self._endCount

    @staticmethod
    def join(road1, road2):
        """Join this road with another road, making a longer road.
        This should be called by GameController when a tile is placed."""
        resScore = road1._score + road2._score
        resMeeples = road1._meeples + road2._meeples
        resTiles = road1._tiles + road2._tiles
        resEndCount = road1._endCount + road2._endCount
        
        resultRoad = Road(resTiles, resEndCount)
        resultRoad._meeples = resMeeples
        resultRoad._score = resScore

        Landmark.reassignSides(resultRoad, resTiles, road1, road2)


class City(Landmark):
    def __init__(self, tiles, crestCount=0):
        """Cities have scores of 2, or 4 if they have a crest"""
        score = 2 + (2*crestCount)
        Landmark.__init__(self, score, tiles)
        self._crestCount = crestCount

    def crestCount(self):
        """Returns true if city has a crest"""
        return self._crestCount

    def isComplete(self):
        """Returns True if the city is complete."""
        #for tile in self._tiles:
            #for side on tile
                #if side in city
                    #get tile adjacent to that side
                    #if adjacent tile NOT in self._tiles:
                        #return False
        #return True
        for tile in self._tiles:
            if tile._left == self:
                pass
            if tile._right == self:
                pass
            if tile._bottom == self:
                pass
            if tile._top == self:
                pass

    @staticmethod
    def join(city1, city2):
        """Join this road with another city, making a bigger city.
        This should be called by GameController when a tile is placed."""
        resScore = city1._score + city2._score
        resMeeples = city1._meeples + city2._meeples
        resTiles = city1._tiles + city2._tiles
        resCrestCount = city1._crestCount + city2._crestCount

        resultCity = City(resTiles, resCrestCount)
        resultCity._meeples = resMeeples
        resultCity._score = resScore

        Landmark.reassignSides(resultCity, resTiles, city1, city2)
    

class Grass(Landmark):
    """Just to represent the grass."""
    def __init__(self):
        score = 0
        Landmark.__init__(self, score)

    
#--- May or may not be added in at a later stage. ---#
class Monastery(Landmark):
    def __init__(self):
        """Monasteries have a score of 9 when completed."""
        score = 9
        Landmark.__init__(self, score)
        
