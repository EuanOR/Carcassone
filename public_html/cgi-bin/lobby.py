#!/usr/bin/python3

#Authors: Catherine, Eimear and Euan
#A lobby that players wait in before the game starts
#Displays a rotating icon and how many players the user is waiting on
#Also handles the form data from the previous page (CreateGameJoinGame.py)
#Calls the game controller and updates the players Name, Avatar and Colour values
#for the player associated with the cookie sent by the browser

from cgitb import enable
enable()

from os import environ
from http.cookies import SimpleCookie
from cgi import FieldStorage, escape
from Player import *
from GameController import *
from getGameController import *

print("Content-Type:text/html")
print()

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

free_colours = ["red", "green", "blue", "yellow"]
taken_colours = []
for p in gc._players:
    c = p.getColour()
    taken_colours.append(c)
    if c in free_colours:
        free_colours.remove(c)

message = ""
if colour in taken_colours:
    colour = free_colours.pop()
    message = "<p id='error'>Apologies, the colour you selected was already taken. You have been given %s instead.</p>" %colour

meepleImage = "MeepleAssets/" + colour + "Meeple.png"
player.setMeepleImage(meepleImage)
player.setColour(colour)
player.setAvatar(avatar)
#closes the GameController
setGameController(gc)

#Displays an animation while the player waits for the lobby to fill.
print("""<!DOCTYPE html>
    <html class="lobbyPage">
    <head>
    <meta charset="UTF-8">
    <title>Carcassonne</title>
    <link rel="stylesheet" type="text/css" href="../Carcassonne.css">
    <script src="../lobby.js"></script>
    </head>
    <body>
    <div id="lobbyPageHeader">
    <img src="../TileAssets/carcassonneLogoCut.jpg" alt="Carcassonne Logo" id="logoImage">
    </div>
    <section class="container">
    <div id="loading">
    <img src="../TileAssets/loader.png" id="loader">
    <p id="playerCount"></p>
    </div>
    %s
    </section>
    </body>
    </html>""" %message)
