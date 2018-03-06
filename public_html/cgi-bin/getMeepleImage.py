#!/usr/bin/python3

# Return current player
from cgitb import enable 
enable()

from getGameController import *
from cgi import FieldStorage, escape
print('Content-Type: text/plain')
print()

form_data = FieldStorage()
gC = getGameController()
if len(form_data) != 0:
    side = form_data.getfirst("side")
    if side == "monastery":
        landmark = gC.getTile()._monastery
    else:
        landmark = gC.getTileSide(gC.getTile(), side)
    gC.placeMeeple(landmark)

imageSrc = gC._players[gC._playing]._meepleImage
print(imageSrc)
setGameController(gC)
