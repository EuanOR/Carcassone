(function() {

    var request;
    var leaderboardRequest;
    var playerRequest;
    // Gameboard & sidebar container
    var div;
    // Relative path of image src
    var currentTile;
    // Current rotation of currentTile
    var rotation = 0;
    // Player index e.g. 0, 1, 2, 3
    var player;
    var tableCellID;
    var startArray = [];
    
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        console.log("GAME STARTING");
        div = document.getElementById("grid");
        startGame();
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
        getPlayer();
        //Get tile for player's turn
        //getPlayerTile();
    }

    //CREATE TABLE FOR GAMEBOARD
    function createGameBoard(){
        // Create HTML table
        var table = document.createElement('table');
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
        div.appendChild(table);
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

        // Array of inital valid places
        startArray = ["1,0","-1,0"];

        showValidPlaces(startArray);
        showPlayerTile("TileAssets/Start.png");
    }

    // Get current Player name and meeples etc.
    function getPlayer(){
	console.log("getting player");
        var url = "cgi-bin/getPlayer.py";
        playerRequest = new XMLHttpRequest();
        playerRequest.addEventListener("readystatechange", playerReceived, false);
        playerRequest.open("GET", url, true);
        playerRequest.send(null);
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
                    //TODO: update display to show who's turn it is
                    // request.responseText.trim() = player index in GameController players array
                    // e.g. 0, 1, 2, 3

                    var player = document.getElementById(playerRequest.responseText.trim());
                    player.className = "active";

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
                    showPlayerTile(request.responseText.trim());    
                }
            }
        }
    }

    function showPlayerTile(tilePath){
	console.log("SHOWING A PLAYER TILE");
        var div = document.getElementById("deckTile");
        var image = document.createElement("img");
        image.src = tilePath;
	console.log(tilePath);
        currentTile = tilePath;
	console.log(currentTile);
	
        div.appendChild(image);
    }

    //SHOW AVAILABLE VALID CELLS
    function getValidPlaces(rotation){
        // Get array of available, valid cells
        var url = "cgi-bin/getValidPlaces.py?rotation=" + rotation;
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", validPlacesReceived, false);
        request.open("GET", url, true);
        request.send(null);
    }

    // Handles 'getValidPlaces()'
    function validPlacesReceived(){
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() != "problem") {
                    // If successful get list of valid cell locations
                    startArray = request.responseText.trim().split(" ");
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
	console.log(image[0]);
        console.log("placed tile");
	tableCellID = cellID;
        checkMeeplePlacements();
    }
    
    function checkMeeplePlacements(){
	console.log("meeples pls");
        // Check if a meeple can be placed
        var url = "cgi-bin/getMeeplePlacements.py";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", canMeepleBePlaced, false);
        request.open("GET", url, true);
        request.send(null);
    }
    
    function canMeepleBePlaced(){
	console.log("can meeples be placed");
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() != "problem") {
                    // If no
                    if (request.responseText.trim() == 0){
                        endTurn();
                    }
                    // else return places
                    else {
                        var placements = request.responseText.trim()
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
        meepleQuestion = document.getElementById("meepleQuestion");
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
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", placeMeepleImage(side), false);
        request.open("GET", url, true);
        request.send(null);
    }
		

    function placeMeepleImage(side){
        // TODO: Needs to place image to correct side of cell
		
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() != "problem") {
                    cell = document.getElementById(tableCellID);
                    var meepleImage = document.createElement("img");
                    meepleImage.src = request.responseText.trim();
                    cell.appendChild(meepleImage);
                    //cell.childNode.style.
                }
            }
        }
    }
    
    function endTurn(){
	console.log("end turn");
        // Delete any meeple buttons
        meepleQuestion.innerHTML = "";
        tableCellID = null;
	hideValidPlaces();
        updateLeaderBoard();
        nextTurn();
    }

    function nextTurn(){
        rotation = 0;
        getPlayer();
        getPlayerTile();
        getValidPlaces(rotation);
    }

    function rotateTile(){
        //TODO: update user of tile rotation display
        // Can do with CSS or JQUERY 
        console.log("PLACE START TILE");
        // ASK CATHY
        if (rotation >= 3){
            rotation = 0;
        } else {
            rotation ++;
        }
        getValidPlaces(rotation);
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
	console.log("newLeaderboard = " +newLeaderboard);
	scoreboard.innerHTML = newLeaderboard;
    }

})();