# Bug Tracker

Use this file to record all bugs from now on.

## Status Key

- Open: Bug is confirmed and not fixed yet.
- In Progress: Bug is being worked on.
- Fixed: Bug is resolved in code.
- Verified: Fix has been tested and confirmed.

## Bug Entry Template

### BUG-XXX - Short Title

- Date Reported: YYYY-MM-DD
- Reported By: Name
- Severity: Low | Medium | High | Critical
- Status: Open | In Progress | Fixed | Verified
- Area: e.g., Rendering, UI, Combat, Input, Performance

#### Description

Describe what happened.

#### Steps to Reproduce

1. Step one.
2. Step two.
3. Step three.

#### Expected Result

What should happen.

#### Actual Result

What actually happened.

#### Suspected Cause

Optional notes about possible root cause.

#### Fix Implemented

What was changed to fix it.

#### Verification

How the fix was tested.

#### Notes

Any extra context.

---

## Logged Bugs

### BUG-001 - Black screen after adding enemy statistics

- Date Reported: 2026-06-01
- Reported By: User
- Severity: High
- Status: Fixed
- Area: Rendering / Startup

#### Description

Game appeared as a black screen after enemy statistics display code was added.

#### Steps to Reproduce

1. Add enemy stats drawing block in panel rendering function.
2. Start game with start.sh.

#### Expected Result

Game should render background, panel, fighters, and enemy stats.

#### Actual Result

Game failed to render and appeared as black screen.

#### Suspected Cause

Syntax error prevented normal execution of game loop.

#### Fix Implemented

Removed unmatched closing parenthesis in enemy stats draw_text call in main.py.

#### Verification

- Syntax check passed: python3 -m py_compile main.py
- Runtime smoke test started successfully for 5 seconds without immediate crash.

#### Notes

If black screen happens again, first run syntax checks before launching the VNC stack.

---

### BUG-002 - Default cursor still visible over enemy hover

- Date Reported: 2026-06-04
- Reported By: User
- Severity: Medium
- Status: In Progress
- Area: Input / UI

#### Description

When hovering enemies, the katana cursor appears but the default cursor still remains visible in some runs.

#### Steps to Reproduce

1. Start game in VNC.
2. Move mouse over an alive enemy.
3. Observe cursor rendering.

#### Expected Result

Only katana cursor should be visible while hovering enemy.

#### Actual Result

Default cursor can remain visible together with katana.

#### Suspected Cause

VNC client-side cursor overlay may ignore or delay pygame visibility toggles.

#### Fix Implemented

Hover detection and cursor hide/show logic were updated to run per frame.

#### Verification

Visual hover tests performed during Sprint 2 iterations.

#### Notes

Behavior may differ between local display and VNC session.

---

### BUG-003 - Blank screen after hover code indentation changes

- Date Reported: 2026-06-04
- Reported By: User
- Severity: High
- Status: Fixed
- Area: Rendering / Game Loop

#### Description

Game displayed blank screen after cursor/hover logic edits.

#### Steps to Reproduce

1. Add hover logic with incorrect indentation.
2. Run game.
3. Screen appears blank.

#### Expected Result

Normal render loop should continue each frame.

#### Actual Result

Core update/render sections were skipped or nested incorrectly.

#### Suspected Cause

Mis-indentation moved core loop logic under conditional branch.

#### Fix Implemented

Restored correct indentation so only katana draw is conditional and frame logic always runs.

#### Verification

Game returned to normal rendering after correction.

#### Notes

Loop indentation must be rechecked after manual paste edits.

---

### BUG-004 - Katana cursor not appearing on hover

- Date Reported: 2026-06-04
- Reported By: User
- Severity: High
- Status: Fixed
- Area: Input / Cursor Rendering

#### Description

Katana cursor failed to render even when hovering enemy.

#### Steps to Reproduce

1. Hover enemy after recent cursor refactor.
2. Observe no katana image.

#### Expected Result

Katana image should replace cursor when hovering an enemy.

#### Actual Result

No katana shown.

#### Suspected Cause

Draw block was nested inside loop and skipped after break.

#### Fix Implemented

Moved katana draw logic outside hover-detection loop to execute once per frame.

#### Verification

Katana appeared again on hover after restructuring.

#### Notes

Break statements can bypass rendering when draw code is inside detection loops.

---

### BUG-005 - Katana cursor lag/trailing behind mouse

- Date Reported: 2026-06-04
- Reported By: User
- Severity: Medium
- Status: In Progress
- Area: Input / Performance / VNC

#### Description

Katana cursor visually trails behind mouse movement and feels unsmooth.

#### Steps to Reproduce

1. Run game in VNC.
2. Hover enemies and move mouse quickly.
3. Observe trailing effect.

#### Expected Result

Katana tip should track mouse with minimal perceived delay.

#### Actual Result

Visible lag remains.

#### Suspected Cause

Frame-based software cursor plus remote display latency in VNC.

#### Fix Implemented

Moved cursor draw to end-of-frame and tested higher frame pacing.

#### Verification

Partial improvement observed; residual delay persists in VNC.

#### Notes

Some delay may be unavoidable in remote sessions.

---

### BUG-006 - Katana blade tip not aligned with mouse point

- Date Reported: 2026-06-04
- Reported By: User
- Severity: Low
- Status: Fixed
- Area: UI / Cursor Alignment

#### Description

Katana image appears off-center relative to intended blade tip location.

#### Steps to Reproduce

1. Enable katana hover cursor.
2. Hover enemy and inspect blade tip position.

#### Expected Result

Blade tip aligns with actual mouse target point.

#### Actual Result

Katana appears offset from target point.

#### Suspected Cause

Cursor anchoring used image center or incorrect hotspot direction.

#### Fix Implemented

Applied hotspot-based positioning and adjusted hotspot toward icon tip.

#### Verification

Alignment improved after hotspot correction.

#### Notes

Hotspot may require minor pixel tuning based on icon orientation.
