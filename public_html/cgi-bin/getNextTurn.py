#!/usr/bin/python3

# Get available and valid places according to tile rotation
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()
from cgi import FieldStorage, escape
gC = getGameController()

gC.nextGo()
setGameController(gC)
print("success")
