#!/usr/local/bin/python3
# Very basic version!
# Not tested!
from cgitb import enable 
enable()
from http.cookies import SimpleCookie
from cgi import FieldStorage, escape
from hashlib import sha256
from shelve import open
from os import environ
from time import time
from getWaitingGames import *
# Cookie holds playerid and creates a session with gameid
form_data = FieldStorage()
cookie = SimpleCookie()
pid = sha256(repr(time()).encode()).hexdigest()
cookie["playerid"] = pid
# Retreive a gameid of game waiting to start or start are new game and return its game id
gameid = getWaitingGames()
if gameid == "'<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'"
    #Something is wrong with DB
    return "<p>joingame.py: Error with DB Table games</p>"
else:
    session_store = open("sessions/sess_" + int(gameid))
    if len(form_data) != 0:
        name = escape(form_data.getfirst('name', '').strip())
        #colour = escape(form_data.getfirst('password', '').strip())

print(cookie)

print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Play game</title>
        </head>
        <body>
            <header id="homeheader">
                <h1>Carcassonne</h1>
            </header>
            <form action="/game.py/gameid=%i">
                Player Name:<br>
                <input type="text" name="name" value="">
                <br>
                <input type="submit" value="Play!">
            </form> 
        </body>
    </html>""" % gameid)
