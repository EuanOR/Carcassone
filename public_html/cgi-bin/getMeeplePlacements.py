#!/usr/bin/python3

from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
# Get all landmark objects on tile that a meeple can be placed on
meeplePlacements = gC.getValidMeeplePlacements()
setGameController(gC)
sides = []
if meeplePlacements != []:
	for side in ["left", "top", "right", "bottom"]:
		# Get all the sides that have a landmark object on tile that a meeple can be placed on
		if gC.getTileSide(gC._tile, side) in meeplePlacements:
			sides.append(side)
print(",".join(sides))

