#!/usr/bin/env python3

# Get available and valid places according to tile rotation
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()
gC = getGamecontroller()
form_data = FieldStorage()
rotation = form_data.getfirst('rotation').escape()
for i in range(int(rotation)):
    validPlaces = gC.rotateTile()
print(validPlaces)
setGameController(gC)
