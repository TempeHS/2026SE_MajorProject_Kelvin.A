# 2026SE Major Project — Turn-Based Samurai Combat

A turn-based RPG combat prototype built with Python and pygame-ce, inspired by Final Fantasy-style battles. The player controls a samurai facing two enemies (Gintoki and Sakata) and can attack, defend, or drink potions on their turn, with randomised attack animations, damage/heal floating text, a turn indicator, and match results (win/loss and remaining HP) logged to a SQLite database for future balancing.

## Status

- **Current sprint:** Sprint 1 

- **Last increment:** Skeleton structure

- **Next planned increment:** Create the attack logic for the game

## How to Run

This project is set up to run inside the provided Dev Container (`.devcontainer/devcontainer.json`), which installs Xvfb, x11vnc, noVNC, and the Python virtual environment automatically via `postCreateCommand`.

1. Open the project (wait for postCreateCommand to finish).

2. Run the game inside a `bash` terminal with:

```
bash start.sh
```

3. Wait for port 6080 to come up, then open it from VS Code's Ports tab to view the game in your browser via noVNC.


> [!NOTE]
> `start.sh` creates the virtual environment and installs `requirements.txt` automatically if needed, so no manual `pip install` step is required.

## Project Planning

- Product Backlog — user stories, priorities, and acceptance criteria
- Sprint Backlog — sprint goals, plans, test summaries, and retrospectives
