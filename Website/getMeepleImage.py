#!/usr/local/bin/python3

# Return current player
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
imageSrc = gC._players[gC._playing]._img
print(imageSrc)
setGameController(gC)
