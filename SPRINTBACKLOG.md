# Sprint Backlog

---

## Sprint 1

**Sprint Goal:** Implement core combat loop — player and enemy can attack, health bars display correctly.

### Committed Items
| PB ID | User Story |
|-------|------------|
| PB-01 | As a player, I want to see my character idle so the game feels alive |
| PB-02 | As a player, I want to attack enemies so I can win the battle |
| PB-03 | As a player, I want to see health bars so I know remaining HP |

### Sprint Plan
1. Load and animate Idle sprites for Samurai and Enemy
2. Implement `Fighter.attack()` with randomised damage
3. Implement turn-based `current_fighter` loop
4. Implement `HealthBar.draw()` with green/red ratio bars
5. Load panel and background assets; render HUD text

### Unit Test Summary

| Test ID | Description | Expected Result | Pass/Fail |
|---------|-------------|-----------------|-----------|
| T-01 | Fighter takes damage | `hp` decreases by `strength ± 5` | Pass |
| T-02 | Health bar renders green segment | Green rect width = `200 * (hp/max_hp)` | Pass |
| T-03 | Idle animation loops | `frame_index` resets to 0 at end of list | Pass |

### Sprint Review
What was completed, what was not, and any scope changes. Reference PB IDs.

### Sprint Retrospective
- **What went well:**
- **What didn't go well:**
- **What to improve next sprint:**

---

## Sprint 2

...