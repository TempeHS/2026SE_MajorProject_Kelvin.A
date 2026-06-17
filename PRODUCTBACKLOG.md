# Product Backlog

## Vision

The combat of a game which is alike a RPG game, inspired by final fantasy turn-based combat. The game is for anyone to play as it should be accessible to everyone, this game delivers values in strategic thinking, and management

---

## Backlog

| ID    | User Story                                                                                               | Priority | Acceptance Criteria                                                                                    | Status |
| ----- | -------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------ | ------ |
| PB-01 | I want to add idle animations                                                                            | Medium   | Idle animation loops continuously on startup                                                           | Done   |
| PB-02 | Health bars should work correctly                                                                        | High     | Green/red bar scales with current HP ratio                                                             | Done   |
| PB-03 | Health bars should react accurately to damage being dealt                                                | High     | Damage is correctly calculated from health, and health bar responds by showing the remainder of health | Done   |
| PB-04 | When Attacking an enemy or an enemy attacking, attack animations should play randomly from the 3 options | Low      | When attacking a random animation should play instead of one                                           | Done   |
| PB-05 | Attacking an enemy is based on the cursor (click to attack an enemy)                                     | Medium   | Clicking an enemy attacks on players turn                                                              | Done   |
| PB-06 | I want to ensure attacking works                                                                         | High     | Whole attacking system works                                                                           | Done   |
| PB‑07 | I want damage and healing text to appear when actions occur                                              | Medium   | DamageText class exists, floats upward, deletes after lifespan, and triggers on damage/heal events     | Done   |
| PB-08 | I want to add aniamtions for being attacked, and dying                                                   | Low      | Animations should play after the corresponding action                                                  | Done   |
| PB-09 | When the player dies the game should end                                                                 | High     | When the player dies, the game should show black and a message on screem                               | Done   |
| PB-10 | The player and enemies should be able to defend                                                          | Done     |
| PB-11 | The amount a player defends from should vary and be fair                                                 | Done     |

---

## Changelog

| Date       | Change                        | Reason                                                   |
| ---------- | ----------------------------- | -------------------------------------------------------- |
| 03=06=2026 | Added PB-01                   | Initial backlog from Phase 1 requirements                |
| 03-06-2026 | Raised PB-02 to High priority | Core combat mechanic needed in Sprint 1                  |
| 10-06-2026 | Add PB-03                     | Core mechanic for health                                 |
| 10-06-2026 | Add PB-04                     | Quality of life feature                                  |
| 10-06-2026 | Add PB-05                     | Core mechanic for attacking                              |
| 10-06-2026 | Add PB-06                     | Core to ensure whole system works as a whole             |
| 16-06-2026 | Add PB-07                     | Visual combat feedback                                   |
| 16-06-2026 | Add PB-08                     | Hurt/Death Animations and code                           |
| 16-06-2026 | Add PB-09                     | Game Over screen implemented                             |
| 17-06-2026 | Add PB-10                     | Defence options implemented                              |
| 17-06-2026 | Add PB-11                     | Defence reduction is randomised with a chance to counter |
