# nVoke

**build it · pose it · read it**

A three-phase tool for finding out how someone actually sees a shape — build a
prompt pack, hand the device to your partner, then read their answers through
the van Hiele levels.

**Live**: https://ohiomathteacher.github.io/applet-library/nvoke/

## The three phases

**1 · Build.** Pick a layout and drag shapes onto the card. Five layouts ship
with it:

- **Which One Doesn't Belong?** — up to 4 shapes
- **Same & Different** — 2 shapes
- **Sort** — up to 9
- **I Spy** — up to 24
- **Single card** — one shape, asked about closely

The library holds 45 figures — quadrilaterals, triangles, many-sided shapes,
curved ones — plus editors for making your own **dot patterns** and
**ten-frames**, so the same tool covers subitizing as well as geometry. Write
the question your partner will see, add the card to the pack, and build the
next one.

**2 · Handoff.** Give the device to your partner. Two modes: *one person,
answers are kept* (a diagnostic, with an optional label for the transcript —
no full names) or *the whole room, nothing kept*. Cards can run as-is or
shuffled; dot and ten-frame cards can flash for 1–5 seconds, while geometry
cards stay on screen while your partner thinks.

**3 · Analyze.** Read what they said against the levels — for geometry, the van
Hiele progression from visual recognition to properties to relationships; for
dot patterns, counting by ones, subitizing a group, composing and decomposing.
Then decide what to offer them next.

## Where your work lives

Everything stays on the device — nothing is uploaded, and there is no account.
Prompt packs and transcripts are kept in the browser's own storage. Export a
pack as `.json` to carry it to another machine or hand it to a colleague, and
import one the same way.

This standalone copy keeps its **own** storage, separate from the copy that
runs inside TCE 318P, even though the two are served from the same domain. A
pack built in class will not appear here unless you export and import it — and,
more to the point, transcripts recorded during a class activity stay in the
class copy.

## Keeping this copy current

`nvoke/index.html` is **generated — do not edit it by hand.** The source is
`week-3-geometry-van-hiele/nvoke.html` in the TCE 318P repo, which is the copy
that gets taught from and therefore the copy that gets fixed. To republish
after changing it:

```
python3 sync-nvoke.py            # from the applet-library root
python3 sync-nvoke.py --check    # is the published copy stale?
```

The script's one job beyond copying is renaming the storage, and it refuses to
run if it can no longer find what it needs to rename — rather than quietly
publishing an applet that shares the classroom's database.

A pre-commit hook enforces this, so a hand edit cannot reach a commit by
accident. Install it once per clone:

```
ln -sf ../../tools/hooks/pre-commit .git/hooks/pre-commit
```

It blocks only when `nvoke/index.html` (or the script) is part of the commit and
does not match what the generator would produce. A commit that has nothing to do
with nVoke is never blocked — if the course copy has moved ahead, it just says
so. If the 318P repo isn't beside this one it cannot check, so it steps aside for
unrelated commits and refuses only ones touching the generated file. `git commit
--no-verify` overrides it.
