#!/usr/bin/python3

# Return current player
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
player = gC._players[gC._playing]
print(player._id + "," + player._name)
