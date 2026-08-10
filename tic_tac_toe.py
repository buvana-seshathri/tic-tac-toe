"""
Tic-Tac-Toe vs AI

RUN:
    python tic_tac_toe.py

You play as X, the AI plays as O. Enter a number 1-9 to place your mark:

     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9

"""

import math

EMPTY = " "
HUMAN = "X"
AI = "O"


def print_board(board):
    print()
    for row in range(3):
        cells = [board[row * 3 + i] or str(row * 3 + i + 1) for i in range(3)]
        print(f"  {cells[0]} | {cells[1]} | {cells[2]}")
        if row < 2:
            print(" -----------")
    print()


def winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]
    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return all(cell != EMPTY for cell in board)


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def minimax(board, is_maximizing):
    """Returns the best score for the current board state.
    AI (maximizing) wants +1, human (minimizing) wants -1, draw is 0."""
    win = winner(board)
    if win == AI:
        return 1
    if win == HUMAN:
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = AI
            score = minimax(board, False)
            board[move] = EMPTY
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            score = minimax(board, True)
            board[move] = EMPTY
            best_score = min(best_score, score)
        return best_score


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


def get_human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= 9):
            print("Enter a number from 1 to 9.")
            continue
        idx = int(raw) - 1
        if board[idx] != EMPTY:
            print("That spot's taken — pick another.")
            continue
        return idx


def play_round():
    board = [EMPTY] * 9
    print_board(board)

    while True:
        # Human turn
        move = get_human_move(board)
        board[move] = HUMAN
        print_board(board)

        win = winner(board)
        if win:
            print(f"{win} wins!" if win == HUMAN else "AI wins!")
            return
        if is_full(board):
            print("It's a draw!")
            return

        # AI turn
        print("AI is thinking...")
        ai_move = best_ai_move(board)
        board[ai_move] = AI
        print_board(board)

        win = winner(board)
        if win:
            print(f"{win} wins!" if win == HUMAN else "AI wins!")
            return
        if is_full(board):
            print("It's a draw!")
            return


def main():
    print("=" * 30)
    print("   TIC-TAC-TOE vs AI")
    print("   You are X. AI is O.")
    print("   The AI plays optimally — good luck getting more than a draw!")
    print("=" * 30)

    while True:
        play_round()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
