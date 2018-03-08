#!/usr/bin/python3

#Authors: Catherine, Eimear and Henry
#Contains fucntions for creating games and adding players to games
#User is presented with a form for entering their name, selecting an
#avatar and meeple colour which is hadled by lobby.py

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
    #Makes a new game for the player.
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
    #Adds player to an already existing game.
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

def getGameController(playerID):
    #Gets the gameController that playerID is a player in
    try:
        player_session = open('../player_sessions/sess_' + playerID, writeback=False)
        gameID = player_session['gameID']
        player_session.close()
        game = open("../game_sessions/sess_" + gameID, writeback=False)
        gC = game["GameController"]
        game.close()
        return gC
    except Exception as e:
        # if resource unavailable, wait and try again
        if e.errno == 11:
            import time
            time.sleep(0.5)
            return getGameController(playerID)


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


taken_avatars = []
taken_colours = []

gc = getGameController(playerID)
if gc._players != []:
    for p in gc._players:
        taken_avatars.append(p.getAvatar())
        taken_colours.append(p.getColour())

avatars = {"avatar1":'<input type = "radio" name = "avatar" value = "avatar1" id="avatar1"> <img src = "../TileAssets/avatar1.png" alt = "Gandalf (Lord of the Ring) Avatar" class="avatars">',\
"avatar2":'<input type = "radio" name = "avatar" value = "avatar2" id="avatar2"> <img src = "../TileAssets/avatar2.png" alt = "Knight Avatar" class="avatars">',\
"avatar3":'<input type = "radio" name = "avatar" value = "avatar3" id="avatar3"> <img src = "../TileAssets/avatar3.png" alt = "Sword Guy Avatar" class="avatars">',\
"avatar4":'<input type = "radio" name = "avatar" value = "avatar4" id="avatar4"> <img src = "../TileAssets/avatar4.png" alt = "Korg (Thor) Avatar" class="avatars">',\
"avatar5":'<input type = "radio" name = "avatar" value = "avatar5" id="avatar5"> <img src = "../TileAssets/avatar5.png" alt = "Assasin Avatar" class="avatars">',\
"avatar6":'<input type = "radio" name = "avatar" value = "avatar6" id="avatar6"> <img src = "../TileAssets/avatar6.png" alt = "Legolas (Lord of the Ring) Avatar" class="avatars">'}

avatar_str = ""
for avatar in sorted(avatars):
    if avatar not in taken_avatars:
        avatar_str += '<label class="labelForImage">'
        avatar_str += avatars[avatar]
        avatar += '</label>'

colours = {"red":"""<input type = "radio" name = "colour" value = "red" required>
                    <img src="../MeepleAssets/redMeeple.png" alt="Red Meeple" class="meepleColor">""",\
"blue":"""<input type = "radio" name = "colour" value = "blue" required>
                    <img src="../MeepleAssets/blueMeeple.png" alt="Blue Meeple" class="meepleColor">""",\
"green":"""<input type = "radio" name = "colour" value = "green" required>
                    <img src="../MeepleAssets/greenMeeple.png" alt="Green Meeple" class="meepleColor">""",\
"yellow":"""<input type = "radio" name = "colour" value = "yellow" required>
                    <img src="../MeepleAssets/yellowMeeple.png" alt="Yellow Meeple" class="meepleColor">"""}

colour_str = ""
for colour in sorted(colours):
    if colour not in taken_colours:
        if colour != "yellow":
            colour_str += """<label class="labelForImage">"""
        else:
            colour_str += """<label id="yellowMeepleImage">"""
        colour_str += colours[colour]
        colour_str += "</label>"


print("""
<!DOCTYPE html>
<html class="createGamePage">
<head>
    <meta charset="UTF-8">
    <title> Carcassonne</title>
    <link rel="stylesheet" type="text/css" href="../Carcassonne.css">
</head>
<body>
<div id="createGamePageHeader"><img src="../TileAssets/carcassonneLogoCut.jpg" alt="Carcassonne Logo" id="logoImage"></div>
    <section class="container">
        <div id="createPlayerDiv">
            <form action="lobby.py" method="GET">
                Name:
                <input type = "text" name = "name" placeholder="Enter name.." required>
                <br>
                <br>
                
                <p id="selectAvatarHeading"> Select an avatar </p>
                
                <div>
                    %s
                </div>
                <p id="selectColorHeading"> Select a meeple colour <p>
                %s
                <br>
                <input type="submit" value="Submit" id="submitFormButton">
            </form>
        </div>
    </section>
</body>
</html>
    """ %(avatar_str, colour_str))
