# Tic-Tac-Toe vs AI

Human vs AI Tic-Tac-Toe with adjustable difficulty and board size. Built as Day 17 of #30Days30Projects.

Backend and frontend are split: Flask handles all game logic (win detection, AI move selection), the HTML/JS frontend just renders the board and sends clicks.

## Features
- **Board sizes:** 3×3, 4×4, 5×5 (win length scales with board size)
- **Difficulty levels:** Easy, Medium, Hard — the AI mixes in random moves at lower difficulties so it's actually beatable
- **AI:** minimax with alpha-beta pruning (full search on 3×3, depth-limited + heuristic evaluation on larger boards)

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000`.

## Project structure

```
tictactoe_app/
├── app.py              # Flask backend — all game logic + AI
├── requirements.txt
└── templates/
    └── index.html       # frontend — rendering + click handling only
```

## How the AI works

- **Hard:** near-optimal play (full minimax on 3×3; alpha-beta pruning with a depth cap on 4×4/5×5, since full search isn't feasible past 3×3)
- **Medium:** plays well but takes a random move ~25% of the time
- **Easy:** mostly random, blocks/wins are frequently missed — good for a quick win

## Next ideas
- Two-player (human vs human) mode
- Persistent scoreboard across sessions
- Deploy the Flask app somewhere it can actually run (Render, Railway, etc.) and embed it in my portfolio next to Snake
