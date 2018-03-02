#!/usr/bin/python3

from shelve import open
def getGameController(playerID):
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

def getTile(gC, x, y):
    return gC._grid.getTile(x, y)

def main():
    gC = getGameController("""PUT ID FROM CONSOLE IN HERE""")
    print("tile=", gC._tile)
    print("meeple placements=", gC.getValidMeeplePlacements)
    print("current player=", gC._players[gC._playing]._name)

if __name__ == "__main__":
    main()



    
