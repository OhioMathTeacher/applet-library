# Chomp & Spell

Eat the letters, then spell the words. A retro maze game for an NES-style controller.

## How to play

Clear every dot in the maze while four ghosts chase you. The power pellets are
**letters**: eating one turns the ghosts blue (eat them for points) and puts
that letter in your **rack** at the bottom of the screen. Each letter you eat
makes a new bonus letter pop up somewhere else a moment later. Bonus letters
don't scare the ghosts and vanish if you leave them too long.

When the dots are gone, the **spelling round** begins:

- Build words from your rack. Each tile can be used **once in the whole
  round**, so choose: QUIZ now, or save the U for something longer?
- Words must be 2–8 letters and in the game's word list.
- A word scores its Scrabble letter values, plus a bonus for 5+ letters, times 10.
- Tiles you don't spend carry over to the next level (the rack holds 16).

You start with 3 lives and earn one more at 10,000 points.

## Controls

| Button | Keyboard | In the maze | In the spelling round |
|---|---|---|---|
| D-pad | Arrows or WASD | Move (turns wait for the next opening) | Move the cursor over your tiles |
| A | Z or K | — | Add the highlighted tile to the word |
| B | X or J | — | Remove the last letter (Backspace) |
| Start | Enter (or P) | Pause | Submit the word |
| Select | Shift | — | Finish the round (press twice) |

In the spelling round, keyboard players can also just **type letters**, then
Enter to submit and Backspace to undo. M toggles sound (anywhere but the
spelling round, where M is a letter); MUTE shows in the corner while it's off.

A USB gamepad works through the browser's Gamepad API; press any button on it
once the page is open so the browser notices it.

## Play

**Live**: https://ohiomathteacher.github.io/applet-library/chomp-and-spell/

One file, no install, no network.
