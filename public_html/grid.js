(function() {
  
    // Request variables for AJAX
    var request;
    var leaderboardRequest;
    var playerRequest;
    var validPlacesRequest;
    var checkMeeplesRequest;
    var placeMeepleRequest;
    var cookieRequest;
    var nextTurnRequest;
    var boardRequest;
    var placeTileRequest;
    // Gameboard & sidebar container
    var grid;
    var board;
    // Relative path of image src
    var currentTile;
    // Current rotation of currentTile
    var rotation = 0;
    // Player table row in leaderboard
    var player;
    var tableCellID;
    // Rotate button for deck tile
    var rotateButton;
    // This players cookie
    var playerCookie;
    // Boolean, true if it is your go
    var currentlyPlaying = false;
    // Polling for player
    var playerPoll;
    // Player tile info div
    var deckTileDiv;
    //player tile
    var curTile;
    // Game grid
    var table;
    // Meeple query for user
    var meepleQuestion;
    // Landmark side meeple is placed on
    var side;
    // Count of remaining tiles
    var tileCount;
    var pTagTile = 71;
    // Player score display
    var scoreboard;
    // if rotateButton pressed
    var rotateActive = true;
    
    //Audio files
     var background;
     var draw;
     var placeM;
     var placeT;
     var point;
     var rotate;
     var victory;
    
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        background = new Audio("AudioAssets/background_music.mp3");
        draw = new Audio("AudioAssets/draw_tile.mp3");
        placeM = new Audio("AudioAssets/place_meeple.mp3");
        placeT = new Audio("AudioAssets/place_tile.mp3");
        point = new Audio("AudioAssets/point_gain.mp3");
        rotate = new Audio("AudioAssets/rotate_tile.mp3")
        victory = new Audio("AudioAssets/victory_fanfare.mp3");
        console.log("GAME STARTING");
	pTagTile = document.getElementById("tileCount");
        grid = document.getElementById("grid");
	board = document.getElementById("board");
	deckTileDiv = document.getElementById("deckTile");
	meepleQuestion = document.getElementById("meepleQuestion");
	curTile = document.getElementById("curTile");
	rotateButton = document.getElementById("rotateImage");
	background.addEventListener("ended", restartMusic, false);
	background.volume = 0.5;
        background.load();
	background.play();
	console.log("geting cookie ID");
	getCookieID();
        startGame();
	console.log("playerCookie=" + playerCookie);
	playerPoll = setInterval(pollTurn, 2000);
    }
    
    //Background music
    function restartMusic(){
      background.currentTime = 0;
      background.load();
      background.play();
    }
    
    // Get players cookie
    function getCookieID(){
	console.log("getting player");
        var url = "cgi-bin/getCookie.py";
        cookieRequest = new XMLHttpRequest();
        cookieRequest.addEventListener("readystatechange", cookieReceived, false);
        cookieRequest.open("GET", url, true);
        cookieRequest.send(null); 
    }
    
    function cookieReceived(){
	console.log("cookie received");
	console.log("readyState = " + cookieRequest.readyState);
        if (cookieRequest.readyState === 4) {
	    console.log("ready");
	    console.log("cookieRequest.status = " + cookieRequest.status);
            if (cookieRequest.status === 200) {
		console.log("OK");
		console.log("cookieRequest = " + cookieRequest.responseText.trim());
                if (cookieRequest.responseText.trim() != "problem") {
		    playerCookie = cookieRequest.responseText.trim();
		    console.log("playerCookie =" + playerCookie);
		}
	    }
	}
    }
    
    function pollTurn(){
	console.log("getting player");
        var url = "cgi-bin/getPlayer.py";
        playerRequest = new XMLHttpRequest();
        playerRequest.addEventListener("readystatechange", playerReceived, false);
        playerRequest.open("GET", url, true);
        playerRequest.send(null); 
    }
    
    function pollBoard(){
	console.log("getting board");
        var url = "cgi-bin/getBoard.py";
        boardRequest = new XMLHttpRequest();
        boardRequest.addEventListener("readystatechange", boardReceived, false);
        boardRequest.open("GET", url, true);
        boardRequest.send(null); 
    }
    
    function boardReceived(){
	    console.log("board received");
	    if (boardRequest.readyState === 4){
	        console.log("ready");
	        console.log("board = " + boardRequest.responseText.trim());
	        if (boardRequest.status === 200){
		        console.log("OK");
		        console.log("board = " + boardRequest.responseText.trim());
		        if (boardRequest.responseText.trim() != "problem"){
		            console.log("board = " + boardRequest.responseText.trim());
		            table.innerHTML = boardRequest.responseText.trim();
			    if (currentlyPlaying === true){
		              getValidPlaces("False");
			    }
	      
		        }
	        }
	    }
    }

    //STARTS GAME
    function startGame(){
        console.log("GameBoard");
        //Create gameboard
        createGameBoard();
	//Create initial leaderboard;
	console.log("get leaderboard");
	getLeaderBoard();
	//Place initial tile in grid cell [0,0]
        console.log("PLACE START TILE");
        placeStartTile(0,0);
        //Get player name
	console.log("made it out");
	//Get player turn
	pollTurn();
    }

    //CREATE TABLE FOR GAMEBOARD
    function createGameBoard(){
        // Create HTML table
        table = document.getElementById('game');
        table.cellPadding = "0";
        table.cellSpacing = "0";
        var tableBody = document.createElement('tbody');
        console.log("table made");
	
        // increment y-coordinate for cell
        for (var yStart = -1; yStart < 2; yStart++){
            // Create row
            var row = document.createElement("tr");

            // increment x-coordinate for cell
            for (var xStart = -1; xStart < 2; xStart++){
                // Create column
                var cell = document.createElement("td");
                // Adds an ID for each cell of table
		cell.id = ((xStart.toString()).concat(",")).concat((yStart.toString()));
                // Add blank image for each cell
                var emptyCell = document.createElement('img');
                emptyCell.src = "TileAssets/FreeTile.png";
                emptyCell.className = "unplaced";
		emptyCell.style.zIndex= "1";
                emptyCell.style.visibility = "hidden";
                cell.appendChild(emptyCell);
		row.appendChild(cell);

                // Increment cell position
            }
            // Increment cell position
            tableBody.appendChild(row);
        }
        // Add table to container div and set a border
        table.appendChild(tableBody);
        board.appendChild(table);
        table.setAttribute("border", "1");
    }

    // PLACE START TILE ON GAME BOARD
    function placeStartTile(x,y){
        console.log("Placing start tile");
        // Cell to place start tile
	var ID = (x.toString()).concat(",").concat((y.toString()));
	var cell = document.getElementById(ID);
	console.log(cell);
        var image = document.createElement('img');
        image.src = "TileAssets/Start.png";
        image.className = "placed";
        cell.innerHTML = "";
	pTagTile.innerHTML = "Remaining tiles: " + tileCount;

        // Place tile in central grid cell [0,0]
        cell.appendChild(image);
    }

    // Handler for 'getPlayer()'
    function playerReceived(){
        console.log("player received");
	console.log("readyState = " + playerRequest.readyState);
        if (playerRequest.readyState === 4) {
	    console.log("ready");
	    console.log("playerRequest.status = " + playerRequest.status);
            if (playerRequest.status === 200) {
		console.log("OK");
		console.log("playerresponse = " + playerRequest.responseText.trim());
                if (playerRequest.responseText.trim() != "problem") {
		    console.log("success");
		    var responseList = playerRequest.responseText.trim().split(",");
		    console.log("response= " + responseList);
		    var player_id = responseList[0];
		    tileCount = responseList[2];
		    var gameOver = responseList[3];
		    console.log("gameOver= " + gameOver);
		    
		    // GAME OVER
		    if (gameOver === "True"){
			console.log("if ended game");
			endGame();
			return;
		    }
		    
		    console.log("!!!player_id= " + player_id);
		    console.log("player=" + player);
		    var oldPlayer = null;
		    
		    // START OF GAME: DID WE GET THE PLAYER
		    if (typeof player !== "undefined" && player !== null){
		        player.style.backgroundColor = "white";
			oldPlayer = player;
		    }
		    player = document.getElementById(player_id);
		    player.style.backgroundColor = "#D8FA9A";
		    console.log("player after being set= " + player);
		    
		    // EVERY TIME A TURN CHANGES
		    if (oldPlayer != player){
			pTagTile.innerHTML = "Remaining Tiles: " + tileCount;
		        pollBoard();
			getLeaderBoard();
		    }
		    
		    // CURRENT PLAYERS TURN
		    if (player_id == playerCookie){
		        currentlyPlaying = true;
			//it's your go, get yo tile etc
		        clearInterval(playerPoll);
			rotation = 0;
		        getPlayerTile();
			pTagTile.innerHTML = "Remaining Tiles: " + tileCount;
		        getValidPlaces("False");
			rotateButton.addEventListener("click", rotateTile, false);
			getLeaderBoard();
			player.style.backgroundColor = "#D8FA9A";
		    }
		    
                } 
            }
        }
    }

    function endGame(){
        console.log("end game function");
        getLeaderBoard();
        window.alert("Game Over!! Final scores are: <table>" + scoreboard + "</table>");
	victory.load();
	victory.play();
    }

    //GET PLAYER THEIR TILE FOR THIS TURN
    function getPlayerTile(){
        var url = "cgi-bin/getTile.py";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", tileReceived, false);
        request.open("GET", url, true);
        request.send(null);    
    }

    function tileReceived(){
        if (request.readyState === 4) {
            if (request.status === 200) {
		console.log(request.responseText.trim());
                if (request.responseText.trim() != "problem") {
                    // request.responseText.trim() = "TileAssets/tile.png"
                    // If successful update user display to new player tile
                    showPlayerTile(request.responseText.trim());    
                }
            }
        }
    }

    function showPlayerTile(tilePath){
	console.log("SHOWING A PLAYER TILE");
        var image = document.createElement("img");
	tilePath = "TileAssets/" + tilePath;
        image.src = tilePath;
	console.log(tilePath);
        currentTile = tilePath;
	console.log(currentTile);
        curTile.appendChild(image);
	draw.load();
	draw.play();
    }

    //SHOW AVAILABLE VALID CELLS
    function getValidPlaces(rotate){
        // Get array of available, valid cells
	console.log("getting valid places");
        var url = "cgi-bin/getValidPlaces.py?rotate=" + rotate;
        validPlacesRequest = new XMLHttpRequest();
        validPlacesRequest.addEventListener("readystatechange", validPlacesReceived, false);
        validPlacesRequest.open("GET", url, true);
        validPlacesRequest.send(null);
    }

    // Handles 'getValidPlaces()'
    function validPlacesReceived(){
	console.log("receiving valid responses");
        if (validPlacesRequest.readyState === 4) {
            if (validPlacesRequest.status === 200) {
	        console.log("VALIDPLACESRECEIVED response= " + validPlacesRequest.responseText.trim());
                if (validPlacesRequest.responseText.trim() != "problem") {
                    // If successful get list of valid cell locations
                    var startArray = validPlacesRequest.responseText.trim().split(" ");
		    console.log("valid array=" + startArray);
		    if (rotateActive === false){
		      rotateButton.addEventListener("click", rotateTile, false);
		      rotateActive = true;
		    }
                    showValidPlaces(startArray);  
                }
            }
        }
    }

    function showValidPlaces(startArray){
	console.log("SHOWVALIDPLACES startArray= " + startArray);
        for (var i=0; i < startArray.length; i++) {
	    console.log(startArray[i]);
            var cellImage = document.getElementById(startArray[i]).firstChild;
            cellImage.style.visibility = "visible";
            // AVAILABLE VS VALID MUST ASK HENRY
            cellImage.className = "available";

            // Add event listeners to valid empty cells
            cellImage.addEventListener("click", function() { placeTile(this.parentNode.id);});
        }
    }

    function hideValidPlaces(){
        console.log("hide valid places");
        // Array of cells marked 'available' 
        var unplacedCellImages = Array.from(document.getElementsByClassName("available"));

        // Traverse through array and hide each cell from user display
        for (var i = 0; i < unplacedCellImages.length; i++) {
            unplacedCellImages[i].className = "unplaced";
            unplacedCellImages[i].setAttribute("style", "visibility:hidden");
            // Remove event listeners
            unplacedCellImages[i].removeEventListener("click", function() {placeTile(this.parentNode.id);});
        }
    }

    //PLAYER PLACES TILE ON TURN
    function placeTile(cellID){
        var image = document.getElementById(cellID).childNodes;
	console.log(currentTile);
        image[0].src = currentTile;
        image[0].className = "placed";
	image[0].style.transform = "rotate(" + rotation + "deg)";
	console.log(image[0]);
        console.log("placed tile");
	tableCellID = cellID;
	placeT.load();
	placeT.play();
	console.log("CELL TILE PLACED IN: " + cellID);
	console.log("disable multiple placements");
	hideValidPlaces();
	var url = "cgi-bin/placeTile.py?cellID=" + cellID;
        placeTileRequest = new XMLHttpRequest();
        placeTileRequest.addEventListener("readystatechange", tilePlaced, false);
        placeTileRequest.open("GET", url, true);
        placeTileRequest.send(null);
    }
    
    function tilePlaced(){
	console.log("PLACE TILE REQUEST READY STATE + STATUS= " + placeTileRequest.readyState, placeTileRequest.status);
        if (placeTileRequest.readyState === 4) {
	    console.log("response= " + placeTileRequest.responseText.trim());
            if (placeTileRequest.status === 200) {
                if (placeTileRequest.responseText.trim() === "placed") {
                    console.log("checking meeple placements");
		    checkMeeplePlacements();
		} else if (placeTileRequest.responseText.trim() !== "problem"){
		    checkMeeplePlacements();
		} else {
		    endTurn();
		}
	     }
	 }
    }
    
    function checkMeeplePlacements(){
	console.log("meeples pls");
	meepleQuestion = document.getElementById("meepleQuestion");
        // Check if a meeple can be placed
        var url = "cgi-bin/getMeeplePlacements.py";
        checkMeeplesRequest = new XMLHttpRequest();
        checkMeeplesRequest.addEventListener("readystatechange", canMeepleBePlaced, false);
        checkMeeplesRequest.open("GET", url, true);
        checkMeeplesRequest.send(null);
    }
    
    function canMeepleBePlaced(){
	console.log("can meeples be placed");
        if (checkMeeplesRequest.readyState === 4) {
            if (checkMeeplesRequest.status === 200) {
                if (checkMeeplesRequest.responseText.trim() != "problem") {
                    console.log("Response = " + checkMeeplesRequest.responseText.trim());
                    if (checkMeeplesRequest.responseText.trim() === ''){
			console.log("No meeples");
                        endTurn();
                    }
                    // else return places
                    else {
                        var sides = checkMeeplesRequest.responseText.trim().split(",");
			console.log("Sides when first created= " + sides);
                        placeMeeple(sides);    
                    } 
                }
            }
        }
    }

    function placeMeeple(sides){
        //  ask user do you want to place meeple?
        //  if True
        meepleQuestion.innerHTML = "";
        var text = document.createTextNode("Place a meeple?");
        meepleQuestion.appendChild(text);
        for (var i = 0; i < sides.length; i++) {
            var newButton = document.createElement('button');
	    newButton.className = "meepleButtons";
	    console.log("button made for side: " + sides[i]);
            newButton.innerHTML = sides[i];
            meepleQuestion.appendChild(newButton);
            newButton.addEventListener("click", function() { 
                console.log("meeple side been pressed");
                // put the meeple on this side of the grid cell
	        side = this.innerHTML;
	        console.log("side being sent: " + side);
                var url = "cgi-bin/getMeepleImage.py?side=" + side;
                placeMeepleRequest = new XMLHttpRequest();
                placeMeepleRequest.addEventListener("readystatechange", placeMeepleImage, false);
                placeMeepleRequest.open("GET", url, true);
                placeMeepleRequest.send(null);
	    }, false);
	    placeM.load();
	    placeM.play();
	    }
        var endGo = document.createElement("button");
        endGo.innerHTML = "NO";
	meepleQuestion.appendChild(endGo);
	endGo.className = "meepleButtons";
        endGo.addEventListener("click",  endTurn, false);
    }
		

    function placeMeepleImage(){
        // TODO: Needs to place image to correct side of cell
        console.log("place meeple image");
	console.log("PLACE MEEPLE READY state= " + placeMeepleRequest.readyState);
	placeM.play();
	console.log("PLACE MEEPLE IMAGE READY STATE= " + placeMeepleRequest.readyState);
        if (placeMeepleRequest.readyState === 4) {
	    console.log("PLACE MEEPLE IMAGE STATUS= " + placeMeepleRequest.status);
            if (placeMeepleRequest.status === 200) {
	      console.log("PLACE MEEPLE IMAGE RESPONSE=" + placeMeepleRequest.responseText.trim());
                if (placeMeepleRequest.responseText.trim() != "problem") {
		    console.log("PLACE MEEPLE IMAGE RESPONSE= " + placeMeepleRequest.responseText.trim());
                    var cell = document.getElementById(tableCellID);
                    var meepleImage = document.createElement("img");
		    meepleImage.style.zIndex = "2";
		    meepleImage.style.position = "relative";
                    meepleImage.src = placeMeepleRequest.responseText.trim();
                    cell.appendChild(meepleImage);
                    endTurn();
                }
            }
        }
    }
    
    function endTurn(){
        currentlyPlaying = false;
	console.log("end turn");
        // Delete any meeple buttons
        meepleQuestion.innerHTML = "";
        tableCellID = null;
	var curdeckTile = curTile.querySelector("img");
	curTile.removeChild(curdeckTile);
	hideValidPlaces();
        getLeaderBoard();
        getNextTurn();
    }

    function getNextTurn(){
        rotateButton.removeEventListener("click", rotateTile, false);
        rotation = 0;
	var url = "cgi-bin/getNextTurn.py";
        nextTurnRequest = new XMLHttpRequest();
        nextTurnRequest.addEventListener("readystatechange", nextTurnReceived, false);
        nextTurnRequest.open("GET", url, true);
        nextTurnRequest.send(null); 
    }
    
    function nextTurnReceived(){
        console.log("getting next turn");
        if (nextTurnRequest.readyState === 4) {
            if (nextTurnRequest.status === 200) {
		console.log("status= " + nextTurnRequest.status);
		console.log("response= " + nextTurnRequest.responseText.trim());
                if (nextTurnRequest.responseText.trim() == "success") {
		    console.log("no problem");
		    pollTurn();
		    playerPoll = setInterval(pollTurn, 2000);
		}
	    }
        }
    }

    function rotateTile(){
        rotateButton.removeEventListener("click", rotateTile, false);
	rotateActive = false;
	var tile = curTile.querySelector("img");
	console.log("rotation = " + rotation);
        if (rotation >= 270){
            rotation = 0;
        } else {
            rotation += 90;
        }
        tile.style.transform = "rotate(" + rotation + "deg)";
	rotate.load();
	rotate.play();
	hideValidPlaces();
        getValidPlaces("True");
	
    }

    // Called in 'placeTile()'
    function getLeaderBoard(){
	console.log("getting leaderboard");
        var url = "cgi-bin/Scoreboard.py";
        leaderboardRequest = new XMLHttpRequest();
        leaderboardRequest.addEventListener("readystatechange", leaderboardReceived, false);
        leaderboardRequest.open("GET", url, true);
        leaderboardRequest.send(null);
    }

    // Handles 'updateScore()'
    function leaderboardReceived(){
	console.log("LEADERBOARD recieve function");
        if (leaderboardRequest.readyState === 4) {
            if (leaderboardRequest.status === 200) {
                if (leaderboardRequest.responseText.trim() != "problem") {
		    updateLeaderboard(leaderboardRequest.responseText.trim());
                }
            }
        }
    }
    
    function updateLeaderboard(newLeaderboard){
        console.log("updating leaderboard");
        scoreboard = document.getElementById("scoreboard");
        scoreboard.innerHTML = newLeaderboard;
	if (typeof player !== "undefined" && player !== null){
 	    player.style.backgroundColor = "#D8FA9A";
	}
    }

})();
