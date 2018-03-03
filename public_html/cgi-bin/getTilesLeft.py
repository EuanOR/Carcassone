#!/usr/bin/python3

from cgitb import enable
enable()
from getGameController import *

print("Content-Type: text/plain")
print()

gC = getGameController()
tilesLeft = gC._deck._deck.length()
print(tilesLeft)

