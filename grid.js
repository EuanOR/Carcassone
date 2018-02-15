(function() {

    var request;
    // Gameboard & sidebar container
    var div;
    // Relative path of image src
    var currentTile;
    // Current rotation of currentTile
    var rotation = 0;
    // Player index e.g. 0, 1, 2, 3
    var player;
    
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
        //Place initial tile in grid cell [0,0]
        console.log("PLACE START TILE");
        placeStartTile(0,0);
        //Get player name
	console.log("made it out");
        getPlayer();
        //Get tile for player's turn
        getPlayerTile();
        //Get valid places where player can place tile
    }

    //CREATE TABLE FOR GAMEBOARD
    function createGameBoard(){
        // Create HTML table
        var table = document.createElement('table');
        table.cellPadding = "0";
        table.cellSpacing = "0";
        var tableBody = document.createElement('tbody');
        console.log("table made");
        // y-coordinate for cell
        var yStart = -1;

        for (var i = 0; i < 3; i++){
            // Create row
            var row = document.createElement("tr");

            // x-coordinate for cell
            var xStart = -1;
            for (var j = 0; j < 3; j++){
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
                xStart ++;
            }
            // Increment cell position
            yStart ++;
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
        var url = "getPlayer.py";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", playerReceived, false);
        request.open("GET", url, true);
        request.send(null);
    }

    // Handler for 'getPlayer()'
    function playerReceived(){
        console.log("player received");
        if (request.readyState === 4) {
	    console.log("ready");
            if (request.status === 200) {
		console.log("OK");
                if (request.responseText.trim() != "problem") {
		    console.log("success");
                    //TODO: update display to show who's turn it is
                    // request.responseText.trim() = player index in GameController players array
                    // e.g. 0, 1, 2, 3

                    var player = document.getElementById(request.responseText.trim());
                    player.className = "active";

                    //TODO: Lock controls to this player
                } 
            }
        }

    }

    //GET PLAYER THEIR TILE FOR THIS TURN
    function getPlayerTile(){
        var url = "getTile.py";
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
        var div = document.getElementById("deckTile");
        var image = document.createElement("img");
        image.src = tilePath;
        currentTile = tilePath;
        div.appendChild(image);
    }

    //SHOW AVAILABLE VALID CELLS
    function getValidPlaces(rotation){
        // Get array of available, valid cells
        var url = "getValidPlaces.py?rotation=" + rotation;
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
        image[0].src = currentTile;
        image[0].className = "placed";
        console.log("placed tile");
        hideValidPlaces();
        //TODO: Update table to show new tile placement
        //TODO: Send cell information to GameController
        placeMeeple();
        updateScore();
        nextTurn();
    }

    function placeMeeple(){
        //TODO: ask GameController if meeple can be placed
        //if meeple placement possible
        //  ask user do you want to place meeple?
        //  if True
        //      place meeple
        //      update display
        //      send info back to game controller
        //  else:
        //      return
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
        // ASK CATHY
        if (rotation >= 3){
            rotation = 0;
        } else {
            rotation ++;
        }
        getValidPlaces(rotation);
    }

    // Called in 'placeTile()'
    function updateScore(){
        //TODO: GET SCORE FROM GAME CONTROLLER
        var url = "getScore.py" + rotation;
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", scoreReceived, false);
        request.open("GET", url, true);
        request.send(null);
    }

    // Handles 'updateScore()'
    function scoreReceived(){
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() != "problem") {
                    // scores = [21, 34, 12, 24]
                    // scores[0] = Player 1's score
                    var scores = request.responseText.trim().split(" ");
                    //TODO: UPDATE LEADERBOARD
                }
            }
        }
    }

})();
