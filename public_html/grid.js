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
    // Gameboard & sidebar container
    var grid;
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
    // Player tile
    var deckTileDiv;
    // Game grid
    var table;
    
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        console.log("GAME STARTING");
        grid = document.getElementById("grid");
	rotateButton = document.getElementById("rotateButton");
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
	    if (boardRequest.status === 200){
		console.log("OK");
		if (boardRequest.responseText.trim() != "problem"){
		    table.innerHTML = boardRequest.responseText.trim();
	      
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
        grid.appendChild(table);
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
                    //TODO: update display to show who's turn it is
                    // request.responseText.trim() = player id + name
		    console.log("!!!player_id= " + player_id);
		    
		    console.log("player=" + player);
		    if (player != null){
		      player.style.backgroundColor = "orange";
		    }
		    player = document.getElementById(player_id);
		    player.style.backgroundColor = "blue";
		    if (player_id == playerCookie){
			//it's your go, get yo tile etc
		        clearInterval(playerPoll);
		        getPlayerTile();
		        getValidPlaces("False");
			rotateButton.addEventListener("click", rotateTile, false);
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
        deckTileDiv = document.getElementById("deckTile");
        var image = document.createElement("img");
	tilePath = "TileAssets/" + tilePath;
        image.src = tilePath;
	console.log(tilePath);
        currentTile = tilePath;
	console.log(currentTile);
	
        deckTileDiv.appendChild(image);
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
        for (var i=0; i < startArray.length; i++) {

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
        checkMeeplePlacements();
    }
    
    function checkMeeplePlacements(){
	console.log("meeples pls");
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
                    if (checkMeeplesRequest.responseText.trim() == '[]'){
			console.log("No meeples");
                        endTurn();
                    }
                    // else return places
                    else {
                        var placements = checkMeeplesRequest.responseText.trim();
                        placeMeeple(placements);    
                    } 
                }
            }
        }
    }

    function placeMeeple(placements){
	console.log("meeple is placed");
        //  ask user do you want to place meeple?
        //  if True
        var meepleQuestion = document.getElementById("meepleQuestion");
        var text = document.createTextNode("Would you like to place a meeple");
        meepleQuestion.appendChild(text);
        for (i = 0; i < placements.length; i++) {
            newButton = document.createElement('button');
            newButton.innerHTML = meeplePlacements[i];
            meepleQuestion.appendChild(newButton);
            newButton.onclick = function () {
                meeplePlacementPressed(placements[i]);
                endTurn();
            }
	}
        var endGo = document.createElement("button");
        endGo.innerHTML = "I don't want to place a meeple";
        endGo.onclick = function () {
            endTurn();
        }
    }
    
    function meeplePlacementPressed(side) {
        // put the meeple on this side of the grid cell
        var url = "cgi-bin/getMeepleImage.py";
        placeMeepleRequest = new XMLHttpRequest();
        placeMeepleRequest.addEventListener("readystatechange", placeMeepleImage(side), false);
        placeMeepleRequest.open("GET", url, true);
        placeMeepleRequest.send(null);
    }
		

    function placeMeepleImage(side){
        // TODO: Needs to place image to correct side of cell
		
        if (placeMeepleRequest.readyState === 4) {
            if (placeMeepleRequest.status === 200) {
                if (placeMeepleRequest.responseText.trim() != "problem") {
                    cell = document.getElementById(tableCellID);
                    var meepleImage = document.createElement("img");
                    meepleImage.src = placeMeepleRequest.responseText.trim();
                    cell.appendChild(meepleImage);
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
	var curdeckTile = deckTileDiv.querySelector("img");
	deckTileDiv.removeChild(curdeckTile);
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
                if (nextTurnRequest.responseText.trim() == "success") {
		    console.log("no problem");
		    pollTurn();
		    playerPoll = setInterval(pollTurn, 2000);
		}
	    }
      }
    }

    function rotateTile(){
	var div = document.getElementById("deckTile");
	var tile = div.querySelector("img");
        if (rotation >= 270){
            rotation = 0;
        } else {
            rotation += 90;;
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
	console.log("readyState= " +leaderboardRequest.readyState);
        if (leaderboardRequest.readyState === 4) {
	    console.log("resonse = " +leaderboardRequest.responseText.trim());
            if (leaderboardRequest.status === 200) {
		console.log("status= " + leaderboardRequest.status);
                if (leaderboardRequest.responseText.trim() != "problem") {
		    console.log("no problem");
		    updateLeaderboard(leaderboardRequest.responseText.trim());
                    //TODO: UPDATE LEADERBOARD
                }
            }
        }
      console.log("END LEADERBOARD");
    }
    
    function updateLeaderboard(newLeaderboard){
	console.log("updating leaderboard");
	scoreboard = document.getElementById("scoreboard");
	console.log("newLeaderboard = " + newLeaderboard);
	scoreboard.innerHTML = newLeaderboard;
    }

})();
