class Landmark:
    """A superclass to represent a landmark such as a road etc
    Each tile can have 4 landmarks - one for each side.
    Mulitple sides can point to the same landmark
    e.g. a diagonal city tile has the top and right both point to the same city"""
    
    def __init__(self, score, meeple=None):
        """Score represent how many points this landmark is worth.
        meeple is a reference to the meeple placed on the item."""
        self._score = score
        self._meeple = meeple

    def getScore(self):
        """returns the score of the landmark."""
        return self._score

    def placeMeeple(self, meeple):
        """places a meeple on the landmark."""
        self._meeple = meeple


class Road(Landmark):
    def __init__(self, roadId, isRoadEnd=False):
        """A road piece is worth a score of 1
        isRoadEnd is a boolean to represent that this road has an end
        e.g in tile with a village, the road landmarks end in the village"""
        score = 1
        Landmark.__init__(self, roadId, score)
        self._isRoadEnd = isRoadEnd

    def isRoadEnd(self):
        """Returns True if road has an end."""
        return self._isRoadEnd


class City(Landmark):
    def __init__(self, cityId, hasCrest=False):
        """Cities have scores of 2, or 4 if they have a crest"""
        score = 2
        if hasCrest:
            score += 2
        Landmark.__init__(self, score)
        self._hasCrest = hasCrest

    def hasCrest(self):
        """Returns true if city has a crest"""
        return self._hasCrest
    

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
        
