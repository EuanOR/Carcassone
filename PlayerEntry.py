#!/usr/bin/python3
from cgitb import enable
enable()

print("Content-Type:text/html")
print()
print("""<!DOCTYPE html>
<html>
<head></head>
<body>
 <form>
   Name:
   <input type = "text" name = "player_name">
   <br>
   <br>
   <input type = "radio" name = "avatar" value = "avatar1" > <img src = "" alt = ""><br>
   <input type = "radio" name = "avatar" value = "avatar2"> <img src = "" alt = ""><br>
   <input type = "radio" name = "avatar" value = "avatar3"> <img src = "" alt = ""><br>
   <input type = "radio" name = "avatar" value = "avatar4"> <img src = "" alt = ""><br>
   <br>
   <input type = "radio" name = "colour" value = "red">Red<br>
   <input type = "radio" name = "colour" value = "blue">Blue<br>
   <input type = "radio" name = "colour" value = "green">Green<br>
   <input type = "radio" name = "colour" value = "yellow">Yellow<br>
   <br>
   <input type="submit" value="Submit">
 </form>
 </body>
</html>""")
