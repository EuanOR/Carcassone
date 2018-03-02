#!/usr/bin/python3

from cgitb import enable 
enable()

from getGameController import *
from cgi import FieldStorage, escape
print('Content-Type: text/plain')
print()

gC = getGameController()

form_data = FieldStorage()
if len(form_data) != 0:
    cell = form_data.getfirst("cellID")
    x, y = cell.split(",")
    gC.placeTile(int(x),int(y))
    print("placed")
else:
    print("problem")

setGameController(gC)

