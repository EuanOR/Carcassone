(function(){

    // <p> to place a little message about num of players left to join
    var playerCountParagraph;
    var playerCount;
    var request;
    document.addEventListener("DOMContentLoaded", init, false);

    function init(){
        playerCountParagraph = document.querySelector("#playerCount");
        setInterval(getPlayerCount, 1000);
    }

    // Get current Player name and meeples etc.
    function getPlayerCount(){
        var url = "getPlayerCount.py";
        request = new XMLHttpRequest();
        request.addEventListener("readystatechange", playerCountReceived, false);
        request.open("GET", url, true);
        request.send(null);
    }

    // Handler for 'getPlayerCount()'
    function playerCountReceived(){
        console.log(request.readyState, request.status );
        if (request.readyState === 4) {
            if (request.status === 200) {
                console.log(request.responseText.trim());
                if (request.responseText.trim() != "problem") {
                    // playerCount is a number between 1 and 4
                    playerCount = parseInt(request.responseText.trim());
                    // waitingOn is the number of players still needed to join before we can start
                    var waitingOn = 4 - playerCount;
                    if (waitingOn == 0){
                        // all players have joined. Redirects you to game page
                        window.location.href = "Carcassone.html";
                    } else if (waitingOn == 1){
                        // print number of players left to join
                        playerCountParagraph.innerHTML = "Waiting on " + waitingOn + " player";
                    } else {
                        // print number of players left to join
                        playerCountParagraph.innerHTML = "Waiting on " + waitingOn + " players";
                    } 
                } 
            }
        }
    }



})();
 
