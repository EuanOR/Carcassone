#!/usr/bin/python3

from cgitb import enable
enable()

from getGameController import *
print("Content-Type: text/plain")
print()

try:
    gc = getGameController()
except Exception as e:
    print("problem")
    exit()
print(len(gc._players))

