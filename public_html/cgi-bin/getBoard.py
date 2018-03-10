#!/usr/bin/python3

# Authors: Cathy, Brendan, Claire
from getGameController import *
from cgitb import enable
enable()


def getSizeOfGrid(gameController):
    # Get the max number of columns and rows needed to build new board
    minX, maxX, minY, maxY = (None, None, None, None)
    for coords, tile in gameController._grid._grid:
        x, y = coords
        if minX == None or x < minX:
            minX = x
        if maxX == None or x > maxX:
            maxX = x
        if minY == None or y < minY:
            minY = y
        if maxY == None or y > maxY:
            maxY = y
    # Add one to add empty cells around the board that
    # can have a tile placed in on the next turn
    return minX-1, maxX+1, minY-1, maxY+1

def getCompleteTableList(minX, maxX, minY, maxY, gameController):
    # Creates 2D array of the board including all empty and full cells
    tableList = []
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            item = None
            for l in gameController._grid._grid:
                if l[0][0] == x and l[0][1] == y:
                    item = l[1]
            tableList.append([x, y, item])
    return tableList

def getRealDirection(tile):
    # Get the side on which the meeple is placed and
    # return the right css style for the position of the meeple
    degree_rotated = tile._degreeRotated
    rotation = 0
    rotation = int((tile._degreeRotated / 90 ) % 4)
    sides = ["top", "right", "bottom", "left"]
    side = tile._meeple_placement
    sideStyle = ""
    sideString = ""
    if side == tile._left:
        sideString = "left"
    elif  side == tile._right:
        sideString = "right"
    elif side == tile._top:
        sideString = "top"
    elif  side == tile._bottom:
        sideString = "bottom"
    else:
        return sideStyle
    # Get the index of where the side string is in the list sides
    # and get the correct rotation
    index = sides.index(sideString)
    index -= rotation
    if index == 5:
        index = 4
    if sides[index] == "left":
        sideStyle = "right: 30px;"
    elif sides[index] == "right":
        sideStyle = "left: 30px;"
    elif sides[index] == "top":
        sideStyle = "bottom: 30px"
    elif sides[index] == "bottom":
        sideStyle = "top: 30px"
    return sideStyle
    
    
    
def buildTable(tableList):
    # Builds HTML table with all currently placed tiles and meeples 
    sideStyle = ""
    
    htmlTable = "<tbody>"
    yVal = None
    for cell in tableList:
        if yVal == None:
            yVal = cell[1]
            htmlTable += "<tr>"
        elif cell[1] > yVal:
            yVal = cell[1]
            htmlTable += "</tr><tr>"
        # If there is a tile in this cell
        if cell[2] != None:
            htmlTable += """<td id='%i,%i' style='background-image: url(TileAssets/%s); transform: rotate(%sdeg); background-repeat: no-repeat;'>""" % (cell[0], cell[1], cell[2]._image, cell[2]._degreeRotated)
            # If there is a meeple to be placed on the tile
            if cell[2]._meeple != None:
                m = cell[2]._meeple
                imageSrc = m._player._meepleImage
                # Get the right css style for the meeple image placement
                sideStyle = getRealDirection(cell[2])
                htmlTable += """<img src='%s' style='z-index:5; transform: rotate(-%sdeg); position: relative; %s'>""" %(imageSrc, cell[2]._degreeRotated, sideStyle)
        # If the cell is empty (no tile has been placed)
        elif cell[2] == None:
            htmlTable += """<td id='%i,%i'>""" %(cell[0], cell[1])
            htmlTable += """<img src='TileAssets/FreeTile.png' style='visibility: hidden;'>"""
        htmlTable += "</td>"
    return htmlTable + "</tbody>"

  
    

print("Content-Type: text/plain")
print()

try:
    gC = getGameController()
    minX, maxX, minY, maxY = getSizeOfGrid(gC)
    tableList = getCompleteTableList(minX, maxX, minY, maxY, gC)
    htmlTable = buildTable(tableList)
except Exception as e:
    print(e)
    exit()

print(htmlTable)
