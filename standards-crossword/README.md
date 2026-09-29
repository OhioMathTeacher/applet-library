# Standards Crossword

An NYT-style crossword for reviewing academic content standards. Pick a
framework, content area, grade and standard, and solve.

**Live**: https://ohiomathteacher.github.io/applet-library/standards-crossword/

## Where the puzzles come from

1. **The library** (`library.js`): teacher-made puzzles, each tied to one
   standards document and the standards it covers. These are listed first,
   under "Puzzle ready", and work offline.
2. **genAI, when there's no library puzzle**: Claude picks the words and
   writes the clues from the standard's official text. The puzzle is
   labeled as genAI-generated and not reviewed by a teacher. This needs
   internet and a Claude API key saved in the builder on that browser.

## The builder

Open `index.html#puzzle-builder`; nothing links to it. Pick the standards,
write or draft words and clues, check the layout, then either:

- **Copy library entry** and paste the line into `library.js`, or
- **Copy student link**. The whole puzzle lives in the link, answers
  included.

The genAI key is stored only in that browser's storage. Anyone using that
browser can use it, and could read it, so use a key with a spending limit
and don't save it on shared machines you don't control.

## Standards data

`standards/` holds 92 standards documents (Common Core, NGSS, Ohio, CSTA)
from the [Common Standards Project](https://commonstandardsproject.com),
one small file per document, loaded only when picked, so the app works
offline and from `file://`. Each document carries its source and license
(mostly CC BY 3.0 US). To add a framework or state, add a line to `PICKS`
in `tools/build_standards.py` and run it (needs internet):

    python3 tools/build_standards.py

Never type standards text by hand; regenerate it from the source.
