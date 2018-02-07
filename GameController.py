from grid import *
from Meeple import *
from TileTypes import *
from DeckOfTiles import *
from landmark import *

class GameController:

    def __init__(self):
        #Note: Only added in the functionality I needed for the isLandmarkComplete
	self._grid = Grid()
        self._players = []
        self._playing = 0 #This is an index pointing to current player in self._playing not a counter of players in game
        self._gameOver = False
        self._deck = DeckOfTiles()
        self._turns = 0
        self._maxTurns = 10*len(self._players)
    
    #Just the bones of how the game could go through each turn
    #Each player has a turn and places a tile and a meeple until the game is over
    #def play(self):
        #while not self._gameOver:
            #for p in self._players:
                #self._playing = player

    """def turn(self):
        turnsTile = self._deck.pop()
        #send the tile to the player
        #send the available locations to the player
        #receive the information when the player rotates the tile
        #receive the selected location from the player
        #validate the selected location
        #if valid, place the tile
        #check the sides to join landmarks
        #if meeples to place, place meeples
        self._turns += 1
        self._playing = self._players[self._turns%len(self._players)]"""


    def start_game(self):
        self._playing = self._players[0]
        while self._turns < self._maxTurns:
            self.turn()
        
    def joinGame(self,player):
        if len(self._players) < 4:
            self._players.append(player)
            self._max_turns = len(self._players)*10
	
    def isLandmarkComplete(self, landmark):
        """Returns True if the landmark 'landmark' is complete."""
    	if isinstance(landmark, City):
            return self.isCityComplete(landmark)
    	elif isinstance(landmark, Road):
            return self.isRoadComplete(landmark)
    	else:
            raise NotImplementedError("Unknown landmark type")

    def isRoadComplete(self, road):
        """Returns True if the road 'road' is complete."""
    	return road.getEndCount() == 2

    def isCityComplete(self, city):
        """Returns True if the city 'city' is complete."""
    	tiles = city.getTiles()
    	for tile in tiles:
    	    if tile._left == city:
                neighbour = self._grid.getTile(tile._xPos-1, tile._yPos)
                if neighbour not in tiles:
                    return False
	    if tile._right == city:
                neighbour = self._grid.getTile(tile._xPos+1, tile._yPos)
                if neighbour not in tiles:
                    return False
            if tile._top == city:
                neighbour = self._grid.getTile(tile._xPos, tile._yPos-1)
                if neighbour not in tiles:
                    return False
            if tile._bottom == city:
    		neighbour = self._grid.getTile(tile._xPos, tile._yPos+1)
    		if neighbour not in tiles:
                    return False
	return True
    
    def getNeighbour(self, tile, direction):
        """Returns a neighbour of tile 'tile'
        direction is a string to specify which neighbour 
        eg "left" for the neighbouring tile on the left"""
        if direction == "left":
            return self._grid.getTile(tile._xPos-1, tile._yPos)
        if direction == "right":
            return self._grid.getTile(tile._xPos+1, tile._yPos)
        if direction == "top":
            return self._grid.getTile(tile._xPos, tile._yPos-1)
        if direction == "bottom":
            return self._grid.getTile(tile._xPos, tile._yPos+1)

    def finishLandmark(self, landmark):
        """Frees up meeples and assigns scores to players."""
        owners = {}
        for tile in landmark.getTiles():
            if tile._meeple_placement == landmark:
                #record meeple count for owner
                owner = tile._meeple.getPlayer()
                owners[owner] = owners.get(owner, 0) + 1

                #clear meeples from tile + player
                owner._activeMeeples.remove(tile._meeple)
                owner._inactiveMeeples.append(tile._meeple)
                tile._meeple._placed = False

                tile._meeple = None
                tile._meeple_placement = None

                #should I remove the meeple from landmark??
                #i dont think not removing it makes any odds 
                #because when its finished its not like you can shove anything else on?

        #determine player(s) had the most meeples on the landmark
        winners = []
        max_meeples = 0
        for p in owners:
            if owners[p] > max_meeples:
                max_meeples = owners[p]
                winners = [p]
            elif owners[p] == max_meeples:
                winners.append(p)

        #give them the points for the landmark
        for winner in winners:
            winner._score += landmark.getScore()

    def join(self, landmark1, landmark2):
        """Joins two landmarks."""
        if isinstance(landmark1, City):
            if not isinstance(landmark2, City):
                return
            City.join(landmark1, landmark2)
        elif isinstance(landmark1, Road):
            if not isinstance(landmark2, Road):
                return
            Road.join(landmark1, landmark2)

    def getTileSide(self, tile, side):
        #just to reduce duplicate code with getting sides!
        #might move to tile class later on? it seems a little messy here???
        if side == "left":
            return tile._left
        elif side == "right":
            return tile._right
        elif side == "top":
            return tile._top
        elif side == "bottom":
            return tile._bottom

    def placeTile(self,tile,x,y):
        """Place a tile on the grid."""
        #list to make iterating with getTileSide easier
        sides = ["left", "right", "top", "bottom"]
        #dict to make getting the opposide side easier
        opposite = {"left": "right", "right":"left", "top":"bottom", "bottom":"top" }
        
        if not self._grid.insertTile(x,y,tile):
            raise InvalidTilePlacementException("insertTile failed")

        for side in sides:
            if not isinstance(self.getTileSide(tile, side), Grass):
                neighbour = self.getNeighbour(tile, side)
                if neighbour != None:
                    #join the side of the tile to the touching side of the neighbour
                    self.join(self.getTileSide(tile, side), self.getTileSide(neighbour, opposite[side]))
                    if self.isLandmarkComplete(self.getTileSide(tile, side)):
                        #this gets score, frees up meeples etc
                        self.finishLandmark(self.getTileSide(tile, side))
        # returns a list of valid places to place a meeple (to be used with placeMeeple()
	validMeeplePlacements = []
        for side in sides:
            landmark = self.getTileSide(tile, side)
            if (not self.isLandmarkComplete(landmark)) and landmark._meeples == []:
                validMeeplePlacements.append(landmark)
        return validMeeplePlacements

    def placeMeeple(self,tile,user_choice):
        #This function places a Meeple on a landmark
        #Assuming user choice is a side (i.e tile._top)
        player=self._players[self._playing]
        if not isinstance(user_choice, Grass):
            if player.meeplesAvailable() > 0:
                meeple=player.getMeeple()
                tile._meeple=meeple
                tile._meeple_placement=user_choice
                user_choice.placeMeeple(meeple)
            else:
                print("No available Meeples")
        else:
            print("Cannot place on grass")

def main():
    end1 = FourWayCrossroad()
    end2 = FourWayCrossroad()
    gc = GameController()
    Brian = Player("Brian")
    Brian.createMeeples()
    gc.joinGame(Brian)

    meeple_placements = gc.placeTile(end1, -1, 0)
    
    gc.placeMeeple(end1, end1._right)
    gc.placeTile(end2, 1, 0)
    
    print("Brian's score=", Brian._score)

if __name__ == "__main__":
    main()
