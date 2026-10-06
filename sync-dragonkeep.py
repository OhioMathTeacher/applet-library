#!/usr/bin/env python3
"""Republish the dragons-keep repo's Dragonkeep as the standalone applet.

    python3 sync-dragonkeep.py                 # uses ../dragons-keep/index.html
    python3 sync-dragonkeep.py path/to/index.html
    python3 sync-dragonkeep.py --check         # say whether the copy is stale; change nothing

index.html in ../dragons-keep IS THE SOURCE. Nobody edits dragonkeep/index.html
here by hand -- this script rewrites it, so a hand edit is lost on the next run.
One source is the point: the game repo is where the work happens, and two
hand-maintained copies of two thousand lines drift apart.

The standalone differs from the source in exactly one way, and it is a real
hazard rather than a cosmetic choice. Everything under ohiomathteacher.github.io
shares ONE browser origin, and localStorage is scoped to the origin. If the game
repo is ever published to Pages as well, both copies would read and write the
same saved level, the same panel states and the same key bindings -- so a level
drawn in one would silently overwrite the other. The keys are namespaced here.

Same reasoning as sync-nvoke.py, which hit this first with IndexedDB.
"""
import sys
import pathlib
import difflib

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_SRC = HERE.parent / "dragons-keep" / "index.html"
DEST = HERE / "dragonkeep" / "index.html"

# (find, replace, why, how many times it must appear). Each count is checked: if
# the source is refactored so a key moves, is renamed or gains a sibling, this
# stops rather than silently publishing an applet that shares the game's saves.
REWRITES = [
    ("'dddh-plan-v1'",   "'dragonkeep-applet-plan-v1'",   "the saved level",    1),
    ("'dddh-panels-v1'", "'dragonkeep-applet-panels-v1'", "collapsed panels",   1),
    ("'dddh-lean'",      "'dragonkeep-applet-lean'",      "hidden masthead",    2),
]

BANNER = """<!--
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  GENERATED FILE - DO NOT EDIT                                            │
  │                                                                          │
  │  Source:    ../dragons-keep/index.html                                   │
  │  Rewritten: python3 sync-dragonkeep.py                                   │
  │                                                                          │
  │  Edits made here are lost on the next sync. Fix the game in the          │
  │  dragons-keep repo and re-run the script.                                │
  └──────────────────────────────────────────────────────────────────────────┘
-->
"""


def build(src_text):
    """Apply every rewrite, or explain exactly which one did not match."""
    out = src_text
    for find, repl, why, want in REWRITES:
        got = out.count(find)
        if got != want:
            raise SystemExit(
                "sync-dragonkeep: %r (%s) appears %d time(s), expected %d.\n"
                "The source changed shape. Nothing written -- fix this script\n"
                "rather than letting the applet share the game's storage."
                % (find, why, got, want)
            )
        out = out.replace(find, repl)
    return BANNER + out


def main():
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv[1:]
    src = pathlib.Path(args[0]) if args else DEFAULT_SRC

    if not src.is_file():
        raise SystemExit("sync-dragonkeep: no source at %s" % src)

    built = build(src.read_text())
    current = DEST.read_text() if DEST.is_file() else None

    if check:
        if current is None:
            print("STALE: %s does not exist yet." % DEST)
            sys.exit(1)
        if current == built:
            print("Up to date: %s matches %s." % (DEST.name, src))
            sys.exit(0)
        diff = list(difflib.unified_diff(
            current.splitlines(), built.splitlines(),
            fromfile="published", tofile="rebuilt", lineterm="", n=0))
        print("STALE: %d differing hunk line(s). First few:" % len(diff))
        for line in diff[:14]:
            print("  " + line)
        sys.exit(1)

    DEST.parent.mkdir(parents=True, exist_ok=True)
    if current == built:
        print("Already up to date: %s" % DEST)
        return
    DEST.write_text(built)
    for _, repl, why, _ in REWRITES:
        print("  %-34s %s" % (repl, why))
    print("\nWrote %s (%d bytes) from %s" % (DEST, len(built), src))


if __name__ == "__main__":
    main()
