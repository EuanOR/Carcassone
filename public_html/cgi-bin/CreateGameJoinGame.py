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
                                                                                                                                                                                                                                                                                                                                                                                              
#values here to be changed. Not sure what to print                                                                                                                                              
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
print(result)
