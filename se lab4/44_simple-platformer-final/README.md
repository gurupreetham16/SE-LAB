# Real-Time Simple Platformer - Final

Completed tasks:

1. Refined platform collision detection using previous/current vertical positions so high-speed falls do not tunnel through platforms.
2. Added an on-screen Game Over screen showing the reason and final score.
3. Added replay after Game Over with Easy, Medium, and Hard difficulty choices.
4. Added sound feedback for jumping, reaching the goal, and dying.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Controls:
- Left/Right or A/D: move
- Space/Up/W: jump
- After Game Over: 1 = Easy, 2 = Medium, 3 = Hard
- Q/Esc = exit

## Task 1 collision fix

The player stores its previous bottom position before vertical movement. After movement, the code checks whether the player's vertical path crossed the top of a platform while moving downward. If so, the player is snapped to the platform and vertical velocity is reset.

## Task 2 Game Over

Falling below the screen or touching the red hazard displays a Game Over overlay instead of only printing to the terminal.

## Task 3 Replay

The Game Over screen lets the player restart with:
- Easy: lower gravity and stronger jump
- Medium: original gravity/jump
- Hard: higher gravity and reduced jump strength

## Task 4 Sound

WAV effects are included for:
- jump
- goal
- death
