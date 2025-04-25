from flask import Flask, render_template, request, jsonify
from minimax import check_winner, is_draw, best_move_pure, best_move_ab

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/game")
def game():
    algo = request.args.get("algo", "alphabeta")
    algo_name = "MiniMax" if algo == "minimax" else "Alpha-Beta Pruning"
    return render_template("index.html", algo=algo_name, algo_code=algo)

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data["board"]
    player_move = data["move"]
    algo = data.get("algo", "alphabeta") 

    if board[player_move] != " ":
        return jsonify({"error": "Invalid move"})

    board[player_move] = "X"
    if check_winner(board, 'X'):
        return jsonify({"board": board, "winner": "Player"})

    if is_draw(board):
        return jsonify({"board": board, "winner": "Draw"})


    if algo == "minimax":
        comp_move = best_move_pure(board)
    else:
        comp_move = best_move_ab(board)

    if comp_move is not None:
        board[comp_move] = "O"
        if check_winner(board, 'O'):
            return jsonify({"board": board, "winner": "Computer"})

    if is_draw(board):
        return jsonify({"board": board, "winner": "Draw"})

    return jsonify({"board": board, "winner": None})

if __name__ == "__main__":
    app.run(debug=True, port=5500)
