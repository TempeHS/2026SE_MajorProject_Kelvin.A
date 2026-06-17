import sqlite3

DB = "/workspaces/2026SE_MajorProject_Kelvin.A/database/game.db"


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS match_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        outcome TEXT NOT NULL CHECK (outcome IN ('WIN', 'LOSS')),
        player_hp INTEGER NOT NULL CHECK (player_hp >= 0),
        gintoki_hp INTEGER NOT NULL CHECK (gintoki_hp >= 0),
        sakata_hp INTEGER NOT NULL CHECK (sakata_hp >= 0)
        );
        """)
    conn.commit()


def save_match_result(outcome, player_hp, gintoki_hp, sakata_hp):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            """
        INSERT INTO match_results (outcome, player_hp, gintoki_hp, sakata_hp)
        VALUES (?, ?, ?, ?)
        """,
            (outcome, max(0, player_hp), max(0, gintoki_hp), max(0, sakata_hp)),
        )
    conn.commit()
