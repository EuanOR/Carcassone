#!/usr/bin/python3

from getGameController import *
from cgitb import enable
enable()


def getSizeOfGrid(gameController):
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
    return minX-1, maxX+1, minY-1, maxY+1

def getCompleteTableList(minX, maxX, minY, maxY, gameController):
    tableList = []
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            item = None
            for l in gameController._grid._grid:
                if l[0][0] == x and l[0][1] == y:
                    item = l[1]
            tableList.append([x, y, item])
    return tableList

def buildTable(tableList):
    #TODO meeple placements on tiles!!!!!!!!!!!
    htmlTable = "<tbody>"
    yVal = None
    for cell in tableList:
        if yVal == None:
            yVal = cell[1]
            htmlTable += "<tr>"
        elif cell[1] > yVal:
            yVal = cell[1]
            htmlTable += "</tr><tr>"
        htmlTable += "<td id='%i,%i'>" %(cell[0], cell[1])
        if cell[2] != None:
            htmlTable += "<img src='TileAssets/%s' style='transform: rotate(%sdeg);'>" %(cell[2]._image, cell[2]._degreeRotated)
            if cell[2]._meeple != None:
                m = cell[2]._meeple
                imageSrc = m._player._meepleImage
                htmlTable += "<img src='%s' style='z-index: -1;'>" %(imageSrc)
        elif cell[2] == None:
            htmlTable += "<img src='TileAssets/FreeTile.png' style='visibility: hidden;'>"
        htmlTable += "</td>"
    return htmlTable + "</tbody>"

print("Content-Type: text/plain")
print()

try:
    gC = getGameController()
    minX, maxX, minY, maxY = getSizeOfGrid(gC)
    tableList = getCompleteTableList(minX, maxX, minY, maxY, gC)
    htmlTable = buildTable(tableList)
except Exception:
    print("problem")
    exit()

print(htmlTable)


