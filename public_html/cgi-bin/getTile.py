#!/usr/bin/python3

# Get current tile in play
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
tile = gC.getTile()
print(tile._image)
setGameController(gC)
