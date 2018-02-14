# Get index of next player

#!/usr/local/bin/python3

# Return current player
from cgitb import enable 
enable()

from getGameController import *
print('Content-Type: text/plain')
print()

gc = getGameController()
print(gC._playing)