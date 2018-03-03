#!/usr/bin/python3

# Return current player and tiles left in deck
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
player = gC._players[gC._playing]
print("%s,%s,%i" %(player._id, player._name, gC._deck._deck.length()))
