#!/usr/local/bin/python3
from cgitb import enable 
enable()
from http.cookies import SimpleCookie
from cgi import FieldStorage, escape
from hashlib import sha256
from os import environ
from time import time

# Update games table in DB so that no more players can join this game (session)
form_data = FieldStorage()
if len(form_data) != 0:
    gameid = escape(form_data.getfirst('gameid', '').strip())
try:
    connection = db.connect("cs1dev.ucc.ie", "cmf4", "thiekiek", "2019_cmf4")
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""UPDATE games SET full = true WHERE gameid = %i""", (int(gameid)))
except db.Error:
    return "Error with DB Table: games"

# Henry's game stuff I guess ???
