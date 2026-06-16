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

**Sprint Goal:** Implement Attack logic, ensure healthbars are reactive, ensure attack animations play, Attack animations should be random, Make attacking based on cursor input

### Committed Items

| PB ID | User Story                                                                                               |
| ----- | -------------------------------------------------------------------------------------------------------- |
| PB-01 | I want to ensure attacking works                                                                         |
| PB-02 | Health bars should react accurately to damage being dealt                                                |
| PB-03 | When Attacking an enemy or an enemy attacking, attack animations should play randomly from the 3 options |
| PB-04 | Attacking an enemy is based on the cursor (click to attack an enemy)                                     |

### Sprint Plan

1. Setup Attacking logic
2. Implement code to show attacking
3. Implement timers, and logic to ensure attacks are turn-based (Look for player action, then enumerate each enemy in Enemy_list)
4. Ensure attacks are using Random attacks from `pick_attack()`
5. Default cursor disappears when hovering an enemy and a katana appears (Default cursor cannt vanish due to VNC settings, but from the code it should work)
6. when a enemy it dead their turn should skip to the next fighter

### Unit Test Summary

| Test ID | Description                                                               | Expected Result                            | Pass/Fail |
| ------- | ------------------------------------------------------------------------- | ------------------------------------------ | --------- |
| T‑03    | Attack animation when Samurai attacks, animation switches to Attack .     | `action == 1` and `frame_index == 0`       | Pass      |
| T‑04    | Random attack variant `Pick_attack()` selects a random `Attack_*` folder. | Different variant in each attack           | Pass      |
| T‑05    | Attacking reduces target HP by `strength + rand`.                         | Target HP decreases correctly              | Pass      |
| T‑06    | When HP < 1, fighter is dead.                                             | `alive == False` and `HP = 0`              | Pass      |
| T‑07    | Turn order cycles: `Samurai` → `Enemy1` → `Enemy2` → repeat.              | `current_fighter` loops 1→3→1              | Pass      |
| T‑10    | Default cursor hides and katana appears when hovering enemy.              | Cursor hidden + katana drawn               | Fail      |
| T‑13    | Enemy idle/attack animations loop correctly.                              | Frame resets at end                        | Pass      |
| T‑14    | Clicking enemy sets `attack = True` and selects `target`.                 | Attack set + target assigned               | Pass      |
| T‑15    | Dead enemies should not attack.                                           | Dead enemy skips their turn without action | Pass      |

### Sprint Review

PB-01 Attacking logic does work, although when collision in detected with an enemy the cursor should dissapear but it stays due to VNC limitations, katana does appear, and turns are iterative.
PB-02 Health bars react correctly in scale and HP to damage being dealt (Fixed problem with negative damage healing target)
PB-03 Attacks randomly iterate through random variants through `pick_attack()`
PB-04 Cursor collision works through pygame library, clicking is also done through collision and left click.

### Sprint Retrospective

- **What went well:** Attack logic is simple, and eveything is working currently
- **What didn't go well:** Due to NoVNC settings, the game may take longer to update actions, or react to inputs, the cursor cannot be hidden
- **What to improve next sprint:** Add potions into the game

---

## Sprint 3

**Sprint Goal:** Add in potions feature, player and enemies should have potions

### Committed Items

| PB ID | User Story                                  |
| ----- | ------------------------------------------- |
| PB-01 | Potions would make the game better          |
| PB-02 | Enemies shoud also have the ability to heal |
| PB-03 | Damage done should also be visualised       |

### Sprint Plan

1. Import potion sprite and button library
2. Create a button with the potion sprite
3. Implement the health boost feature into when clicking the button
4. Set up function to display damage text

### Unit Test Summary

| Test ID | Description                      | Expected Result                          | Pass/Fail |
| ------- | -------------------------------- | ---------------------------------------- | --------- |
| T-01    | Health bar renders green segment | Green rect width = `200 * (hp/max_hp)`   | Pass      |
| T-02    | Idle animation loops             | `frame_index` resets to 0 at end of list | Pass      |

### Sprint Review

PB-01 was a success and idle animations were implemented, attack animations were also added to test action logic aswell.
PB-02 Works correctly as it should, but logic it currently untested as there is no attack function yet

### Sprint Retrospective

- **What went well:** Idle animations are simple repeating loops, health bar is a coloured rectangle with scalable values
- **What didn't go well:** Couldn't test health bar reactivity due to missing logic
- **What to improve next sprint:** Implement Attack logic

## Sprint 4

**Sprint Goal:** Add in a class that allows for damage/heal text to appear when those actions are called

### Committed Items

| PB ID | User Story                        |
| ----- | --------------------------------- |
| PB-01 | I've gotta add damage trext       |
| PB-02 | I've also got to add healing text |

### Sprint Plan

1. Crete a DamageText class
2. Define its parameters
3. Implement into actions

### Unit Test Summary

| Test ID | Description                                          | Expected Result                               | Pass/Fail |
| ------- | ---------------------------------------------------- | --------------------------------------------- | --------- |
| T-01    | Instantiate `DamageText object with valid parameters | Correct `rect.center`, `counter = 0`          | Pass      |
| T-02    | Verify upwards movement                              | After `update()`, `rect.y` decreases by 1     | Pass      |
| T-03    | Verify counter increment                             | Each `update()` increases `counter` by 1      | Pass      |
| T-04    | Delete after lifespan                                | after `update()` is called 31 times `.kill()` | Pass      |
| T-05    | Render is correct                                    | `image` is a valid `Surface`                  | Pass      |
| T-06    | Group behaviour                                      | Calling `group.update()` updates position     | Pass      |
| T-07    | DamageText                                           | Only one text per `action`                    | Pass      |

### Sprint Review

PB-01 Fully implemented text into combat loop. Damage numbers appear. Behaviour matches
PB-02 Healing text follows the same logic. Colour is different. Healing is implemented although combat logic is still incomplete.

### Sprint Retrospective

- **What went well:** `DamageText` shows damage correctly, healing is also visualised
- **What didn't go well:** Enemy behaviour is still basic, linear
- **What to improve next sprint:** Add animations for other states, begin planning defence options

## Sprint 5

**Sprint Goal:** Implement core stats, health bars display correctly.

### Committed Items

| PB ID | User Story                                             |
| ----- | ------------------------------------------------------ |
| PB-01 | I want to add aniamtions for being attacked, and dying |
| PB-02 | When the player dies the game should end               |

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
