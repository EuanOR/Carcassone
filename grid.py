from Tile import Tile

# Grid class of size 5 by 5 squares
class Grid:
    def __init__(self, tile, size):
        self._size = size
        self._grid = []
        self._center = self._size // 2
        self._initialTile = tile
        self._count = 0

        self.createGrid()

    # Creates grid and places initial tile in center of grid
    def createGrid(self):
        self._grid = [[0 for y in range(self._size)] for x in range(self._size)]
        self.insertTile(self._center, self._center, self._initialTile)
        return self._grid

    # Places tile at grid location x, y
    def insertTile(self, x, y, tile):
        tile._x = x
        tile._y = y
        tile._order = self._count
        self._grid[x][y] = tile
        self._count += 1
        

    def place_tile(self, board, newtile, x, y):
        if y == board._y:
            if x > board._x:
                if self.side_match(board._east, newtile._west):
                    self.insertTile(x, y, newtile)
            else:
                if self.side_match(board._west, newtile._east):
                    self.insertTile(x, y, newtile)
        elif x == board._x:
            if y > board._y:
                if self.side_match(board._north, newtile._south):
                    self.insertTile(x, y, newtile)
            else:
                if self.side_match(board._south, newtile._north):
                    self.insertTile(x, y, newtile)
        

    def side_match(self, side1, side2):
        if side1 == side2:
            return True


def main():
    tile1 = Tile("Road", "Road", "Grass", "City")
    tile2 = Tile("Road", "Road", "Grass", "Road")
    grid = Grid(tile1, 5)
    grid.place_tile(grid._initialTile, tile2, grid._initialTile._y,
                    (grid._initialTile._y - 1))
    print(grid)
    
    

main()
