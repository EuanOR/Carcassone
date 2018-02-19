#!/usr/bin/env python3

# Return current player
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gC = getGameController()
print(gC._playing)
setGameController(gC)
