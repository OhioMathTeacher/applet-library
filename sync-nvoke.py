#!/usr/bin/env python3
"""Republish TCE 318P's nVoke as the standalone applet.

    python3 sync-nvoke.py                    # uses ../tce318p-fa26/…
    python3 sync-nvoke.py path/to/nvoke.html
    python3 sync-nvoke.py --check            # say whether the copy is stale; change nothing

nvoke.html in the course repo is the SOURCE. Nobody edits nvoke/index.html here by
hand -- this script rewrites it, so a hand edit is lost on the next run. Keeping one
source is the point: the course copy is the one Todd teaches from and therefore the
one that gets fixed, and two hand-maintained copies of 1,700 lines drift apart.

The standalone differs from the course copy in exactly one way, and it is a real
hazard rather than a cosmetic choice: BOTH copies are served from
ohiomathteacher.github.io, so they share one browser origin, and IndexedDB is scoped
to the origin. Left alone, the public applet would open the same 'seesay' and
'nvoke-transcripts' stores the course activity writes to -- reading transcripts of
partner answers recorded in class. So the store names are rewritten here. Everything
else, including the ?embed=planner handshake, is carried over untouched.
"""
import sys, pathlib, re, difflib

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_SRC = HERE.parent / "tce318p-fa26" / "week-3-geometry-van-hiele" / "nvoke.html"
DEST = HERE / "nvoke" / "index.html"

# (what to find, what to write, why). Each MUST match exactly once: if the course copy
# is refactored so a marker moves or changes shape, this stops rather than silently
# publishing an applet that shares the classroom's database.
REWRITES = [
    ('const DBN="seesay",STORE="packs";',
     'const DBN="nvoke-standalone",STORE="packs";',
     "prompt packs"),
    ('const TDBN="nvoke-transcripts";',
     'const TDBN="nvoke-standalone-transcripts";',
     "handoff transcripts"),
]

BANNER = """<!--
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  GENERATED FILE — do not edit.                                          │
  │                                                                         │
  │  Source:  tce318p-fa26/week-3-geometry-van-hiele/nvoke.html             │
  │  Rebuild: python3 sync-nvoke.py      (from the applet-library root)     │
  │                                                                         │
  │  Edit the course copy and re-run the script. The only difference here   │
  │  is that the IndexedDB stores are renamed: both copies are served from  │
  │  the same origin, and without this the public applet would share the    │
  │  classroom's packs and its transcripts of partner answers.              │
  └─────────────────────────────────────────────────────────────────────────┘
-->
"""

def build(src_text):
    out = src_text
    for find, repl, what in REWRITES:
        n = out.count(find)
        if n != 1:
            raise SystemExit(
                "sync-nvoke: expected exactly one %r in the source (the %s store), found %d.\n"
                "The course copy has changed shape. Fix REWRITES in this script before "
                "republishing -- shipping it unchanged would share the classroom's database."
                % (find, what, n))
        out = out.replace(find, repl)
    # banner goes under the doctype so the file still starts the way a browser expects
    m = re.match(r'(<!DOCTYPE html>\s*\n)', out, re.I)
    if not m:
        raise SystemExit("sync-nvoke: source does not start with <!DOCTYPE html>.")
    return m.group(1) + BANNER + out[m.end():]

def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv[1:]
    src = pathlib.Path(args[0]) if args else DEFAULT_SRC
    if not src.exists():
        # Exit 2, distinct from 1: "I could not check" is not "the copy is wrong",
        # and the pre-commit hook has to tell those apart to know whether to block.
        print("sync-nvoke: no source at %s" % src, file=sys.stderr)
        return 2

    built = build(src.read_text())
    current = DEST.read_text() if DEST.exists() else None

    if check:
        if current == built:
            print("nvoke/index.html is current with %s" % src)
            return 0
        print("nvoke/index.html is STALE against %s" % src)
        print("  Either the course copy moved ahead, or this file was edited by hand.")
        print("  Either way the fix is the same: python3 sync-nvoke.py")
        if current is not None:
            diff = list(difflib.unified_diff(current.splitlines(), built.splitlines(),
                                             "published", "rebuilt", lineterm="", n=0))
            print("  %d differing lines; first few:" % len([d for d in diff if d[:1] in "+-"]))
            for line in diff[:12]:
                print("   ", line)
        return 1

    DEST.parent.mkdir(parents=True, exist_ok=True)
    if current == built:
        print("nvoke/index.html already current — nothing written.")
        return 0
    DEST.write_text(built)
    print("wrote %s (%d KB) from %s" % (DEST.relative_to(HERE), len(built) // 1024, src))
    for _, repl, what in REWRITES:
        print("   %s → %s" % (what, repl.split('"')[1]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
