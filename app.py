import math
import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

EMPTY = None
HUMAN = "X"
AI = "O"

WIN_LENGTH = {3: 3, 4: 4, 5: 4}

SEARCH_DEPTH = {3: 9, 4: 4, 5: 3}

DIFFICULTY_RANDOMNESS = {"easy": 0.65, "medium": 0.25, "hard": 0.0}

_lines_cache = {}

def all_lines(size, win_len):
    key = (size, win_len)
    if key in _lines_cache:
        return _lines_cache[key]

    def idx(r, c):
        return r * size + c

    lines = []

    # Horizontal and vertical runs
    for r in range(size):
        for c in range(size - win_len + 1):
            lines.append(tuple(idx(r, c + k) for k in range(win_len)))
    for c in range(size):
        for r in range(size - win_len + 1):
            lines.append(tuple(idx(r + k, c) for k in range(win_len)))

    # Diagonal runs (both directions)
    for r in range(size - win_len + 1):
        for c in range(size - win_len + 1):
            lines.append(tuple(idx(r + k, c + k) for k in range(win_len)))
            lines.append(tuple(idx(r + k, c + win_len - 1 - k) for k in range(win_len)))

    _lines_cache[key] = lines
    return lines


def winning_line(board, size, win_len):
    for line in all_lines(size, win_len):
        first = board[line[0]]
        if first is not None and all(board[i] == first for i in line):
            return line
    return None


def winner(board, size, win_len):
    line = winning_line(board, size, win_len)
    return board[line[0]] if line else None


def is_full(board):
    return all(cell is not None for cell in board)


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell is None]


def evaluate(board, size, win_len):
    score = 0
    for line in all_lines(size, win_len):
        cells = [board[i] for i in line]
        has_human = HUMAN in cells
        has_ai = AI in cells
        if has_human and has_ai:
            continue  # dead line, no one can complete it
        ai_count = cells.count(AI)
        human_count = cells.count(HUMAN)
        if ai_count:
            score += 10 ** ai_count
        elif human_count:
            score -= 10 ** human_count
    return score


def alphabeta(board, size, win_len, depth, alpha, beta, maximizing):
    win = winner(board, size, win_len)
    if win == AI:
        return 100_000 + depth
    if win == HUMAN:
        return -100_000 - depth
    if is_full(board) or depth == 0:
        return evaluate(board, size, win_len)

    if maximizing:
        value = -math.inf
        for move in available_moves(board):
            board[move] = AI
            value = max(value, alphabeta(board, size, win_len, depth - 1, alpha, beta, False))
            board[move] = EMPTY
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            value = min(value, alphabeta(board, size, win_len, depth - 1, alpha, beta, True))
            board[move] = EMPTY
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def best_search_move(board, size, win_len, depth):
    moves = available_moves(board)
    random.shuffle(moves)  # avoid deterministic bias among equally-good moves
    best_score = -math.inf
    best_move = moves[0]
    for move in moves:
        board[move] = AI
        score = alphabeta(board, size, win_len, depth - 1, -math.inf, math.inf, False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def choose_ai_move(board, size, difficulty):
    win_len = WIN_LENGTH[size]
    depth = SEARCH_DEPTH[size]
    moves = available_moves(board)

    rand_chance = DIFFICULTY_RANDOMNESS.get(difficulty, 0.0)
    if random.random() < rand_chance:
        return random.choice(moves)

    return best_search_move(board, size, win_len, depth)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json(force=True) or {}
    board = data.get("board")
    size = data.get("size", 3)
    difficulty = data.get("difficulty", "hard")

    if size not in WIN_LENGTH:
        return jsonify({"error": "size must be 3, 4, or 5"}), 400
    if difficulty not in DIFFICULTY_RANDOMNESS:
        return jsonify({"error": "difficulty must be easy, medium, or hard"}), 400
    if not isinstance(board, list) or len(board) != size * size:
        return jsonify({"error": f"board must be a list of {size * size} cells"}), 400
    if any(cell not in (None, HUMAN, AI) for cell in board):
        return jsonify({"error": "invalid cell value in board"}), 400

    win_len = WIN_LENGTH[size]

    win = winner(board, size, win_len)
    if win or is_full(board):
        return jsonify({
            "move": None,
            "board": board,
            "winner": win,
            "is_draw": win is None and is_full(board),
            "line": list(winning_line(board, size, win_len)) if win else None,
        })

    move = choose_ai_move(board, size, difficulty)
    board[move] = AI

    win = winner(board, size, win_len)
    return jsonify({
        "move": move,
        "board": board,
        "winner": win,
        "is_draw": win is None and is_full(board),
        "line": list(winning_line(board, size, win_len)) if win else None,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
