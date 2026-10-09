#!/usr/bin/env python3
"""Republish the retro games from their own repos as applets.

    python3 sync-games.py            # copy every game in GAMES
    python3 sync-games.py --check    # say whether any copy is stale; change nothing

Each game's index.html in ../<repo> IS THE SOURCE. Nobody edits the copies here
by hand -- this script rewrites them, so a hand edit is lost on the next run.
Same reasoning as sync-dragonkeep.py: one source, no drift.

The game repos are private; only what this script copies becomes public. That is
index.html and the README's player-facing part (everything above "## How to run",
which talks about the repo rather than the game). NEXT-STEPS.md, tools/ and the
rest of the repo are never copied.

Unlike Dragonkeep, no storage keys are rewritten: each game already namespaces
its one localStorage key (the high score), and the game repos are not published
to Pages, so nothing else on this origin shares them.
"""
import sys
import pathlib
import difflib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = "https://ohiomathteacher.github.io/applet-library/"

# (source repo next to this one, folder here)
GAMES = [
    ("haunt", "haunt"),
    ("chomp-and-spell", "chomp-and-spell"),
    ("circuit-breaker", "circuit-breaker"),
]

BANNER = """<!--
  GENERATED FILE - DO NOT EDIT
  Source:    ../{repo}/index.html
  Rewritten: python3 sync-games.py
  Edits made here are lost on the next sync. Fix the game in the
  {repo} repo and re-run the script.
-->
"""


def build(repo, folder):
    """Return {path: text} for one game's published files."""
    src = HERE.parent / repo
    page = src / "index.html"
    readme = src / "README.md"
    for f in (page, readme):
        if not f.is_file():
            raise SystemExit("sync-games: no source at %s" % f)

    player_part = readme.read_text().split("\n## How to run", 1)[0].rstrip()
    return {
        HERE / folder / "index.html": BANNER.format(repo=repo) + page.read_text(),
        HERE / folder / "README.md": player_part
            + "\n\n## Play\n\n**Live**: %s%s/\n\nOne file, no install, no network.\n" % (LIVE, folder),
    }


def main():
    check = "--check" in sys.argv[1:]
    stale = 0
    for repo, folder in GAMES:
        for dest, text in build(repo, folder).items():
            current = dest.read_text() if dest.is_file() else None
            name = dest.relative_to(HERE)
            if current == text:
                print("Up to date: %s" % name)
                continue
            if check:
                stale += 1
                if current is None:
                    print("STALE: %s does not exist yet." % name)
                    continue
                diff = list(difflib.unified_diff(
                    current.splitlines(), text.splitlines(),
                    fromfile="published", tofile="rebuilt", lineterm="", n=0))
                print("STALE: %s, %d differing line(s)." % (name, len(diff)))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text)
            print("Wrote %s (%d bytes)" % (name, len(text)))
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
