let board = Array(9).fill(" ");
let gameOver = false; 

const boardDiv = document.getElementById("board");
const status = document.getElementById("status");

function drawBoard() {
    boardDiv.innerHTML = "";
    board.forEach((cell, i) => {
        const div = document.createElement("div");
        div.className = "cell";

        if (cell === "X") div.classList.add("X");
        if (cell === "O") div.classList.add("O");

        div.innerText = cell;

        if (cell === " " && !gameOver) {
            div.addEventListener("click", () => playerMove(i));
        }

        boardDiv.appendChild(div);
    });
}

function playerMove(i) {
    if (gameOver) return;

    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board: board, move: i })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        board = data.board;
        drawBoard();

        if (data.winner) {
            gameOver = true;

            if (data.winner === "Player") {
                showResult("Player won the game!");
            } else if (data.winner === "Computer") {
                showResult("Computer won the game!");
            } else if (data.winner === "Draw") {
                showResult("It's a draw!");
            }
        }
    });
}

function showResult(message) {
    document.getElementById("resultText").innerText = message;
    document.getElementById("resultPopup").style.display = "block";
}

function replayGame() {
    board = Array(9).fill(" ");
    gameOver = false;
    drawBoard();
    status.innerText = "";
    document.getElementById("resultPopup").style.display = "none";
}

function goHome() {
    window.location.href = "/";
}

drawBoard();  
