# Circuit Breaker

Lights out. Robots in the maze. Six bullets. A retro maze game for an NES-style controller.

## How to play

The fuse is blown: you see only what your light reaches. Find the gun, shoot what hunts you, and survive one endless, escalating night.

| Button | Keyboard | Does |
|---|---|---|
| D-pad | Arrows / WASD | Move. Turns pressed early are remembered until the next junction. You face the way you last moved. |
| A | Z or K | Fire the way you're facing. |
| B | X or J | **Hold aim**: while held, your facing is locked, so you can back away and keep shooting. |
| Select | Shift | Sound on/off. |
| Start | Enter (or P) | Start / pause / resume. |

A standard USB gamepad works too. Pads that report the D-pad as an analog stick (common on cheap NES-style pads) are handled.

**What's in the dark**

- **Gun**: it appears somewhere in the maze. Walk over it to get 6 shots. When it's empty, a new gun turns up somewhere else after a few seconds. It glints now and then.
- **Bats and spiders**: touching one stuns you for 2 seconds. Shoot them for points. The spider lives in the web, top left. Bats can fly into the bunker.
- **Robots**: they hunt you, and one shot from a robot kills you. Destroy one and a tougher one replaces it: gray, then blue, then white (takes 2 hits), then red. From red on, robot shots break the bunker doors. The robot's eyes show in the dark, and you can hear it walking when it's close.
- **Bunker**: the green room in the middle. Robots and spiders can't get in and robot shots can't get through its doors, until the doors are broken.

Points: spider 50, bat 100, robot 150 × its number. Extra life every 5,000.

## Play

**Live**: https://ohiomathteacher.github.io/applet-library/circuit-breaker/

One file, no install, no network.
