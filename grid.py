
# Grid class of size 5 by 5 squares
class Grid:
    def __init__(self, tile, size):
        self._size = size
        self._grid = []
        self._center = self._size // 2
        self._initialTile = tile

        self.createGrid()

    # Creates grid and places initial tile in center of grid
    def createGrid(self):
        self._grid = [[0 for y in range(self._size)] for x in range(self._size)]
        self.insertTile(self._center, self._center, self._initialTile)
        return self._grid

    # Places tile at grid location x, y
    def insertTile(self, x, y, tile):
        self._grid[x][y] = tile


def main():
    tile1 = Tile()
    grid = Grid(tile1, 5)
    print(grid.createGrid())

main()
