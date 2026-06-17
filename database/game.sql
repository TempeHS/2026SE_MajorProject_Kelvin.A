CREATE TABLE match_results (
id INTEGER PRIMARY KEY AUTOINCREMENT,
played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
outcome TEXT NOT NULL CHECK (outcome IN ('WIN', 'LOSS')),
player_hp INTEGER NOT NULL CHECK (player_hp >= 0),
gintoki_hp INTEGER NOT NULL CHECK (gintoki_hp >= 0),
sakata_hp INTEGER NOT NULL CHECK (sakata_hp >= 0)
);
