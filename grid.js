    (function() {

    var div;
    var mostRight;
    var availableArray = [];

    var nextTile;

    document.addEventListener("DOMContentLoaded", init, false);

    function init() {
        div = document.querySelector("div");
        createTable();
        placeInitialTile(0,0);

        showAvailableTiles(availableArray);
        showDeckTile("./TileAssets/3T4R2G.png");
    }


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
                cell.id = ((xStart).toString()).concat((yStart.toString()));

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

    function placeInitialTile(x,y) {
        var stringLocation = (x.toString()).concat( (y.toString())); 
        var cell = document.getElementById(stringLocation);

        var image = document.createElement('img');
        image.src = "./TileAssets/Start.png";
        image.className = "placed";
        cell.innerHTML = "";
        cell.appendChild(image);

        availableArray = ["01","10", "0-1", "-10"];

        showAvailableTiles(availableArray);
    }

    function showAvailableTiles(xYList) {
        for (var i=0; i < xYList.length; i++) {

            var cellImage = document.getElementById(xYList[i]).firstChild;

            cellImage.style.visibility = "visible";
            cellImage.className = "available";

            cellImage.addEventListener("click", function() { insertTile(this.parentNode.id);});
        }
    }
    function insertTile(id) {
        var image = document.getElementById(id).childNodes;

        image[0].src = nextTile;

        image[0].className = "placed";

        hideAvailableTiles();

        //TODO: get a new tile from TileDeck + display it
        //TODO: get the new available Tiles from python.
        //TODO: Display the available tiles


    }

    function hideAvailableTiles() {
        var unplacedCellImages = Array.from(document.getElementsByClassName("available"));

        for (var i=0; i < unplacedCellImages.length; i++) {
            unplacedCellImages[i].className = "unplaced";
            unplacedCellImages[i].setAttribute("style", "visibility:hidden");

            unplacedCellImages[i].removeEventListener("click", function() {insertTile(this.parentNode.id);});
        }
    }

    function showDeckTile(tilePath) {
        var div = document.getElementById("deckTile");

        var image = document.createElement("img");
        image.src = tilePath;
        div.appendChild(image);
        nextTile = tilePath;
    }
}) ();