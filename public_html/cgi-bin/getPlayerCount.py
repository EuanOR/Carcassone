#!/usr/bin/python3

from cgitb import enable
enable()

from getGameController import *
print("Content-Type: text/plain")
print()

playersWithNames = 0
try:
    gc = getGameController()
except Exception as e:
    print("problem")
    exit()

for player in gc._players:
    if player._name != "":
        playersWithNames += 1 
print(playersWithNames)

