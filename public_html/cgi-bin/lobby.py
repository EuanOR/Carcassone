#!/usr/bin/python3

from cgitb import enable
enable()

from os import environ
from http.cookies import SimpleCookie
from cgi import FieldStorage, escape
from Player import *
from GameController import *
from getGameController import *

#Takes the Name, Colour and Avatar values sent from the previous page
#and assigns them to variables
name = ""
avatar = ""
colour = ""
form_data = FieldStorage()
if len(form_data) != 0:
    name = escape(form_data.getfirst("name","").strip())
    avatar = escape(form_data.getfirst("avatar", "").strip())
    colour = escape(form_data.getfirst("colour","").strip())

#note for when using the game controller setGameController must
#be called at the end with the game controller in the parameter

#gets the users cookie from their browsers
cookie = SimpleCookie()
http_cookie_header = environ.get('HTTP_COOKIE')
#if there's no cookie return an error
if not http_cookie_header:
    print("Error! Cookie header")
    exit()

#loads the cookie and checks for the player ID returning an
#error if it isnt there
cookie.load(http_cookie_header)
if not 'playerID' in cookie:
    print("Error! Player ID not in cookie")
    exit()

#assigns the player ID value to a variable
playerID = cookie['playerID'].value

#opens the GameController and gets the player with the cookies ID
gc = getGameController()
player = gc.getPlayer(playerID)

#Sets the name, avatar and meeple colour attributes based on the values
#sent by the previous page
player.setName(name)
meepleImage = "MeepleAssets/" + colour + "Meeple.png"
player.setMeepleImage(meepleImage)
player.setAvatar(avatar)
#closes the GameController
setGameController(gc)

#Displays an animation while the player waits for the lobby to fill.
print("Content-Type:text/html")
print()
print("""<!DOCTYPE html>
    <head>
        <meta charset="UTF-8"> 
	<title>Carcassonne</title>
	<link rel="stylesheet" type="text/css" href="../Carcassonne.css">
        <script src="../lobby.js"></script>
        <style>
            #loader {
                margin-left: auto;
                margin-right: auto;
                border-radius: 5%;
                -webkit-animation: spin 4s linear infinite;
                animation: spin 3s 1s linear infinite;
            }
            
            #loading {
	      text-align: center;
	    }

            @-webkit-keyframes spin {
                0% { -webkit-transform: rotate(0deg); }
                100% { -webkit-transform: rotate(360deg); }
            }

            /* little spinny animation */
            @keyframes spin {
                0% { transform: rotate(0deg); }

                20% { transform: rotate(90deg); }
                25% { transform: rotate(90deg); }

                45% { transform: rotate(180deg); }
                50% { transform: rotate(180deg); }

                70% { transform: rotate(270deg); }
                75% { transform: rotate(270deg); }

                95% { transform: rotate(360deg); }
                100% { transform: rotate(360deg); }
            }            

        </style>
    </head>

    <body>
	    <div id="header"><img src="../TileAssets/carcassonne-logo.png" alt="Carcassonne Logo" id="logoImage"></div>
	    <section class="container">
		<div id="loading">
		<img src="../TileAssets/loader.png" id="loader">
		<p id="playerCount"></p>
		</div>
	    </section>

    </body>
</html>""")
