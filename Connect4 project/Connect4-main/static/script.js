const ROWS = 6;
const COLUMNS = 7;
let currentPlayer = 'red';
let board = [];
let vsAI = true;

document.addEventListener('DOMContentLoaded', () => {
    createBoard();
    updateTurnIndicator();
    document.getElementById('reset').addEventListener('click', createBoard);

    if (typeof defaultAlgorithm !== 'undefined') {
        document.getElementById('algorithm-select').value = defaultAlgorithm;
        updateAlgoDisplay();
    }
});

async function createBoard() {
    const response = await fetch('/create_board', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    board = data.board;
    document.getElementById('winner-popup').classList.add('hidden');

    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';

    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLUMNS; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.addEventListener('click', () => handleCellClick(row, col));
            boardElement.appendChild(cell);
        }
    }

    updateBoardDisplay();
    currentPlayer = 'red';
    updateTurnIndicator();
}

async function handleCellClick(row, col) {
    if (currentPlayer !== 'red') return;

    const response = await fetch('/make_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            row,
            col,
            player: currentPlayer,
            board
        })
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    board = data.board;
    updateBoardDisplay();

    if (data.winner) {
        setTimeout(() => {
            showWinner(data.winner);
        }, 100);
        return;
    }

    currentPlayer = 'yellow';
    updateTurnIndicator();
    await aiMove();
}

async function aiMove() {
    const algorithm = document.getElementById('algorithm-select').value;

    const response = await fetch('/ai_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            player: currentPlayer,
            board,
            algorithm
        })
    });

    const data = await response.json();

    board = data.board;
    updateBoardDisplay();

    if (data.winner) {
        setTimeout(() => {
            showWinner(data.winner);
        }, 100);
        return;
    }

    currentPlayer = 'red';
    updateTurnIndicator();
}

function updateBoardDisplay() {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS; c++) {
            const cell = document.querySelector(`[data-row="${r}"][data-col="${c}"]`);
            cell.className = 'cell';
            if (board[r][c]) {
                cell.classList.add(board[r][c]);
            }
        }
    }
}

function updateTurnIndicator() {
    const currentPlayerElement = document.getElementById('current-player');
    currentPlayerElement.textContent = currentPlayer.charAt(0).toUpperCase() + currentPlayer.slice(1);
    currentPlayerElement.style.color = currentPlayer;
}

function showWinner(winner) {
    const popup = document.getElementById('winner-popup');
    const msg = document.getElementById('winner-message');
    msg.textContent = winner === 'draw' ? "It's a draw!" : `${winner.charAt(0).toUpperCase() + winner.slice(1)} wins!`;
    popup.classList.remove('hidden');
}
