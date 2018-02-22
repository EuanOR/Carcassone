from grid import *
from Meeple import *
from TileTypes import *
from DeckOfTiles import *
from landmark import *
from Player import *

class GameController:

    def __init__(self):
        self._grid = Grid()
        self._players = []
        self._playing = -1 # This is an index pointing to current player in self._playing not a counter of players in game
        self._gameOver = False
        self._deck = DeckOfTiles()
        self._tile = None # tile to be placed in current go
        self._validPlacements = [] # list of places you can place tile
        self._validMeeplePlacements = [] # list of places you can place meeple

        
    def getPlayer(self, playerID):
        """Returns the player with the id playerID"""
        for player in self._players:
            if player._id == playerID:
                return player
        return None

    def getTile(self):
        """Get the tile currently being placed."""
        return self._tile

    def getValidTilePlacements(self):
        """Returns list of coords to place current tile."""
        return self._validPlacements

    def getValidMeeplePlacements(self):
        """Gets list of places to place meeple on current tile."""
        return self._validMeeplePlacements
   
    def gameFinished(self):
        if self._deck.is_empty:
            self._gameOver = True
            self.finishGame()

    def nextGo(self):
        """Begin a new player's go. Also used to begin game. 
        Returns the tile for their go and a list of valid locations to place that tile."""
        self._playing = (self._playing + 1) % len(self._players)
        valid_tile = False
        runThrough = False
        count = 0
        size = self._deck._deck.length()
        self._tile = self._deck.drawTile()
        while not valid_tile:
            if len(self._grid.returnValidLocations(self._tile)) > 0:
                valid_tile = True
            elif len(self._grid.returnValidLocations(self._tile)) == 0:
                for i in range(4):
                    self._tile.rotateTile()
                    if len(self._grid.returnValidLocations(self._tile)) > 0:
                        valid_tile = True

            if not valid_tile:
                self._deck.moveToBottom(self._tile)
                self._tile = self._deck.drawTile()
                count += 1
            if count == size:
                runThrough = True#
                """Functionality for end game needed here.
                If there are no more tiles that can be placed, the game must end at this point.
                Game-ending functions should appear here."""
        self._validPlacements = self._grid.returnValidLocations(self._tile)
        return self._tile, self._validPlacements

    def rotateTile(self):
        """Rotates the tile and returns a list of valid locations to place that tile."""
        self._tile.rotateTile()
        self._validPlacements =  self._grid.returnValidLocations(self._tile)
        return self._validPlacements

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

    def joinGame(self,player):
        """Allow another player should join the game.
        Player should already have created meeples!"""
        if len(self._players) < 4:
            self._players.append(player)
	
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
        if road.getEndCount() == 2:
            return True
        else:
            tiles = road.getTiles()
            for tile in tiles:
                if tile._left == road:
                    neighbour = self._grid.getTile(tile._xPos-1, tile._yPos)
                    if neighbour not in tiles:
                        return False
                if tile._right == road:
                    neighbour = self._grid.getTile(tile._xPos+1, tile._yPos)
                    if neighbour not in tiles:
                        return False
                if tile._top == road:
                    neighbour = self._grid.getTile(tile._xPos, tile._yPos-1)
                    if neighbour not in tiles:
                        return False
                if tile._bottom == road:
                    neighbour = self._grid.getTile(tile._xPos, tile._yPos+1)
                    if neighbour not in tiles:
                        return False
            return True

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

    def placeTile(self,x,y):
        """Place a tile on the grid."""
        # list to make iterating with getTileSide easier
        sides = ["left", "right", "top", "bottom"]
        # dict to make getting the opposide side easier
        opposite = {"left": "right", "right":"left", "top":"bottom", "bottom":"top" }
        
        if not self._grid.insertTile(x,y,self._tile):
            print("Tile insertion failed")

        for side in sides:
            if not isinstance(self.getTileSide(self._tile, side), Grass):
                neighbour = self.getNeighbour(self._tile, side)
                if neighbour != None:
                    # join the side of the tile to the touching side of the neighbour
                    self.join(self.getTileSide(self._tile, side), self.getTileSide(neighbour, opposite[side]))
                    if self.isLandmarkComplete(self.getTileSide(self._tile, side)):
                        # this gets score, frees up meeples etc
                        self.finishLandmark(self.getTileSide(self._tile, side))
        # returns a list of valid places to place a meeple (to be used with placeMeeple()
        self._validPlacements = []
        self._validMeeplePlacements = []
        
        for side in sides:
            landmark = self.getTileSide(self._tile, side)
            if (not self.isLandmarkComplete(landmark)) and landmark._meeples == []:
                self._validMeeplePlacements.append(landmark)
        return self._validMeeplePlacements

    def placeMeeple(self, user_choice):
        # This function places a Meeple on a landmark
        # Assuming user choice is a side (i.e tile._top)
        player=self._players[self._playing]
        if user_choice not in self._validMeeplePlacements:
            print("Not valid")
        if not isinstance(user_choice, Grass):
            if player.meeplesAvailable() > 0:
                meeple=player.getMeeple()
                self._tile._meeple=meeple
                self._tile._meeple_placement=user_choice
                user_choice.placeMeeple(meeple)
            else:
                print("No available Meeples")
        else:
            print("Cannot place on grass")
        self._validMeeplePlacements = []


def main():
    from unittest.mock import MagicMock
    from TileTypes import FourWayCrossroad
    A = Player("Anne")
    A.createMeeples()
    B = Player("Brian")
    B.createMeeples()
    
    gc = GameController()
    gc.joinGame(A)
    gc.joinGame(B)
    gc._deck.drawTile = MagicMock(return_value=FourWayCrossroad())
    print("Game Beginning!")
    print()
    gc.nextGo()
    print(gc._players[gc._playing]._name + "'s go")
    print(gc._tile)
    print(gc.getValidTilePlacements())
    gc.placeTile(1, 0)
    print("Placed FourWayCrossroad at 1, 0")
    print("valid meeple placements=", gc.getValidMeeplePlacements())
    gc.placeMeeple(gc._tile._right)
    print("Placed on left")
    print()
    gc._deck.drawTile = MagicMock(return_value=FourWayCrossroad())
    gc.nextGo()
    print(gc._players[gc._playing]._name + "'s go")
    print(gc._tile)
    print(gc.getValidTilePlacements())
    gc.placeTile(-1, 0)
    print("valid meeple placements=", gc.getValidMeeplePlacements())
    print(A._score)
    gc.placeMeeple(gc._tile._top)

    gc._deck.drawTile = MagicMock(return_value=FourWayCrossroad())
    gc.nextGo()
    print(gc._players[gc._playing]._name + "'s go")
    print(gc._tile)
    print(gc.getValidTilePlacements())
    gc.placeTile(2, 0)
    print(A._score)
    
def main2():
    from unittest.mock import MagicMock
    from TileTypes import StraightRoad, LRoad
    gc = GameController()
    A = Player("A")
    B = Player("B")
    A.createMeeples()
    B.createMeeples()
    gc.joinGame(A)
    gc.joinGame(B)
    
    gc._deck.drawTile = MagicMock(return_value=StraightRoad())
    gc.nextGo()
    gc.rotateTile()
    gc.placeTile(0, 1)
    gc.placeMeeple(gc._tile._left)

    gc._deck.drawTile = MagicMock(return_value=LRoad())
    gc.nextGo()
    gc.placeTile(1, 0)
    gc.placeMeeple(gc._tile._left)

    gc._deck.drawTile = MagicMock(return_value=LRoad())
    gc.nextGo()
    gc.rotateTile()
    gc.placeTile(1, 1)

    gc._deck.drawTile = MagicMock(return_value=LRoad())
    gc.nextGo()
    gc.rotateTile()
    gc.rotateTile()
    gc.placeTile(-1, 1)

    gc._deck.drawTile = MagicMock(return_value=LRoad())
    gc.nextGo()
    gc.rotateTile()
    gc.rotateTile()
    gc.rotateTile()
    gc.placeTile(-1, 0)

    print(A._score)
       
    
    
if __name__ == "__main__":
    main2()
    

    

