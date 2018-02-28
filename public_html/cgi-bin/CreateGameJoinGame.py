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

print("Content-Type:text/html")                                                                                                                                                                 
print()   
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
    if len(player_list) == 4:
      gc.nextGo()
    game["GameController"] = gc
    game.close()
    # make player session
    makePlayerSession(playerID, gameID, index)
    return str([pl._name for pl in player_list])

result = ""
mode = ""
form_data = FieldStorage()
if len(form_data) != 0:
    # mode should be start or join
    mode = escape(form_data.getfirst("mode","").strip())

loop_again = True
while loop_again:
    loop_again = False
    try:
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
    except Exception as e:
        print(e)
        if e.errno == 11:
            time.sleep(0.5)
            loop_again = True             

print("""
<!DOCTYPE html>
<head>
    <meta charset="UTF-8"> 
    <title> Carcassonne</title>
    <link rel="stylesheet" type="text/css" href="../Carcassonne.css">
</head>
<body>
     <div id="header"><img src="../TileAssets/carcassonne-logo.png" alt="Carcassonne Logo" id="logoImage"></div>	
     <section class="container">
     <div style="width: 50%; margin: 0 auto; border: 1px solid black; padding: 10px;">
	     <form action="lobby.py" method="GET">
		    Name:
		    <input type = "text" name = "name">
		    <br>
		    <br>
		    <input type = "radio" name = "avatar" value = "avatar1" > <img src = "" alt = ""><br>
		    <input type = "radio" name = "avatar" value = "avatar2"> <img src = "" alt = ""><br>
		    <input type = "radio" name = "avatar" value = "avatar3"> <img src = "" alt = ""><br>
		    <input type = "radio" name = "avatar" value = "avatar4"> <img src = "" alt = ""><br>
		    <br>
		    <input type = "radio" name = "colour" value = "red">Red<br>
		    <input type = "radio" name = "colour" value = "blue">Blue<br>
		    <input type = "radio" name = "colour" value = "green">Green<br>
		    <input type = "radio" name = "colour" value = "yellow">Yellow<br>
		    <br>
		    <input type="submit" value="Submit">
		    </form>
     </div>
     </section>
</body>
</html>
  """)
