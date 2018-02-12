    (function() {


    /* I have set some protocols for the table.
    *  Every cell in the table is have an co-ordinate id attribute. -> "0,1" "1,-1"
    *  The valid tile image (FreeTile.png) tag has a class name of "unplaced".
    *  Valid tiles (FreeTile.png) image are in every cell once the grid is created but it is set to hidden.
    *  If a table cell is taken, the tile image tag will be set to "placed"
    *  The use of IDs and Class names are so that you can retrieve all the elements by class name or id easier.
    *  For example if you want the the cell at location -1, 2, call document.getElementbyId(id)
    */

    var div;
    var validPlacesArray = [];

    var nextTile;

    document.addEventListener("DOMContentLoaded", init, false);

    function init() {
        div = document.querySelector("div");
        createTable();
        placeInitialTile(0,0);

        showAvailableTiles(validPlacesArray);

        // Required to get a tile off the tile deck display it. At the moment im just using a random tile and displaying it.
        showDeckTile("./TileAssets/3T4R2G.png");
        testAJAX();
    }

    function testAJAX() {
        var url = "test.py?function=printString&paramname='hi'";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", handle_response, false);
        request.open("GET", url, true);
        request.send(null);
    }

    function handle_response() {
        if (request.readyState === 4) {
            if (request.status === 200) {
                if (request.responseText.trim() === "success") {
                    listOfStrings = request.responseText.trim().split(" ");
                    console.log(listOfStrings);
                } 
            }
        }
    }


    // A function to create a 2D html table. Each cell has an co-ordinate ID attribute -> "0,0" , "-1,0"
    function createTable() {
        var table = document.createElement('table');
        table.cellPadding = "0";
        table.cellSpacing = "0";
        var tableBody = document.createElement('tbody');

        var yStart = 1
        for (var i=0; i < 3; i++) {
            var xStart = -1;

            var row = document.createElement("tr");
            for (var i2=0; i2 < 3; i2++) {
                var cell = document.createElement("td");
                cell.id = (((xStart).toString()).concat(",")).concat((yStart.toString()));

                var freeTileImage = document.createElement('img');
                freeTileImage.src = "./TileAssets/FreeTile.png";
                freeTileImage.className = "unplaced";
                freeTileImage.style.visibility = "hidden";
                cell.appendChild(freeTileImage);
                row.appendChild(cell);
                xStart ++;
            }
            yStart--;
            tableBody.appendChild(row);
        }
        table.appendChild(tableBody);
        div.appendChild(table);
        table.setAttribute("border", "1");
    }


    // A function to place the initial tile onto the table.
    function placeInitialTile(x,y) {

        // Construct a variable containing the string of x y co-ordinate -> param X and Y will turn into "X,Y". Eg X = 1, Y = 0 -> "1,0"
        var stringLocation = (x.toString()).concat(",").concat((y.toString()));

        var cell = document.getElementById(stringLocation);

        // Creating a img element and append it to the center cell (initial tile)
        var image = document.createElement('img');
        image.src = "./TileAssets/Start.PNG";
        image.className = "placed";
        cell.innerHTML = "";
        cell.appendChild(image);

        // This only shows the available locations rather than valid places. Need ajax to retrieve valid location.
        validPlacesArray = ["0,1","1,0", "0,-1", "-1,0"];

        showAvailableTiles(validPlacesArray);
    }

    // A function to show all the valid places on the table.
    // If it is valid it will display a valid image on the table (FreeTile.png)
    // Param validCoordinates should be a list that is retrieved by ajax of the valid coordinates.
    function showAvailableTiles(validCoordinates) {
        for (var i=0; i < validCoordinates.length; i++) {

            var cellImage = document.getElementById(validCoordinates[i]).firstChild;

            cellImage.style.visibility = "visible";
            cellImage.className = "available";

            cellImage.addEventListener("click", function() { insertTile(this.parentNode.id);});
        }
    }

    // Insert a tile to the grid.
    // Param id is a string of the cell's ID attribute that we want to place the tile to.
    // NOT COMPLETED
    function insertTile(id) {
        var image = document.getElementById(id).childNodes;

        image[0].src = nextTile;

        image[0].className = "placed";

        hideAvailableTiles();

        //TODO: get a new tile from TileDeck + display it
        //TODO: get the new available Tiles from python.
        //TODO: Display the available tiles
    }

    // Function to hide all available tiles. 
    // This function should be used when a tile is placed and we need to hide all the valid places for the next tile.
    function hideAvailableTiles() {
        var unplacedCellImages = Array.from(document.getElementsByClassName("available"));

        for (var i=0; i < unplacedCellImages.length; i++) {
            unplacedCellImages[i].className = "unplaced";
            unplacedCellImages[i].setAttribute("style", "visibility:hidden");

            unplacedCellImages[i].removeEventListener("click", function() {insertTile(this.parentNode.id);});
        }
    }

    // A function to display the tile to the deckTile DIV.
    function showDeckTile(tilePath) {
        var div = document.getElementById("deckTile");

        var image = document.createElement("img");
        image.src = tilePath;
        div.appendChild(image);
        nextTile = tilePath;
    }
}) 
();
