# Sprint Backlog

---

## Sprint 1

**Sprint Goal:** Implement core stats, health bars display correctly.

### Committed Items

| PB ID | User Story                        |
| ----- | --------------------------------- |
| PB-01 | I want to add idle animations     |
| PB-02 | Health bars should work correctly |

### Sprint Plan

1. Load and animate Idle sprites for Samurai and Enemy
2. Implement `HealthBar.draw()` with green/red ratio bars
3. Load panel and background assets; render HUD text

### Unit Test Summary

| Test ID | Description                      | Expected Result                          | Pass/Fail |
| ------- | -------------------------------- | ---------------------------------------- | --------- |
| T-01    | Health bar renders green segment | Green rect width = `200 * (hp/max_hp)`   | Pass      |
| T-02    | Idle animation loops             | `frame_index` resets to 0 at end of list | Pass      |

### Sprint Review

PB-01 was a success and idle animations were implemented, attack animations were also added to test action logic aswell.
PB-02 Works correctly as it should, but logic it currently untested as there is no attack function yet

### Sprint Retrospective

- **What went well:**Idle animations are simple repeating loops, health bar is a coloured rectangle with scalable values
- **What didn't go well:**Couldn't test health bar reactivity due to missing logic
- **What to improve next sprint:**Implement Attack logic

---

## Sprint 2

...
