from grid import *
from Meeple import *
from TileTypes import *
from DeckOfTiles import *
from landmark import *
from Player import *

class GameController:

    def __init__(self):
        # Note: Only added in the functionality I needed for the isLandmarkComplete
        self._grid = Grid()
        self._players = []
        self._playing = 0 # This is an index pointing to current player in self._playing not a counter of players in game
        self._gameOver = False
        self._deck = DeckOfTiles()
    
    # Just the bones of how the game could go through each turn
    # Each player has a turn and places a tile and a meeple until the game is over
    # def play(self):
        # while not self._gameOver:
            # for p in self._players:
                # self._playing = player

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


    def startGame(self):
        self._playing = self._players[0]
        while not self._gameOver:
            self.turn()
            self.gameFinished()
   
    def gameFinished(self):
        if self._turns == self._maxTurns:
            self._gameOver = True
            self.finishGame()

    def nextGo(self):
        """Move on to next player's go
        Returns the tile for their go and a list of valid locations to place that tile."""
        self._playing = (self._playing+1)%len(self._players)
        self._turns += 1
        tile = self._deck.drawTile()
        available_tiles = self._grid.returnValidLocations(tile)
        return tile, available_tiles

    def rotateTile(self, tile):
        """Rotates the tile and returns a list of valid locations to place that tile."""
        tile.rotateTile()
        return self._grid.returnValidLocations(tile)

    def finishGame(self):
        """Finshes the game, allocates points for unfinished landmarks, returns winner."""
        # give points for unfinished landmarks
        for pos, tile in self._grid._grid:
            for side in ["left", "right", "top", "bottom"]:
                landmark = self.getTileSide(tile, side)
                if landmark._meeples != []:
                    self.finishLandmark(landmark, endgame=True)
        # get winner(s) of the game        
        winners = []
        max_score = 0
        for player in self._players:
            if player._score > max_score:
                max_score = player._score
                winners = [player]
            elif player._score == max_score:
                winners.append(player)
        return winners
	
    def maximumTurns(self):
        # if self._maxTurns > 71:
        while self._maxTurns > 71:
            self._maxTurnsPP -= 1
            self._maxTurns = self.setMaximumTurns()
       
    def setMaximumTurns(self):
        return self._maxTurnsPP*len(self._players)
	
    def joinGame(self,player):
        if len(self._players) < 4:
            self._players.append(player)
            self.maximumTurns()
	
    def isLandmarkComplete(self, landmark):
        """Returns True if the landmark 'landmark' is complete."""
        if isinstance(landmark, City):
            return self.isCityComplete(landmark)
        elif isinstance(landmark, Road):
            return self.isRoadComplete(landmark)
        elif isinstance(landmark, Grass):
            return True

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

    def finishLandmark(self, landmark, endgame=False):
        """Frees up meeples and assigns scores to players."""
        owners = {}
        for tile in landmark.getTiles():
            if tile._meeple_placement == landmark:
                # record meeple count for owner
                owner = tile._meeple.getPlayer()
                owners[owner] = owners.get(owner, 0) + 1

                # clear meeples from tile + player
                owner._activeMeeples.remove(tile._meeple)
                owner._inactiveMeeples.append(tile._meeple)
                tile._meeple._placed = False
                landmark._meeples.remove(tile._meeple)
                tile._meeple = None
                tile._meeple_placement = None
        # determine player(s) had the most meeples on the landmark
        winners = []
        max_meeples = 0
        for p in owners:
            if owners[p] > max_meeples:
                max_meeples = owners[p]
                winners = [p]
            elif owners[p] == max_meeples:
                winners.append(p)

        # give them the points for the landmark
        for winner in winners:
            if not endgame:
                winner._score += landmark.getScore()
            else:
                winner._score += landmark.getEndgameScore()

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
        # just to reduce duplicate code with getting sides!
        # might move to tile class later on? it seems a little messy here???
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
        # list to make iterating with getTileSide easier
        sides = ["left", "right", "top", "bottom"]
        # dict to make getting the opposide side easier
        opposite = {"left": "right", "right":"left", "top":"bottom", "bottom":"top" }
        
        if not self._grid.insertTile(x,y,tile):
            raise InvalidTilePlacementException("insertTile failed")

        for side in sides:
            if not isinstance(self.getTileSide(tile, side), Grass):
                neighbour = self.getNeighbour(tile, side)
                if neighbour != None:
                    # join the side of the tile to the touching side of the neighbour
                    self.join(self.getTileSide(tile, side), self.getTileSide(neighbour, opposite[side]))
                    if self.isLandmarkComplete(self.getTileSide(tile, side)):
                        # this gets score, frees up meeples etc
                        self.finishLandmark(self.getTileSide(tile, side))
        # returns a list of valid places to place a meeple (to be used with placeMeeple()
        validMeeplePlacements = []
        for side in sides:
            landmark = self.getTileSide(tile, side)
            if (not self.isLandmarkComplete(landmark)) and landmark._meeples == []:
                validMeeplePlacements.append(landmark)
        return validMeeplePlacements

    def placeMeeple(self,tile,user_choice):
        # This function places a Meeple on a landmark
        # Assuming user choice is a side (i.e tile._top)
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
    print(end1._right)
    gc.placeTile(end2, 1, 0)
    print(end1._right)
    print(gc.isLandmarkComplete(end1._right))
    print("Brian's score=", Brian._score)
    print("\n\n")

    #-- city test --#
    gc2 = GameController()
    Anne = Player("Anne")
    Anne.createMeeples()
    gc2.joinGame(Anne)
    
    diag = DiagonalCap()
    diag.rotateTile()
    diag.rotateTile()

    gc2.placeTile(diag, 0, -1)
    gc2.placeMeeple(diag, diag._bottom)

    cap1 = CityCapTile()
    cap1.rotateTile()
    gc2.placeTile(cap1, 1, -1)
    print("\ncap1.leftneighbour=", gc2.getNeighbour(cap1, "left"))
    print("diag._bottom=",  diag._bottom)
    print("diag._right=",  diag._right)
    print("init._top=", gc2._grid.getTile(0,0)._top)
    print("cap1._left= ", cap1._left)
    
    print("Anne's score=", Anne._score)
    


if __name__ == "__main__":
    main()
    #testNextGo()

