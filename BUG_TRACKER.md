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
