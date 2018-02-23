#!/usr/bin/python3

from getGameController import *
from cgitb import enable
enable()
print("Content-Type: text/plain")
print()


def tableCreator(GameController):
    Players=GameController._players
    Players.sort(key=lambda x: x._score,reverse=True)
    outstr=""
    outstr+=("""
        <table id ="scoreboard">
                <tr>
                    <th>Player</th>
                    <th>Score</th>
                    <th>Meeples Remaining</th>
                </tr>\n""")
    for i in Players:
        outstr+=("""
                <tr>
                    <th>%s</th>
                    <th>%i</th>
                    <th>%i</th>
                </tr>\n"""%(i._name,i._score,len(i._inactiveMeeples)))
    outstr+=("""
        </table>""")
    return outstr

gc=getGameController()
table=tableCreator(gc)
print(table)
