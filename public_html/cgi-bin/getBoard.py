#!/usr/bin/python3

from getGameController import *
from cgitb import enable
enable()


def getSizeOfGrid(gameController):
    minX, maxX, minY, maxY = (None, None, None, None)
    for x, y, tile in gameController._grid:
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
            for l in lst:
                if l[0] == x and l[1] == y:
                    item = l[2]
            tableList.append([x, y, item])
    return tableList

def buildTable(tableList):
    #TODO meeple placements on tiles!!!!!!!!!!!
    htmlTable = "<table>"
    yVal = None
    for cell in tableList:
        if yVal == None:
            yVal = cell[1]
            htmlTable += "<tr>"
        elif cell[1] > yVal:
            yVal = cell[1]
            htmlTable += "</tr><tr>"
        htmlTable += "<td id='%i%i'>" %(cell[0], cell[1])
        if cell[2] != None:
            htmlTable += "<img src='%s' style='transform: rotate(%sdeg);'>" %(cell[2]._image, cell[2]._degreeRotated)
        htmlTable += "</td>"
    return htmlTable + "</table>"

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


