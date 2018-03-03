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
    var tileCount = 72;
    var pTagTile;
    // Player score display
    var scoreboard;
    
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        console.log("GAME STARTING");
	pTagTile = document.getElementById("tileCount");
        grid = document.getElementById("grid");
	board = document.getElementById("board");
	deckTileDiv = document.getElementById("deckTile");
	meepleQuestion = document.getElementById("meepleQuestion");
	curTile = document.getElementById("curTile");
	rotateButton = document.getElementById("rotateImage");
	console.log("geting cookie ID");
	getCookieID();
        startGame();
	console.log("playerCookie=" + playerCookie);
	playerPoll = setInterval(pollTurn, 2000);
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
		            //getValidPlaces("False");
	      
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
		emptyCell.style.position = "relative";
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
	tileCount -= 1;
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
		    var player_id = responseList[0];
		    console.log("!!!player_id= " + player_id);
		    console.log("player=" + player);
		    var oldPlayer = null;
		    if (typeof player !== "undefined" && player !== null){
		        player.style.backgroundColor = "white";
			oldPlayer = player;
		    }
		    player = document.getElementById(player_id);
		    console.log("player after being set= " + player);
		    player.style.backgroundColor = "#D8FA9A";
		    if (player_id == playerCookie){
			//it's your go, get yo tile etc
		        clearInterval(playerPoll);
		        getPlayerTile();
		        getValidPlaces("False");
			rotateButton.addEventListener("click", rotateTile, false);
		    }
		    if (oldPlayer != player){
			tileCount -= 1;
			pTagTile.innerHTML = "Remaining Tiles: " + tileCount;
		        pollBoard();
		    }
                    //TODO: Lock controls to this player
                } 
            }
        }
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
                if (request.responseText.trim() != "problem") {
                    // request.responseText.trim() = "TileAssets/tile.png"
                    // If successful update user display to new player tile
		            console.log("tilepath=" + request.responseText.trim());
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
        // ASK HENRY WHAT EXACTLY THIS LINE DOES
        var image = document.getElementById(cellID).childNodes;
	console.log(currentTile);
        image[0].src = currentTile;
        image[0].className = "placed";
	image[0].style.transform = "rotate(" + rotation + "deg)";
	console.log(image[0]);
        console.log("placed tile");
	tableCellID = cellID;
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
                    if (checkMeeplesRequest.responseText.trim() == ''){
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
        var text = document.createTextNode("Would you like to place a meeple");
        meepleQuestion.appendChild(text);
        for (var i = 0; i < sides.length; i++) {
            var newButton = document.createElement('button');
	    newButton.className = "playButton";
	    console.log("button made for side: " + sides[i]);
            newButton.innerHTML = sides[i];
            meepleQuestion.appendChild(newButton);
            newButton.addEventListener("click", function() { 
                console.log("meeple side been pressed")
                // put the meeple on this side of the grid cell
	        side = this.innerHTML;
	        console.log("side being sent: " + side);
                var url = "cgi-bin/getMeepleImage.py?side=" + side;
                placeMeepleRequest = new XMLHttpRequest();
                placeMeepleRequest.addEventListener("readystatechange", placeMeepleImage, false);
                placeMeepleRequest.open("GET", url, true);
                placeMeepleRequest.send(null);
            }, false);
	    }
        var endGo = document.createElement("button");
        endGo.innerHTML = "NO";
	    meepleQuestion.appendChild(endGo);
	    endGo.style.className = "playButton";
        endGo.addEventListener("click",  endTurn, false);
    }
		

    function placeMeepleImage(){
        // TODO: Needs to place image to correct side of cell
        console.log("place meeple image");
	console.log("PLACE MEEPLE READY state= " + placeMeepleRequest.readyState);
        if (placeMeepleRequest.readyState === 4) {
	    console.log("PLACE MEEPLE IMAGE READY STATE= " + placeMeepleRequest.readyState);
            if (placeMeepleRequest.status === 200) {
		console.log("PLACE MEEPLE IMAGE STATUS= " + placeMeepleRequest.status);
                if (placeMeepleRequest.responseText.trim() != "problem") {
		    console.log("PLACE MEEPLE IMAGE RESPONSE= " + placeMeepleRequest.responseText.trim());
                    var cell = document.getElementById(tableCellID);
                    var meepleImage = document.createElement("img");
		    meepleImage.style.top= "2px";
		    meepleImage.style.left= "4px";
		    meepleImage.style.zIndex = "2";
		    meepleImage.style.position = "absolute";
                    meepleImage.src = placeMeepleRequest.responseText.trim();
                    cell.appendChild(meepleImage);
                    endTurn();
                }
            }
        }
    }
    
    function endTurn(){
	console.log("end turn");
        // Delete any meeple buttons
        meepleQuestion.innerHTML = "";
        tableCellID = null;
	//player.style.backgroundColor = "orange";
	var curdeckTile = curTile.querySelector("img");
	curTile.removeChild(curdeckTile);
	if (tileCount < 0){
	    var winner = scoreboard.childNodes[0];
	    winner = winner.childNodes[0];
	    console.log(winner);
	    window.alert("Game Over!! Winner is " + winner);
	}
	hideValidPlaces();
        getLeaderBoard();
        getNextTurn();
    }

    function getNextTurn(){
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
	var tile = curTile.querySelector("img");
	console.log("rotation = " + rotation);
        if (rotation >= 270){
            rotation = 0;
        } else {
            rotation += 90;
        }
        tile.style.transform = "rotate(" + rotation + "deg)";
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
    }

})();
