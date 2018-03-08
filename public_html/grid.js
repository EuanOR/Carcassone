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
    // Game winner
    var winner;
    //Audio files
    var background;
    var defeat;
    var draw;
    var placeM;
    var placeT;
    var point;
    var rotate;
    var victory;
    
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        // Get audio files
	background = new Audio("AudioAssets/background_music.mp3");
	defeat = new Audio("AudioAssets/defeat_fanfare.mp3");
	draw = new Audio("AudioAssets/draw_tile.mp3");
	placeM = new Audio("AudioAssets/place_meeple.mp3");
	placeT = new Audio("AudioAssets/place_tile.mp3");
	point = new Audio("AudioAssets/point_gain.mp3");
	rotate = new Audio("AudioAssets/rotate_tile.mp3");
	victory = new Audio("AudioAssets/victory_fanfare.mp3");
	pTagTile = document.getElementById("tileCount");
        grid = document.getElementById("grid");
	board = document.getElementById("board");
	deckTileDiv = document.getElementById("deckTile");
	meepleQuestion = document.getElementById("meepleQuestion");
	curTile = document.getElementById("curTile");
	rotateButton = document.getElementById("rotateImage");
	//Start background music
	background.addEventListener("ended", restartMusic, false);
	background.volume = 0.5;
	background.load();
	background.play();
	getCookieID();
        startGame();
	// Poll for next players turn every 2 seconds
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
        var url = "cgi-bin/getCookie.py";
        cookieRequest = new XMLHttpRequest();
        cookieRequest.addEventListener("readystatechange", cookieReceived, false);
        cookieRequest.open("GET", url, true);
        cookieRequest.send(null); 
    }
    
    // Handler of 'getCookieID' function
    function cookieReceived(){
        if (cookieRequest.readyState === 4) {
            if (cookieRequest.status === 200) {
                if (cookieRequest.responseText.trim() != "problem") {
		    playerCookie = cookieRequest.responseText.trim();
		}
	    }
	}
    }
    
    // Poll for next players turn
    function pollTurn(){
        // Create AJAX request
        var url = "cgi-bin/getPlayer.py";
        playerRequest = new XMLHttpRequest();
        playerRequest.addEventListener("readystatechange", playerReceived, false);
        playerRequest.open("GET", url, true);
        playerRequest.send(null); 
    }
    
    // Ask for game board updates
    function pollBoard(){
        // Create AJAX request
        var url = "cgi-bin/getBoard.py";
        boardRequest = new XMLHttpRequest();
        boardRequest.addEventListener("readystatechange", boardReceived, false);
        boardRequest.open("GET", url, true);
        boardRequest.send(null); 
    }
    
    
    // Handles 'pollBoard'
    function boardReceived(){
	if (boardRequest.readyState === 4){
	    if (boardRequest.status === 200){
		 if (boardRequest.responseText.trim() != "problem"){
		     //Update board
		     table.innerHTML = boardRequest.responseText.trim();
		     if (currentlyPlaying === true){
		         //If you are the current player show valid tile placements
		         getValidPlaces("False");
		     }
	      
		  }
	     }
	}
    }

    //STARTS GAME
    function startGame(){
        //Create gameboard
        createGameBoard();
	//Create initial leaderboard;
	getLeaderBoard();
	//Place initial tile in grid cell [0,0]
        placeStartTile(0,0);
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
        // Cell to place start tile
	var ID = (x.toString()).concat(",").concat((y.toString()));
	var cell = document.getElementById(ID);
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
        if (playerRequest.readyState === 4) {
            if (playerRequest.status === 200) {
                if (playerRequest.responseText.trim() != "problem") {
		  
		    // Responses from server
		    // [playerID, player name, remaining number of tiles, gameOver check]
		    var responseList = playerRequest.responseText.trim().split(",");
		    var player_id = responseList[0];
		    tileCount = responseList[2];
		    var gameOver = responseList[3];
		    
		    // GAME OVER
		    if (gameOver === "True"){
			endGame();
			return;
		    }

		    var oldPlayer = null;
		    
		    // START OF GAME: DID WE GET THE PLAYER
		    if (typeof player !== "undefined" && player !== null){
		        player.style.backgroundColor = "white";
			oldPlayer = player;
		    }
		    player = document.getElementById(player_id);
		    player.style.backgroundColor = "#D8FA9A";
		    
		    // EVERY TIME A TURN CHANGES
		    if (oldPlayer != player){
			pTagTile.innerHTML = "Remaining Tiles: " + tileCount;
		        pollBoard();
			getLeaderBoard();
		    }
		    
		    // CURRENT PLAYERS TURN
		    if (player_id == playerCookie){
		        currentlyPlaying = true;
			// If its your turn stop polling for a player
		        clearInterval(playerPoll);
			// Set tile rotation back to 0 degrees
			rotation = 0;
			// Get current players tile
		        getPlayerTile();
			// Update user of remaining tiles
			pTagTile.innerHTML = "Remaining Tiles: " + tileCount;
			// Get valid tile placements for players tile
		        getValidPlaces("False");
			// Add event listener to rotate tile button
			rotateButton.addEventListener("click", rotateTile, false);
			// Get most recent leaderboard
			getLeaderBoard();
			// Update user display who is the current player
			player.style.backgroundColor = "#D8FA9A";
		    }
		    
                } 
            }
        }
    }
    
    // End game function - display winner name 
    function endGame(){
        // Stop polling for new player
        clearInterval(playerPoll);
	// Get most recent scores with updated leaderboard
        getLeaderBoard();
	var rows = scoreboard.getElementsByTagName('tr');
	winner = scoreboard.rows[1].cells[0].innerHTML;
	window.alert("Game Over!! Winner is " + winner + "!!");
	victory.load();
	victory.play();
    }
    
    // Get player tile from server
    function getPlayerTile(){
        // Create AJAX request
        var url = "cgi-bin/getTile.py";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", tileReceived, false);
        request.open("GET", url, true);
        request.send(null);    
    }
    
    // Handles 'getPlayerTile'
    function tileReceived(){
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() != "problem") {
                    // request.responseText.trim() = "TileAssets/tile.png"
                    // If successful update user display to new player tile
                    showPlayerTile(request.responseText.trim());    
                }
            }
        }
    }
    
    // Display players current tile
    function showPlayerTile(tilePath){
        var image = document.createElement("img");
	tilePath = "TileAssets/" + tilePath;
        image.src = tilePath;
        currentTile = tilePath;
        curTile.appendChild(image);
	draw.load();
	draw.play();
    }

    //Gets valid tile placements from server
    function getValidPlaces(rotate){
        // Get array of available, valid cells
        // Create AJAX request
        var url = "cgi-bin/getValidPlaces.py?rotate=" + rotate;
        validPlacesRequest = new XMLHttpRequest();
        validPlacesRequest.addEventListener("readystatechange", validPlacesReceived, false);
        validPlacesRequest.open("GET", url, true);
        validPlacesRequest.send(null);
    }

    // Handles 'getValidPlaces()'
    function validPlacesReceived(){
        if (validPlacesRequest.readyState === 4) {
            if (validPlacesRequest.status === 200) {
                if (validPlacesRequest.responseText.trim() != "problem") {
                    // If successful get list of valid cell locations
                    var startArray = validPlacesRequest.responseText.trim().split(" ");
		    if (rotateActive === false){
		      // Allow user to rotate tile again now that board is updated
		      rotateButton.addEventListener("click", rotateTile, false);
		      rotateActive = true;
		    }
		    //Display valid tile placements to user
                    showValidPlaces(startArray);  
                }
            }
        }
    }
    
    //Show valid tile placements - usually at start of players turn
    function showValidPlaces(startArray){
        for (var i=0; i < startArray.length; i++) {
            var cellImage = document.getElementById(startArray[i]).firstChild;
            cellImage.style.visibility = "visible";
            cellImage.className = "available";

            // Add event listeners to valid empty cells
            cellImage.addEventListener("click", function() { placeTile(this.parentNode.id);});
        }
    }

    //Hides valid tile placements - usually at end of a players turn
    function hideValidPlaces(){
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

    // Player places their tile
    function placeTile(cellID){
        var image = document.getElementById(cellID).childNodes;
        image[0].src = currentTile;
        image[0].className = "placed";
	// place tile on board according to user rotation choice
	image[0].style.transform = "rotate(" + rotation + "deg)";
	tableCellID = cellID;
	placeT.load();
	placeT.play();
	// Hide current calid places now that user has placed tile
	hideValidPlaces();
	// Create AJAX request
	var url = "cgi-bin/placeTile.py?cellID=" + cellID;
        placeTileRequest = new XMLHttpRequest();
        placeTileRequest.addEventListener("readystatechange", tilePlaced, false);
        placeTileRequest.open("GET", url, true);
        placeTileRequest.send(null);
    }
    
    // Handler for 'placeTile'
    function tilePlaced(){
        if (placeTileRequest.readyState === 4) {
            if (placeTileRequest.status === 200) {
                if (placeTileRequest.responseText.trim() === "placed") {
		    checkMeeplePlacements();
		} else if (placeTileRequest.responseText.trim() !== "problem"){
		    checkMeeplePlacements();
		} else {
		    endTurn();
		}
	     }
	 }
    }
    
    // Ask server is a meeple can be placed
    function checkMeeplePlacements(){
        //Create AJAX request
	meepleQuestion = document.getElementById("meepleQuestion");
        // Check if a meeple can be placed
        var url = "cgi-bin/getMeeplePlacements.py";
        checkMeeplesRequest = new XMLHttpRequest();
        checkMeeplesRequest.addEventListener("readystatechange", canMeepleBePlaced, false);
        checkMeeplesRequest.open("GET", url, true);
        checkMeeplesRequest.send(null);
    }
    
    // 'Handles checkMeeplePlacements'
    function canMeepleBePlaced(){
        if (checkMeeplesRequest.readyState === 4) {
            if (checkMeeplesRequest.status === 200) {
                if (checkMeeplesRequest.responseText.trim() != "problem") {
		    //if no meeple placements, end turn
                    if (checkMeeplesRequest.responseText.trim() === ''){
                        endTurn();
                    }
                    // else display meeple placement options to user
                    else {
                        var sides = checkMeeplesRequest.responseText.trim().split(",");
                        placeMeeple(sides);    
                    } 
                }
            }
        }
    }

    function placeMeeple(sides){
        meepleQuestion.innerHTML = "";
	var pTag = document.createElement("p");
	pTag.className = "sideboardHeadings";
	//Does the user want to place a meeple
        var text = document.createTextNode("Place a meeple?");
	pTag.appendChild(text);
        meepleQuestion.appendChild(pTag);
        for (var i = 0; i < sides.length; i++) {
	    //Display all possible meeple placement choices to user
            var newButton = document.createElement('button');
	    newButton.className = "meepleButtons";
            newButton.innerHTML = sides[i];
            meepleQuestion.appendChild(newButton);
            newButton.addEventListener("click", function() { 
                // put the meeple on this side of the grid cell
	        side = this.innerHTML;
		//Create AJAX request
                var url = "cgi-bin/getMeepleImage.py?side=" + side;
                placeMeepleRequest = new XMLHttpRequest();
                placeMeepleRequest.addEventListener("readystatechange", placeMeepleImage, false);
                placeMeepleRequest.open("GET", url, true);
                placeMeepleRequest.send(null);
	    }, false);
	    placeM.load();
	    placeM.play();
	    }
	//Add a 'No' option to placing a meeple.
        var endGo = document.createElement("button");
        endGo.innerHTML = "No";
	meepleQuestion.appendChild(endGo);
	endGo.className = "meepleButtons";
        endGo.addEventListener("click",  endTurn, false);
    }
		

    function placeMeepleImage(){
	placeM.play();
        if (placeMeepleRequest.readyState === 4) {
            if (placeMeepleRequest.status === 200) {
                if (placeMeepleRequest.responseText.trim() != "problem") {
		    //Place meeple image in correct table cell
                    var cell = document.getElementById(tableCellID);
                    var meepleImage = document.createElement("img");
		    //Set styling so meeple image appears above tile image
		    meepleImage.style.zIndex = "2";
		    meepleImage.style.position = "relative";
                    meepleImage.src = placeMeepleRequest.responseText.trim();
                    cell.appendChild(meepleImage);
		    //Finish players turn
                    endTurn();
                }
            }
        }
    }
    
    // End turn function
    function endTurn(){
	// This user is no longer currentlyPlaying
        currentlyPlaying = false;
        // Delete any meeple buttons
        meepleQuestion.innerHTML = "";
        tableCellID = null;
	//Remove their tile image from the sidebar
	var curdeckTile = curTile.querySelector("img");
	curTile.removeChild(curdeckTile);
	//Hide valid places
	hideValidPlaces();
	//Update Leaderboard
        getLeaderBoard();
	//Set next players turn
        getNextTurn();
    }
    
    // Sets next players turn
    function getNextTurn(){
	// Create AJAX request
        rotateButton.removeEventListener("click", rotateTile, false);
	// Reset tile rotation to 0 degrees
        rotation = 0;
	var url = "cgi-bin/getNextTurn.py";
        nextTurnRequest = new XMLHttpRequest();
        nextTurnRequest.addEventListener("readystatechange", nextTurnReceived, false);
        nextTurnRequest.open("GET", url, true);
        nextTurnRequest.send(null); 
    }
    
    // Handler for 'getNextTurn'
    function nextTurnReceived(){
        if (nextTurnRequest.readyState === 4) {
            if (nextTurnRequest.status === 200) {
                if (nextTurnRequest.responseText.trim() == "success") {
		    // If the server has changed to the next player successfully
		    // Get next players turn
		    pollTurn();
		    playerPoll = setInterval(pollTurn, 2000);
		}
	    }
        }
    }

    function rotateTile(){
	//Remove event listener until computations complete
        rotateButton.removeEventListener("click", rotateTile, false);
	rotateActive = false;
	var tile = curTile.querySelector("img");
        if (rotation >= 270){
            rotation = 0;
        } else {
            rotation += 90;
        }
        //Update user disply to correct rotation of the tile
        tile.style.transform = "rotate(" + rotation + "deg)";
	rotate.load();
	rotate.play();
	//Hide current valid places
	hideValidPlaces();
	//Get new valid places for rotated tile
        getValidPlaces("True");
	
    }

    //Calls for updated scoreboard for user display 
    function getLeaderBoard(){
	//Create AJAX request
        var url = "cgi-bin/Scoreboard.py";
        leaderboardRequest = new XMLHttpRequest();
        leaderboardRequest.addEventListener("readystatechange", leaderboardReceived, false);
        leaderboardRequest.open("GET", url, true);
        leaderboardRequest.send(null);
    }

    // Handles 'getLeaderBoard()'
    function leaderboardReceived(){
        if (leaderboardRequest.readyState === 4) {
            if (leaderboardRequest.status === 200) {
                if (leaderboardRequest.responseText.trim() != "problem") {
		    //Pass updated scoreboard to 'updateLeaderboard'
		    updateLeaderboard(leaderboardRequest.responseText.trim());
                }
            }
        }
    }
    
    function updateLeaderboard(newLeaderboard){
	// Update user display of new scoreboard
        scoreboard = document.getElementById("scoreboard");
        scoreboard.innerHTML = newLeaderboard;
	// Set current player style to a light green
	if (typeof player !== "undefined" && player !== null){
 	    player.style.backgroundColor = "#D8FA9A";
	}
    }

})();
