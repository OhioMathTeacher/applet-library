# Dragonkeep

Draw a dungeon floor plan and it becomes a prism you can walk through. A
first-person crawler in the spirit of the early-1980s cartridge era, built around
one idea: **a floor plan extruded to a ceiling height is a right prism over an
irregular polygon.**

**Live**: https://ohiomathteacher.github.io/applet-library/dragonkeep/

This is the game from
[dragons-keep](https://github.com/OhioMathTeacher/dragons-keep), republished here
to stand on its own. Same game, different storage keys — see the note at the
bottom.

## What the mathematics is doing

The designer's two knobs are the two quantities students chronically conflate.
Volume is `A · h`; interior surface is `2A + P · h`. So three misconceptions fall
out of building rather than being quizzed:

- **Same volume, different wall.** *Open Hall* and *Snake Corridor* are both
  sixteen cells — identical area, identical volume, more than double the
  perimeter.
- **Surface area is not additive.** *Two Rooms Apart* is `A=18, P=24`. *Two Rooms
  Joined* is the same eighteen cells pushed together: `A=18, P=18`. Six units of
  perimeter vanish, because a shared wall stops being surface.
- **The square-cube law.** Double every dimension: volume ×8, wall ×4.

The maze index, `P ÷ 4√A`, cannot drop below 1.00 — a square of area *A* has
perimeter `4√A` and nothing beats it. Near 1.00 plays open and safe; above 2.00
is blind corners. In first person, surface area is not an abstraction: it is
what fills the screen.

## You win by not killing the dragon

It cannot be fought. Strike it and it wakes; come within *k* open steps — path
distance through floor, not straight line — and it wakes.

You win by walling it in with the bricks your party carries, then walking out
while it still breathes. Which makes *"is this level winnable?"* a **minimum
vertex cut**: the fewest cells you must turn to rock to separate the entrance
from the dragon, counting only cells outside the wake radius. The Creator panel
solves it exactly with max-flow, so the number it reports is the real one.

## How it is played

Open in **Creator**. Click to carve floor out of solid rock — clicking again
fills it back in. Drop in weapons, treasure, monsters and puzzles, set the
ceiling height, mist, wake radius and party size, and watch the six measurements
move. The perimeter is drawn thick on the plan, so the number is also a thing
you can see.

Press **Play** and it goes full screen. `Esc` steps back out. Movement is on the
numpad with forward on the top-middle key, or the arrow cluster; `.` lays a
brick. Every binding is clickable and rebindable.

Two health tracks run in parallel: swords and bows spend **War**, books and
fireballs spend **Spiritual**. Run either to zero and the expedition is over.

## In a classroom

The Creator is the assignment. "Build a keep of volume at least 60 whose wall
area is under 100" is an area–perimeter optimisation problem with a reason to
care about the answer, and the panel marks it instantly. Levels export as JSON,
so students can hand them to each other and play what someone else designed.

## A note on storage

`index.html` here is **generated** by `../sync-dragonkeep.py` from the game repo.
Do not edit it by hand; the next sync overwrites it.

Everything under `ohiomathteacher.github.io` shares one browser origin, so this
copy's saved level, panel states and key bindings use namespaced keys. Without
that, a level drawn here and a level drawn in another copy would silently
overwrite each other.
