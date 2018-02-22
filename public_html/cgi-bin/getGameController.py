from http.cookies import SimpleCookie
from os import environ
from shelve import open

# Get game controller instance from session
def getGameController():
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        print("Error! Cookie header")
        exit()
    cookie.load(http_cookie_header)
    if not 'playerID' in cookie:
        print("Error! Player ID not in cookie")
        exit()
    playerID = cookie['playerID'].value
    player_session = open('../player_sessions/sess_' + playerID, writeback=False)
    gameID = player_session['gameID']
    player_session.close()
    game = open("../game_sessions/sess_" + gameID, writeback=True)
    gC = game["GameController"]
    game.close()
    return gC

def setGameController(gC):
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        print("Error! Cookie header")
        exit()
    cookie.load(http_cookie_header)
    if not 'playerID' in cookie:
        print("Error! Player ID not in cookie")
        exit()
    playerID = cookie['playerID'].value
    player_session = open('../player_sessions/sess_' + playerID, writeback=False)
    gameID = player_session['gameID']
    player_session.close()
    game = open("../game_sessions/sess_" + gameID, writeback=True)
    game["GameController"] = gC
    game.close()
