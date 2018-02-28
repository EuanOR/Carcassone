#!/usr/bin/python3

# Return player cookie
from os import environ
from http.cookies import SimpleCookie

print('Content-Type: text/plain')
print()

cookie = SimpleCookie()
http_cookie_header = environ.get('HTTP_COOKIE')
if not http_cookie_header:
    print("problem")
    exit()
cookie.load(http_cookie_header)
if not 'playerID' in cookie:
    print("problem")
    exit()
playerID = cookie['playerID'].value

print(playerID)


