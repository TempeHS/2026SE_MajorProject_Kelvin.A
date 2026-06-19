# Developer Documentation — 2026SE Major Project
---

## Decision Log (for Arcadia 1970)

| # | Decision | Context / Trade-off | Sprint |
| --- | --- | --- | --- |
| 1 | Use `pygame-ce` instead of `pygame` | Community edition is actively maintained and SDL2-based; no functional downside found for this project's needs. | 1 |
| 2 | Force `SDL_RENDER_DRIVER=software` | The dev container has no real GPU/display, only Xvfb. | 8 |
| 3 | Run the game inside Xvfb + x11vnc + noVNC rather than a native window | Required because the container has no physical display; Trade-off is added input/render latency over the network, which directly caused the cursor lag and visibility issues (BUG-002, BUG-005). | 1–2 |
| 4 | Model turn order as a single increasing integer (`current_fighter`) rather than a state machine | Simple combat; Won't scale correctly if `Fighter` becomes dynamic. | 2 |
| 5 | Draw a custom cursor (katana/shield) instead of relying on `pygame.mouse.set_visible()` | The OS cursor can't be hidden over VNC, so a software-drawn cursor was needed for interaction; trade-off is the custom cursor reintroduces a frame of lag the real OS cursor wouldn't have. | 2 |
| 6 | Inject shared render state (`screen`, `font`, colours) into `entities/player.py` via `configure_player_module()` module-level globals, rather than passing them into every `Fighter` | Keeps the `Fighter` class short; trade-off is hidden coupling — `configure_player_module()` must run before any `Fighter` method. | 8 |
| 7 | Match results to SQLite (`database/game.sql`, `core/game.py`) instead of a flat log file | Enables queries for future balancing; trade-off is an added schema/dependency for a single table. | 7 |
| 8 | Split the single `main.py` prototype into `core/`, `entities/`, `scripts/`, `utilities/` modules | Improves readability and makes individual pieces (collision, rendering, persistence) easier to test in isolation; trade-off was a real risk of breaking indentation/control-flow during the move. | 8 |

---

## Sprint Documentation

### Sprint 1 — Core stats and health bars
 
**Goal:** Idle animations load and loop. Health bars display correctly.
 
**Outcome vs plan:** Idle animations were implemented, and attack animations were also added early to test action logic. Health bars render correctly, but reactivity to damage couldn't be verified yet since attack logic didn't exist.
 
**Key commits**
- [create animation code for idle](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/f6818905baef977debc7548bb118fe1d323f1afe) — Add idle animation loading and Fighter sprite scaling
- [feature:Player and enemy hp and bar](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/d82b143f8a6226a08f855bba093d339078e47619) — Implement HealthBar with green/red rectangles
- [wip: create funcion to draw text](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/6821217e6d680c332e4ccb8059c51d08d67cc237) — Fix BUG-001 — remove unmatched paren in enemy stats draw_text call

**Client feedback**
> "The game's base layout is good, but I don't know how much damage is being done, also there's no attack logic yet"

**Response:** Implemented attacking logic into Sprint 2, health bars also react to damage done
 
**Difficulties encountered**

- **BUG-001 (High):** Adding the enemy stats drawing block introduced an unmatched closing parenthesis in a `draw_text` call inside `draw_panel`, causing a syntax error and a black screen on startup. Fixed by removing the stray parenthesis.
- Health bar reactivity to damage was untested, since attack logic hadn't been built yet. Carried forward explicitly as a gap rather than a bug.

**Screenshots**

<img width="1686" height="522" alt="image" src="https://github.com/user-attachments/assets/4db42831-1831-4236-b210-df708e630db5" />


<img width="1904" height="346" alt="image" src="https://github.com/user-attachments/assets/a46e499a-dd27-432f-8984-110673218298" />


**Next sprint plan**
Implement attack logic so health bars can be verified against damage, make attacking based on the cursor.
 
---
 
### Sprint 2 — Attack logic, reactive health bars, cursor-based targeting
 
**Goal:** Working attack system; health bars react to damage; random attack animations; cursor inputs attack; dead enemies skip their turn.
 
**Outcome vs plan:** Attacking works and turn order is correctly iterative; random attack variants play through `pick_attack()`; clicking an enemy sets `attack=True`; dead fighters are skipped. The one problem: the OS cursor can't be hidden over NoVNC, so the katana cursor sometimes shows alongside the default arrow.
 
**Key commits**
- [wip: working on attack logic](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/7a52361f50e9d240c1edbe66d431b53caa0dcb7a) — Implement player_action/hovering_enemy collision detection
- [feature: Attack function on enemy pressed, wip: add clarification to function](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/d064c75ec239665b86548e5c9b499b6638346ea2) — Add Fighter.attack/guard_damage and turn-order increment
- [wip: Working on attack logic](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/5960faaa59d51a6f15ba5ce93e668142475c36d2) — Fix BUG-003 — restore loop indentation

**Client feedback**
"Every RPG game basically features a way to heal, I think that would be a good feature to add"

**Response:** Added potion system in Sprint 3 for both players and enemies
 
**Difficulties encountered**
- **BUG-002 (Medium, In Progress):** OS cursor sometimes still shows due to VNC overlay delays. Frame‑by‑frame hiding helps but doesn’t fully fix it.
- **BUG-003 (High):** Bad indentation put the whole frame loop inside a conditional, causing a blank screen.
- **BUG-004 (High):** Katana draw call was inside the hover‑detection loop and skipped after `break`.
- **BUG-005 (Medium, In Progress):** Katana cursor lags due to software rendering + VNC latency. End‑of‑frame draw helps but delay is unavoidable.
- **BUG-006 (Low):**Katana was offset because the anchor point was wrong. Fixed with hotspot-based positioning anchored near the blade tip.

**Screenshots**

- [ ] <img width="230" height="257" alt="image" src="https://github.com/user-attachments/assets/58814fbb-2374-4320-9ec9-17aff9108937" />

- [ ] <img width="354" height="87" alt="image" src="https://github.com/user-attachments/assets/20d810c0-280a-42c4-9373-423336c96170" />

*Next sprint plan**
Add a potion feature for the player and enemies, and visualise damage/healing on screen.
 
---
 
### Sprint 3 — Potions
 
**Goal:** Player and enemies can use potions to heal. Damage should also be visualised.
 
**Outcome vs plan:** A potion button was added. Damage visualisation was deferred and became the explicit goal of Sprint 4.
 
**Key commits**
- [feature: add button class for potion collision, and click detection](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/958d210eb9e9491322987940718ffb43cd45dfc4) — Add potion button 
- [feature: add potion button, enemy logic](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/8a7faf53e62fcfe3186bbe3d901dcdda11e2cb6a) — Add enemy low-HP potion behaviour

**Client feedback**
> "Healing feature is good, but I want to visualise how much damage is being done"

**Response:** Built DamageText class in Sprint 4
 
**Difficulties encountered**
- Potions had difficulty scaling fairness with amount and quantity: set a fixed num

**Screenshots**

 <img width="247" height="195" alt="image" src="https://github.com/user-attachments/assets/120dd1b1-4aea-4a3e-8af7-686a40937aa3" />

 <img width="390" height="276" alt="image" src="https://github.com/user-attachments/assets/758f583f-8838-4ac7-9a81-e95cc5d7be7d" />

 <img width="427" height="274" alt="image" src="https://github.com/user-attachments/assets/473f5683-b241-4397-aa27-4064557ac11f" />

**Next sprint plan**
Add a `DamageText` class so damage and healing are visible on screen.
 
---
 
### Sprint 4 — Damage/heal floating text
 
**Goal:** A `DamageText` class shows damage and healing numbers when those actions occur.
 
**Outcome vs plan:** Fully delivered.
 
**Key commits**
- [Feature: class to show damagfe dealt visaually](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/c7413f3292e989a2692b81932b7e4f0bf89884da) — Add DamageText sprite class with upward float + lifespan

**Client feedback**
> "The combat is more responsive now. But the lack of animations makes the combat a bit bland"

*Response:** Added hurt and death animations in Sprint 5 + an additional death screen
 
**Difficulties encountered**
- enemy behaviour was still fairly basic and linear (low-HP-then-potion, otherwise attack)

**Screenshots**

 <img width="183" height="277" alt="image" src="https://github.com/user-attachments/assets/25affe28-3c86-4312-820c-e0d988775fa5" />

 <img width="285" height="358" alt="image" src="https://github.com/user-attachments/assets/dd7e9158-5194-4347-a935-4cc69350e324" />

**Next sprint plan**
Add hurt and death animations, and begin planning defence options for the sprint after.
 
---
 
### Sprint 5 — Hurt/death animations and game over
 
**Goal:** Add animations for being attacked and dying; end the game when the player dies.
 
**Outcome vs plan:** Both delivered. Hurt and death animations are integrated into the combat loop, and a game-over overlay correctly appears when the player dies.
 
**Key commits**
- [feature: add hurt animation](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/fbf5c9c5ac8a1c2ff06a6693df28724ee9520450) — Add Hurt/Death animation loading *(related commits: [death animation method](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/926f929a133d86cc468bf5c0ab8ac2e2d306414e), [add death logic](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/49d1c70e61accde4030163ddd0c03bb9eec7d9d0))*
- [feature: when samurai dies play 'gameover'](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/c6bdbcdc258fb4e630ac84364b8bd41ea1a79584) — Add game_over state + draw_game_over_overlay branch in main loop

**Client feedback**
> "Its good, but there should be a system to defend from the enemies"

**Response:** Added a defence action in Sprint 6 for player and enemies
 
**Difficulties encountered**
- early testing of the combat loop was limited, since hurt/death/game-over all needed to be exercised together to confirm they didn't conflict with existing attack/potion states.

**Screenshots**

 <img width="216" height="272" alt="image" src="https://github.com/user-attachments/assets/6dc852c2-e4ca-4dce-a4fc-461c8a977566" />

 <img width="1062" height="530" alt="image" src="https://github.com/user-attachments/assets/da003ec8-1985-4e7a-b720-eaa172462b66" />

**Next sprint plan**
Add a defend action (a "run" action was considered and dropped as not worth implementing (future vision)); revisit sound effects later.
 
---
 
### Sprint 6 — Defence
 
**Goal:** Player and enemies can defend. The amount blocked should vary and be fair.
 
**Outcome vs plan:** Fully delivered. Defending is integrated into the combat system for both sides, with random partial-block, full-block, and counter-attack outcomes.
 
**Key commits**
- [feature: implement blocking state using same logic as attacking](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/4a307280134c4017ddb91ca804f8201d26dd37bd) — Add mode toggle button + Fighter.defend() state
- [feature: create defending state, and comput damage after blocking](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/432c9166ab534643978a0beba2ba8a7554312594) — Add guard_damage() with block/partial-block/counter rolls

**Client feedback**
> "Tracking whose turn it is that makes the game confusing "

**Response:** Added visible indicator and text in Sprint 7 + add an database feature to log final combat moments
 
**Difficulties encountered**
- turn-clarity issue: both client and internal testing flagged it, reinforcing it as the priority for Sprint 7.

**Screenshots**

 <img width="661" height="371" alt="image" src="https://github.com/user-attachments/assets/ba8c9277-4b27-48cf-a18f-6fad494fc0a3" />

 <img width="230" height="329" alt="image" src="https://github.com/user-attachments/assets/0775a955-e1b9-4e9e-b84f-70c3e2e10222" />

**Next sprint plan**
Implement a turn indicator, and add a database to log match results (including whether the Samurai died) for future difficulty balancing.
 
---
 
### Sprint 7 — Turn indicator and match database
 
**Goal:** Make turns visible to the player; track match statistics for future balancing.
 
**Outcome vs plan:** Both delivered. A turn indicator shows whose turn it is and skips dead fighters, and `save_match_result()` writes outcome to SQLite via `core/game.py`.
 
**Key commits**
- [refactor: enemy names, wip: add indicator text and arrows](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/b81b9dc9068e0e126aef060898a2522967daee3b) — Add turn indicator (text + arrow) to scene_manager
- [feature: database captures final moments, wip: init database](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/86bc48e9690ef2b85e9d20a540acccfd9081935a) — Add match_results table + save_match_result on game over

**Client feedback**
> "The code looks good, and the gameplay is good enough"

**Response:**refactored the code structure in Sprint 8 on my own basis
 
**Difficulties encountered**
- two originally-intended features were dropped from scope rather than carried forward as bugs: a wave-based enemy structure, and sound effects.

**Screenshots**
 <img width="1872" height="689" alt="image" src="https://github.com/user-attachments/assets/44b3f76a-fd98-4f68-9a44-69bbcb6a7026" />

 <img width="1893" height="710" alt="image" src="https://github.com/user-attachments/assets/6e5b4c6e-01ed-469b-8768-818d654d8cb6" />

 <img width="918" height="248" alt="image" src="https://github.com/user-attachments/assets/22923048-8790-46b2-90c1-498780477b3e" />

**Next sprint plan**
Refactor the codebase into clearer, separate modules: my own retrospective as the priority before wrapping up.
 
---
 
### Sprint 8 — Refactor into modules (final sprint)
 
**Goal:** Split the project into its own respective modules while preserving existing behaviour.
 
**Outcome vs plan:** Both committed items delivered — the original single-file prototype is now organised into `core/` (settings, scene rendering, database), `entities/` (player and enemy logic), `scripts/` (collision, spawning), and `utilities/` (buttons, resource loading, timer).
 
**Key commits**
- [refactor: draw methods into scene_manager](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/70f863100b81d004deb68b745b2e71bd631c7f66) — Extract core/scene_manager.py from main.py rendering code
- [Refactor: fighter class into enemy and player. debug: conn.commity() indentation](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/04a842e8e8596c245d5c6db542a47f9c09685cf5) — Extract entities/player.py and entities/enemy.py
- [refactor: mouse hovering logic into collision](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/28e2b1cffdb83dd3668dc1ec828bf64f6af5c71e) — Extract scripts/collision.py and scripts/spawner.py *(companion commit: [refactor: move buttons into spawner](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/ad1c773cd21d310cb0efb35a417b903570f73ee5))*
- [refactor: load images successfully refactored](https://github.com/TempeHS/2026SE_MajorProject_Kelvin.A/commit/3538ad19d03d4afd8c79b35fb95212531b28fc07) — Extract utilities/resource_loader.py; final main.py cleanup

**Client feedback**
> "I don't get what you did, but at least it still works"

**Response:** 	Final development sprint
 
**Difficulties encountered**
- Per the retrospective: integrating the new module structure introduced a number of indentation, control-flow, and import-ordering errors during the move — consistent with the kind of bug already seen in Sprint 2 (BUG-003, BUG-004), reinforcing that a syntax/smoke check after every extraction step is worth doing as a standing habit, not just a one-off lesson from BUG-001.

- BUG-002 (cursor visibility) and BUG-005 (cursor lag) remain open at project end of development, since both are rooted in VNC limitations.
