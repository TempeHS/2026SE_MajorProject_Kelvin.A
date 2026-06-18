# 2026SE Major Project — Turn-Based Samurai Combat

A turn-based RPG combat prototype built with Python and pygame-ce, inspired by Final Fantasy-style battles. The player controls a samurai facing two enemies (Gintoki and Sakata) and can attack, defend, or drink potions on their turn, with randomised attack animations, damage/heal floating text, a turn indicator, and match results (win/loss and remaining HP) logged to a SQLite database for future balancing.

## Status

- **Current sprint:** Sprint 8 (final sprint of the project)

- **Last increment:** Refactored the single-file prototype into separate modules (`core/`, `entities/`, `scripts/`, `utilities/`) for rendering, game state, collision/input, spawning, and resource loading, while preserving existing gameplay behaviour (PB-14, PB-15).

- **Next planned increment:** No further sprints are scheduled — Sprint 8 was marked as the last. Remaining work is bug-fix only, tracked in `BUG_TRACKER.md`: cursor visibility not reliably hiding over VNC (BUG-002) and residual katana cursor lag over VNC (BUG-005).

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
