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
    sid = cookie['playerID'].value
    player_session = open('player_sessions/sess_' + playerID, writeback=False)
    gameID = player_session['gameID']
    game = open("game_sessions/sess_" + gameID, writeback=True)
    gC = game["GameController"]
    return gc