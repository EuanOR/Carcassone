#!/usr/bin/python3

# Get available and valid places according to tile rotation
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()
from cgi import FieldStorage, escape
gC = getGameController()

form_data = FieldStorage()
if len(form_data) != 0:
	rotate = form_data.getfirst("rotate")
	if rotate == "True":
		validPlaces = gC.rotateTile()
	else:
		validPlaces = gC.getValidTilePlacements()
setGameController(gC)
ret_str = ""
for cell in validPlaces:
	ret_str += "%s,%s " %(cell[0], cell[1])
print(ret_str)
