# Haunt

You are the ghosts. A retro maze game for an NES-style controller.

The computer plays Pac-Man; you steer one ghost at a time and switch between
the others. Catch him before he clears the maze.

## Rules

- **Any ghost that touches Pac-Man catches him.** The ghost you steer is a
  little faster than he is and can run him down from behind (**GOTCHA!**).
  The others run on autopilot and are slower than him, so they can't chase
  him down, but they can close a trap: block a corridor, sit on the last
  dots, come in from the other end. A catch by an autopilot ghost is a
  **TRAPPED!** and scores 1.5x.
- A catch scores (200 + 5 x dots left) x level x the mode's multiplier.
  Pac-Man eating a frightened ghost costs you 100.
- If Pac-Man clears the maze you lose a life and the level restarts.
- Power pellets turn your ghosts blue and slow for a few seconds.
- Pac-Man gets faster and smarter level by level: by level 5 he reads the
  maze for pincers and dead ends and avoids corridors where ghosts are closing
  from both ends.

## Modes

Pick on the title screen with the D-pad, then Start or A. The choice and a
separate high score for each mode are remembered.

| Mode   | Ghosts | Catch multiplier |
|--------|--------|------------------|
| EASY   | 4      | x1               |
| NORMAL | 3      | x1.5             |
| HARD   | 2      | x2               |
| SOLO   | 1 (just you) | x3         |

In SOLO there is nobody to switch to, so A, B and Select do nothing. Your
ghost is still faster than Pac-Man at every level, so it can be won.

## Sound

Chiptune music plays the whole time you are playing, synthesized in the
browser (no audio files). Its tempo follows the ghosts' speed and climbs as
the dots run out; when Pac-Man eats a power pellet it switches to a jittery
"you're the prey now" loop. **M** mutes and unmutes (remembered). Sound stops
while paused and when the tab is hidden.

## How to play

| Button  | Keyboard            | Does                              |
|---------|---------------------|-----------------------------------|
| D-pad   | Arrows or WASD      | Steer your ghost (turns are buffered) |
| A       | Z or K              | Switch to the next ghost          |
| B       | X or J              | Switch to the previous ghost      |
| Select  | Shift               | Switch to the ghost nearest Pac-Man |
| Start   | Enter (or P to pause) | Start, pause, resume            |
|         | 1-4                 | Pick a ghost directly             |
|         | M                   | Mute / unmute                     |

On the title screen the D-pad picks the mode. After Game Over, Start goes
back to the title screen.

Ghost order is red, pink, cyan, orange. A gamepad works through the browser's
standard mapping; pads that report the D-pad as a stick work too.

## Play

**Live**: https://ohiomathteacher.github.io/applet-library/haunt/

One file, no install, no network.
