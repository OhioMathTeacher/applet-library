# Routines & Conjecturing — TCE 412M guest session, Tue 29 Sep 2026

Naz Bautista's middle-grades methods class, 10:05 to about 11:15, 316 McGuffey.
Naz asked for a modeled math methods lesson for middle school.

- **Slides (public):** https://ohiomathteacher.github.io/applet-library/tce412-routines-conjecturing/
  — arrow keys, space, or click to move; **N** shows speaker notes; **F** is full screen;
  `#12` in the address opens slide 12.
- **Handouts:** https://ohiomathteacher.github.io/applet-library/tce412-routines-conjecturing/handouts/
- **Editable deck (private, claude.ai):** https://claude.ai/artifact/8hGrVxjjEEULSSjn4bqNUG

## Flow

| Time | Slides | What happens |
|---|---|---|
| 10:05 | 1–2 | Welcome, the plan |
| ~10:07 | 3–7 | Routines as learners: Dan Meyer's Nissan Girl Scout Cookies three-act task, Which One Doesn't Belong (9, 16, 25, 43), Would You Rather #50 (70% vs 40/20/10) |
| 10:30 | 8–10 | Switch hats (three questions), "Warm it up. Don't give it away.", nVoke prompt pack. Hand out the field guide |
| ~10:40 | 11–14 | School math vs. research math, the 3n − 1 rule on 1–5 by hand, four moves in Orbit Explorer, the Collatz reveal. Hand out the task card |
| 11:05 | 15–16 | Teacher hat, open problems. Hand out the open-problems handout |
| — | 17–25 | Optional: one slide per open problem |

## Before class

- Move 3 in Orbit Explorer: max steps must be raised to 200 before running 27.

## Files

- `index.html` — the slides, built from the claude.ai deck by `src/build_slides_site.py`
- `img/` — slide images (the Nissan task stills, the eight open-problem pictures)
- `handouts/` — the three printed handouts and an index page
- `src/` — handout HTML; rebuild a PDF with `python3 render.py <file>.html <out>.pdf`
  (needs Playwright and /usr/bin/chromium-browser)
- Reading: Newell & Orton (2018), "Classroom Routines: An Invitation for Discourse,"
  *Teaching Children Mathematics* 25(2), 94–102. https://www.jstor.org/stable/10.5951/teacchilmath.25.2.0094
- Open problems: https://ohiomathteacher.github.io/applet-library/open-problems/
  (source and build scripts in `../open-problems/src`)
