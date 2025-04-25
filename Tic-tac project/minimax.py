def check_winner(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def is_draw(board):
    return all(cell != ' ' for cell in board)

def minimax(board, depth, is_max, alpha, beta):
    if check_winner(board, 'O'): return 1
    if check_winner(board, 'X'): return -1
    if is_draw(board): return 0

    if is_max:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
        return min_eval

def best_move_ab(board):
    best_val = -float('inf')
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_val = minimax(board, 0, False, -float('inf'), float('inf'))
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

def pure_minimax(board, depth, is_max):
    if check_winner(board, 'O'): return 1
    if check_winner(board, 'X'): return -1
    if is_draw(board): return 0

    if is_max:
        best = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                val = pure_minimax(board, depth + 1, False)
                board[i] = ' '
                best = max(best, val)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                val = pure_minimax(board, depth + 1, True)
                board[i] = ' '
                best = min(best, val)
        return best

def best_move_pure(board):
    best_val = -float('inf')
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_val = pure_minimax(board, 0, False)
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move
