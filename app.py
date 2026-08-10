import math
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

EMPTY = None
HUMAN = "X"
AI = "O"

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def winner(board):
    for a, b, c in LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return all(cell is not None for cell in board)


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell is None]


def minimax(board, is_maximizing):
    win = winner(board)
    if win == AI:
        return 1
    if win == HUMAN:
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for move in available_moves(board):
            board[move] = AI
            best = max(best, minimax(board, False))
            board[move] = EMPTY
        return best
    else:
        best = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            best = min(best, minimax(board, True))
            board[move] = EMPTY
        return best


def best_ai_move(board):
    best_score = -math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/move", methods=["POST"])
def api_move():
    """
    Expects JSON: { "board": [9 values, each "X" | "O" | null] }
    Returns JSON: {
        "move": <index the AI played, or null if no move made>,
        "board": <updated 9-cell board after the AI's move>,
        "winner": "X" | "O" | null,
        "is_draw": true | false
    }
    """
    data = request.get_json(force=True) or {}
    board = data.get("board")

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "board must be a list of 9 cells"}), 400
    if any(cell not in (None, HUMAN, AI) for cell in board):
        return jsonify({"error": "invalid cell value in board"}), 400

    # If the game is already decided, don't move.
    win = winner(board)
    if win or is_full(board):
        return jsonify({
            "move": None,
            "board": board,
            "winner": win,
            "is_draw": win is None and is_full(board),
        })

    move = best_ai_move(board)
    board[move] = AI

    win = winner(board)
    return jsonify({
        "move": move,
        "board": board,
        "winner": win,
        "is_draw": win is None and is_full(board),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
