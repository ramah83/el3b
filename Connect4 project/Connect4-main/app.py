from flask import Flask, request, jsonify, render_template
import math
import copy

app = Flask(__name__)

ROWS = 6
COLUMNS = 7

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    algo = request.args.get('algorithm', 'alphabeta')
    return render_template('board.html', algorithm=algo)

@app.route('/create_board', methods=['POST'])
def create_board():
    board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    return jsonify(board=board)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    row, col, player, board = data['row'], data['col'], data['player'], data['board']

    for r in range(ROWS - 1, -1, -1):
        if board[r][col] is None:
            board[r][col] = player
            if check_win(r, col, player, board):
                return jsonify(board=board, winner=player)
            if is_draw(board):
                return jsonify(board=board, winner='draw')
            return jsonify(board=board, winner=None)

    return jsonify(error='Invalid move'), 400

@app.route('/ai_move', methods=['POST'])
def ai_move():
    data = request.json
    board = data['board']
    player = data['player']
    algorithm = data['algorithm']
    depth = 4  # You can adjust this value based on the desired difficulty level and performance trade-offs.

    if algorithm == 'minimax':
        col, _ = minimax(board, depth, True, player)
    else:
        col, _ = minimax_alpha_beta(board, depth, -math.inf, math.inf, True, player)

    for r in range(ROWS - 1, -1, -1):
        if board[r][col] is None:
            board[r][col] = player
            if check_win(r, col, player, board):
                return jsonify(board=board, winner=player)
            if is_draw(board):
                return jsonify(board=board, winner='draw')
            return jsonify(board=board, winner=None)

    return jsonify(error='AI failed to make a move'), 400

def get_valid_locations(board):
    return [col for col in range(COLUMNS) if board[0][col] is None]

def is_draw(board):
    return all(cell is not None for row in board for cell in row)

def is_terminal_node(board):
    return is_draw(board) or any(check_win(r, c, board[r][c], board)
                                 for r in range(ROWS)
                                 for c in range(COLUMNS)
                                 if board[r][c] is not None)

def score_position(board, player):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player and check_win(r, c, player, board):
                return 100
            elif board[r][c] and check_win(r, c, board[r][c], board):
                return -100
    return 0

def minimax(board, depth, maximizingPlayer, player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        return None, score_position(board, player)

    if maximizingPlayer:
        value = -math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            temp_board = copy.deepcopy(board)
            for r in range(ROWS - 1, -1, -1):
                if temp_board[r][col] is None:
                    temp_board[r][col] = player
                    break
            _, new_score = minimax(temp_board, depth - 1, False, player)
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        value = math.inf
        opponent = 'red' if player == 'yellow' else 'yellow'
        best_col = valid_locations[0]
        for col in valid_locations:
            temp_board = copy.deepcopy(board)
            for r in range(ROWS - 1, -1, -1):
                if temp_board[r][col] is None:
                    temp_board[r][col] = opponent
                    break
            _, new_score = minimax(temp_board, depth - 1, True, player)
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer, player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        return None, score_position(board, player)

    if maximizingPlayer:
        value = -math.inf
        best_col = valid_locations[0]
        for col in valid_locations:
            temp_board = copy.deepcopy(board)
            for r in range(ROWS - 1, -1, -1):
                if temp_board[r][col] is None:
                    temp_board[r][col] = player
                    break
            _, new_score = minimax_alpha_beta(temp_board, depth - 1, alpha, beta, False, player)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        opponent = 'red' if player == 'yellow' else 'yellow'
        best_col = valid_locations[0]
        for col in valid_locations:
            temp_board = copy.deepcopy(board)
            for r in range(ROWS - 1, -1, -1):
                if temp_board[r][col] is None:
                    temp_board[r][col] = opponent
                    break
            _, new_score = minimax_alpha_beta(temp_board, depth - 1, alpha, beta, True, player)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def check_win(row, col, player, board):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        count += count_in_direction(row, col, dr, dc, player, board)
        count += count_in_direction(row, col, -dr, -dc, player, board)
        if count >= 4:
            return True
    return False

def count_in_direction(row, col, dr, dc, player, board):
    count = 0
    r, c = row + dr, col + dc
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
        count += 1
        r += dr
        c += dc
    return count

if __name__ == '__main__':
    app.run(debug=True)
