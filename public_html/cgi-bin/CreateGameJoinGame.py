#!/usr/bin/python3

from cgitb import enable
from cgi import FieldStorage, escape
from hashlib import sha256
from http.cookies import SimpleCookie
from os import environ
from shelve import open
from time import time

from Player import *
from GameController import *
enable()

playerID = sha256(repr(time()).encode()).hexdigest()
player = Player(playerID)
player.createMeeples()

cookie = SimpleCookie()
cookie["playerID"] = playerID
print(cookie)
def makePlayerSession(playerID, gameID, index):
    """Makes a player_session for the player.
    so that the player can get their gameID easily
    + get which position they are in gc._players (to check if it's their go) etc
    """
    player_session = open("../player_sessions/sess_" + playerID, writeback=True)
    player_session["gameID"] = gameID
    player_session["index"] = index
    player_session.close()

def newGame(playerID, player):
    """Makes a new game for the player."""
    game_sessions = open("../game_sessions/sessionlist", writeback=True)
    # create a new entry in game_sessions
    gameID = sha256(repr(time()).encode()).hexdigest()
    game_sessions[gameID] = [player]
    index = 0
    player_list = game_sessions[gameID]
    game_sessions.close()
    #print(list(game_sessions.keys()))
    # create a game, create a GameController for it and add the player
    game = open("../game_sessions/sess_" + gameID, writeback=True)
    gc = GameController()
    gc.joinGame(player)
    game["GameController"] = gc
    game.close()
    # make player session
    makePlayerSession(playerID, gameID, index)
    return str([pl._name for pl in player_list])

def joinGame(gameID, playerID, player):
    """Adds player to an already existing game."""
    game_sessions = open("../game_sessions/sessionlist", writeback=True)
    # add to entry in game_sessions
    player_list = game_sessions[gameID]
    index = len(player_list)
    player_list += [player]
    game_sessions[gameID] = player_list
    game_sessions.close()
    # add player to GameController
    game = open("../game_sessions/sess_" + gameID, writeback=True)
    gc = game["GameController"]
    gc.joinGame(player)
    game["GameController"] = gc
    game.close()
    # make player session
    makePlayerSession(playerID, gameID, index)
    return str([pl._name for pl in player_list])
    return ""

result = ""
mode = ""
form_data = FieldStorage()
if len(form_data) != 0:
    # mode should be start or join
    mode = escape(form_data.getfirst("mode","").strip())

# we might be able to get rid of the index variable in the player session
# and make it easier to set player._name and player._colour at the same time
# by changing Player's constructor to take playerID as player._id and then use
# setters for colour and name

if mode == "start":
    result = newGame(playerID, player)
else:
    gameFound = None
    game_sessions = open("../game_sessions/sessionlist", writeback=False)
    for gameID in game_sessions:
        player_list = game_sessions[gameID]
        if player_list != None and len(player_list) < 4:
            gameFound = gameID
            break
    game_sessions.close()
    if gameFound != None:
        result = joinGame(gameFound, playerID, player)
    else:
        result = newGame(playerID, player)

taken_avatars = []
taken_colours = []

gc = getGameController()
if gc._players != []:
    for p in gc._players:
        taken_avatars.append(p.getAvatar())
        taken_colours.append(p.getColour())

#closes the GameController
setGameController(gc)

avatars = {"avatar1":'<input type = "radio" name = "avatar" value = "avatar1" > <img src = "../TileAssets/avatar1.jpg" alt = "avatar1"><br>',\
"avatar2":'<input type = "radio" name = "avatar" value = "avatar2"> <img src = "../TileAssets/avatar2.jpg" alt = "avatar2"><br>',\
"avatar3":'<input type = "radio" name = "avatar" value = "avatar3"> <img src = "../TileAssets/avatar3.jpg" alt = "avatar3"><br>',\
"avatar4":'<input type = "radio" name = "avatar" value = "avatar4"> <img src = "../TileAssets/avatar4.jpg" alt = "avatar4"><br>',\
"avatar5":'<input type = "radio" name = "avatar" value = "avatar5"> <img src = "../TileAssets/avatar5.jpg" alt = "avatar5"><br>',\
"avatar6":'<input type = "radio" name = "avatar" value = "avatar6"> <img src = "../TileAssets/avatar6.jpg" alt = "avatar6"><br>'}

colours = {"red":'<input type = "radio" name = "colour" value = "red">Red<br>',\
"blue":'<input type = "radio" name = "colour" value = "blue">Blue<br>',\
"green":'<input type = "radio" name = "colour" value = "green">Green<br>',\
"yellow":'<input type = "radio" name = "colour" value = "yellow">Yellow<br>'}

print("Content-Type:text/html")
print()

print("""
<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
    <title> Carcassonne</title>
    <link rel="stylesheet" type="text/css" href="Carcassonne.css">
</head>
<body>
     <section class="container">
     <form action="lobby.py" method="GET">
	Name:
	<input type = "text" name = "player_name">
	<br>
	<br>""")

for a in avatars:
    if a not in taken_avatars:
        print(avatars[v])

for c in colours:
    if c not in taken_colours:
        print(colours[c])
print("""
	<br>
	<br>
	<input type="submit" value="Submit">
    </form>
    </section>
</body>
</html>
  """)
