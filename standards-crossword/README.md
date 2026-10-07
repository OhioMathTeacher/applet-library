# Standards Crossword

An NYT-style crossword for reviewing academic content standards. Pick a
framework, content area, grade and standard, and solve.

**Live**: https://ohiomathteacher.github.io/applet-library/standards-crossword/

## Where the puzzles come from

1. **The library** (`library.js`): teacher-made puzzles, each tied to one
   standards document and the standards it covers. These are listed first,
   under "Puzzle ready", and work offline.
2. **genAI, when there's no library puzzle**: an AI model picks the words and
   writes the clues from the standard's official text. The puzzle is labeled
   genAI-generated, names the model that wrote it, and is not reviewed by a
   teacher. It needs a model chosen in **AI Setup** (below).

Choosing a standard with no puzzle opens it at its own address (`#s=…`), so
the **← All puzzles** link at the top and the browser's Back button both
return to the puzzle list, and the address can be shared.

## Español

The **Español / English** button at the top right switches the student-facing
app (menus, buttons, messages, worksheet labels) and is remembered in that
browser; a browser set to Spanish starts in Spanish. In Spanish, genAI writes
the words, clues and "why" sentences in Spanish, and Spanish puzzles are kept
apart from English ones: a standard with only an English library puzzle offers
to generate a Spanish one. The grid takes **Ñ**; accents are dropped in the
grid, as in Spanish crosswords, and kept in the clues. Standards text stays as
published, in English. The builder stays in English; a library entry with
`"l": "es"` is a Spanish puzzle.

## Why this word?

Each word can carry one sentence on why it matters for the standard. genAI
writes one for every word; in the builder, add one after a bar:
`WORD: clue | why it matters`. They stay hidden while solving, appear under
each clue once the puzzle is solved, and print on the answer key.

## Printing

Every puzzle has a **Print** menu: **Worksheet** prints one page with the
standard, a Name and Date line, the empty grid and the clues;
**Worksheet + answer key** adds a second page with the filled grid and the
answers. A genAI puzzle's footer names the model that wrote it.

## Keeping a genAI puzzle

A genAI puzzle that's worth keeping has **Edit in builder** beside its label.
It opens the puzzle in the builder with its words, clues and standard filled
in. Fix anything that needs it, then **Copy library entry** and paste the line
into `library.js`: from then on every student sees it under "Puzzle ready",
with no AI needed.

## AI Setup

The **AI Setup** button at the top right offers the same choice as Clique,
Journaler and Allegory. The choice, and any key, stay in that browser.

- **Local model (recommended)**: [Ollama](https://ollama.com/) or any
  OpenAI-compatible server. AI Setup finds Ollama at `127.0.0.1:11434` and
  LM Studio at `127.0.0.1:1234`; **+ Add local server** takes any other
  address. No key, no cost, nothing leaves the computer. A small model such as
  `qwen2.5:3b` runs on most laptops; a large one such as `qwen3.8:27b` writes
  noticeably better clues, in under 20 seconds on a workstation GPU.
- **Groq** or **Gemini**: free keys. Use a personal Gmail for Gemini, not a
  school account.
- **Claude**: your own Anthropic key (Claude Opus 5). Give it a low spending
  limit.
- **No AI**: teacher-made puzzles only.

On the hosted (HTTPS) page, Safari blocks calls to a local `http://` server;
Chrome allows them, but Ollama must also allow the site's origin:
`OLLAMA_ORIGINS=https://ohiomathteacher.github.io`, then restart Ollama.
Running a local copy (`python3 -m http.server` in this folder) avoids both.

A key saved here can be used, or read from browser storage, by anyone using
that browser. Don't save one on shared computers you don't control. Browsers
that used the old builder key box carry their Claude key over automatically.

## The builder

Open `index.html#puzzle-builder`; nothing links to it. Pick the standards,
write or draft words and clues, check the layout, then either:

- **Copy library entry** and paste the line into `library.js`, or
- **Copy student link**. The whole puzzle lives in the link, answers
  included.

**Draft words with genAI** uses the model chosen in AI Setup.

## Standards data

`standards/` holds 92 standards documents (Common Core, NGSS, Ohio, CSTA)
from the [Common Standards Project](https://commonstandardsproject.com),
one small file per document, loaded only when picked, so the app works
offline and from `file://`. Each document carries its source and license
(mostly CC BY 3.0 US). To add a framework or state, add a line to `PICKS`
in `tools/build_standards.py` and run it (needs internet):

    python3 tools/build_standards.py

Never type standards text by hand; regenerate it from the source.
