#!/usr/bin/env python3
"""Build the landing page for each family of games, from families.json, READMEs and teaching.json.

    python3 make-notes.py            # write every family page
    python3 make-notes.py --check    # say whether any page is stale; change nothing

The library shows one card per family (maze games, shooting games, ...). Each card opens
<family>/index.html, which introduces the family and gives every game in it a block: what
it is, whether it is ready as a teaching tool, what is in it now, the ideas being
considered, a Play button and the rules.

Nothing on these pages is written twice:

  families.json  which games belong together, and a line about each family.
  README.md      what each game is and how to play it. sync-games.py copies it from the
                 game's own repo; it is never edited here. Run this after sync-games.py.
  teaching.json  the teaching side of each game, kept here. "ready" or "building";
                 "by" records whose idea each one is and is never shown.

A game with its own live site (Dragonkeep) is linked, never copied: families.json gives
its address, its README in the sibling repo (read as last committed), and its teaching.

The feedback invitation appears once a family has a feedback_doc link.
"""
import html
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

BANNER = """<!--
  GENERATED FILE - DO NOT EDIT
  Built from families.json, each game's README.md and teaching.json by: python3 make-notes.py
-->
"""

# ------------------------------------------------------------------ a little Markdown

def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def markdown(md: str) -> str:
    """Paragraphs, lists, tables and ### headings: what the game READMEs use."""
    out, para, items, rows = [], [], [], []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in items) + "</ul>")
            items.clear()
        if rows:
            head, body = rows[0], [r for r in rows[1:] if not set("".join(r)) <= set("-: ")]
            out.append("<table><thead><tr>" + "".join("<th>" + inline(c) + "</th>" for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join("<td>" + inline(c) + "</td>" for c in r) + "</tr>"
                                 for r in body)
                       + "</tbody></table>")
            rows.clear()

    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("|"):
            if para or items:
                flush()
            rows.append([c.strip() for c in s.strip("|").split("|")])
        elif re.match(r"^#{3,}\s", s):
            flush()
            out.append("<h4>" + inline(s.lstrip("#").strip()) + "</h4>")
        elif re.match(r"^([-*]|\d+\.)\s", s):
            if para or rows:
                flush()
            items.append(re.sub(r"^([-*]|\d+\.)\s+", "", s))
        elif items and line.startswith((" ", "\t")):
            items[-1] += " " + s
        else:
            if items or rows:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


def readme_parts(text: str):
    """Title, the intro above the first section, and every section except ## Play."""
    title = re.search(r"^#\s+(.+)$", text, re.M).group(1).strip()
    body = text.split("\n", 1)[1]
    chunks = re.split(r"^##\s+(.+)$", body, flags=re.M)
    intro = chunks[0].strip()
    sections = [(chunks[i].strip(), chunks[i + 1].strip()) for i in range(1, len(chunks), 2)]
    sections = [(h, b) for h, b in sections if h.lower() != "play"]
    return title, intro, sections


def icon(game_id: str) -> str:
    """The game's icon, the same drawing as on its card: icons/<id>.svg."""
    f = HERE / "icons" / (game_id + ".svg")
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


# ------------------------------------------------------------------ the games

def committed(path: pathlib.Path) -> str:
    """A sibling repo's file as last committed, never its working copy."""
    repo = path.parent
    return subprocess.run(["git", "-C", str(repo), "show", "HEAD:" + path.name],
                          check=True, capture_output=True, text=True).stdout


def load_game(entry, index_html):
    """Everything a game block needs, from a folder here or an inline entry."""
    if isinstance(entry, str):
        folder = entry
        title, intro, sections = readme_parts((HERE / folder / "README.md").read_text(encoding="utf-8"))
        return {"id": folder, "name": title, "play": "../" + folder + "/", "intro": intro,
                "sections": sections, "icon": icon(folder),
                "teaching": json.loads((HERE / folder / "teaching.json").read_text(encoding="utf-8"))}
    title, intro, sections = readme_parts(committed((HERE / entry["readme"]).resolve()))
    keep = [h.lower() for h in entry.get("howto", [])]
    if keep:
        sections = [(h, b) for h, b in sections if h.lower() in keep]
    return {"id": entry["id"], "name": entry.get("name", title), "play": entry["url"],
            "intro": entry.get("intro", intro), "sections": sections,
            "icon": icon(entry["id"]),
            "teaching": entry["teaching"]}

# ------------------------------------------------------------------ the page

CSS = """
:root{--ink:#121212;--muted:#363636;--rule:#dcdcdc;--tile:#f7f6f3;--yellow:#f7da21;--green:#6aaa64;
  --blue:#6f95e8;--purple:#b582d6;--pink:#f4a3c0;--teal:#5cc4b8;--orange:#f39b4a}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:var(--ink)}
body{font-family:"Libre Franklin",system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.55}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 64px}
.crumbs{font-size:14px;color:var(--muted)}
.crumbs a{text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.crumbs span{color:var(--ink);font-weight:700}
h1{font-size:36px;font-weight:800;letter-spacing:-.01em;margin:14px 0 8px}
.lead{font-size:18px;color:var(--muted);margin:0 0 14px}
.note{background:#f3ece0;border-left:4px solid #c9a46a;border-radius:6px;padding:14px 18px;font-size:16px;margin:18px 0 0}
.games{display:grid;grid-template-columns:repeat(var(--cols,2),minmax(0,1fr));gap:18px;margin-top:28px}
.game{--wash:#eef1f5;--deep:#4f6a9a;display:flex;flex-direction:column;border:1.5px solid var(--deep);border-top-width:6px;
  border-radius:10px;padding:20px;background:var(--wash)}
.game.c0{--wash:#eaf1f7;--deep:#4f6f96}
.game.c1{--wash:#f6ece6;--deep:#a0694a}
.game.c2{--wash:#e8f2ec;--deep:#4f8064}
.game.c3{--wash:#f1eaf4;--deep:#7d5f8f}
.ghead{display:flex;align-items:flex-start;gap:14px;margin-bottom:10px}
.tile{flex:none;width:76px;height:76px;background:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center}
.tile svg{width:44px;height:44px;overflow:visible}
.ic{stroke:var(--ink);stroke-width:2.5;stroke-linejoin:round}
.ic-thin{fill:none;stroke:var(--ink);stroke-width:2;stroke-linecap:round}
h2{font-size:24px;font-weight:800;margin:4px 0 0;line-height:1.15}
.intro{font-size:16px;color:var(--muted);margin:0 0 6px}
.status{display:inline-block;padding:2px 9px;font-size:12px;font-weight:700;letter-spacing:.02em;
  border:1.5px solid var(--ink);border-radius:3px}
.status.ready{background:var(--green);color:#fff;border-color:var(--green)}
.status.building{background:var(--yellow)}
.btn{display:inline-block;padding:10px 18px;font-weight:700;font-size:15px;text-decoration:none;
  border:2px solid var(--ink);border-radius:6px;text-align:center}
.push{flex:1}
.btn.play{background:var(--deep);border-color:var(--deep);color:#fff;margin-top:16px}
.btn:hover{background:#fff;color:var(--deep)}
h3{font-size:15px;font-weight:800;margin:16px 0 6px;color:var(--deep)}
h4{font-size:15px;margin:16px 0 6px}
p,li{font-size:15px}
ul{padding-left:1.2em;margin:0 0 8px}
li{margin:0 0 5px}
.none{color:var(--muted);margin:0}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:6px 0 12px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.9em;background:var(--tile);padding:1px 4px}
details{margin-top:12px;border-top:1px solid color-mix(in srgb,var(--deep) 30%,transparent);padding-top:10px}
details summary{cursor:pointer;font-size:15px;font-weight:800}
details[open] summary{margin-bottom:8px}
.ask{margin-top:48px;padding:20px 22px;background:var(--tile)}
.ask h2{font-size:22px;margin:0 0 6px}
@media (max-width:1000px){.games{grid-template-columns:repeat(min(var(--cols,2),2),minmax(0,1fr))}}
@media (max-width:640px){.games{grid-template-columns:minmax(0,1fr)}h1{font-size:28px}}
"""


def game_block(g, n: int = 0) -> str:
    """One card: icon, status and name, the intro, what it teaches, then Play at the
    bottom. The longer material folds away inside the card."""
    t, e = g["teaching"], html.escape
    ready = t["status"] == "ready"
    badge = ('<span class="status ready">Ready to use</span>' if ready
             else '<span class="status building">Under construction</span>')
    ext = g["play"].startswith("http")
    play = ('<a class="btn play" href="' + e(g["play"]) + '"'
            + (' target="_blank" rel="noopener"' if ext else "") + ' aria-label="Play ' + e(g["name"]) + '">▶ Play</a>')
    out = ['<section class="game c' + str(n % 4) + '" id="' + e(g["id"]) + '"><div class="ghead"><span class="tile">' + g["icon"]
           + "</span><div>" + badge + "<h2>" + e(g["name"]) + "</h2></div></div>"
           + '<p class="intro">' + inline(" ".join(g["intro"].split())) + "</p>"]
    if ready:
        out.append("<h3>What students practice</h3><ul>"
                   + "".join("<li>" + inline(x) + "</li>" for x in t.get("practice", [])) + "</ul>")
        if t.get("thinking"):
            out.append("<h3>The thinking it makes visible</h3><p>" + inline(t["thinking"]) + "</p>")
    else:
        now = t.get("now", [])
        out.append("<h3>In it now</h3>" + ("<ul>" + "".join("<li>" + inline(x) + "</li>" for x in now) + "</ul>"
                                         if now else '<p class="none">Nothing yet. It is a game for now.</p>'))
    out.append('<div class="push"></div>')
    ideas = t.get("considering", [])
    if ideas:
        out.append("<details><summary>Ideas we are considering</summary><ul>"
                   + "".join("<li>" + inline(i["text"]) + "</li>" for i in ideas) + "</ul></details>")
    if g["sections"]:
        body = "\n".join(("<h4>" + inline(h) + "</h4>" if h.lower() != "how to play" else "") + markdown(b)
                         for h, b in g["sections"])
        out.append('<details><summary>How to play</summary><div class="scroll">' + body + "</div></details>")
    out.append(play + "</section>")
    return "\n".join(out)


def page(fam, index_html: str) -> str:
    e = html.escape
    games = [load_game(x, index_html) for x in fam["games"]]
    building = [g for g in games if g["teaching"]["status"] != "ready"]
    parts = ['<nav class="crumbs" aria-label="You are here"><a href="../">Applet Library</a> › '
             '<a href="../?section=games">Retro Educational Games</a> › <span>' + e(fam["name"]) + "</span></nav>",
             "<h1>" + e(fam["name"]) + '</h1><p class="lead">' + inline(fam["blurb"]) + "</p>"]
    if building:
        which = ("All of these games are" if len(building) == len(games)
                 else ", ".join(g["name"] for g in building) + (" is" if len(building) == 1 else " are"))
        parts.append('<p class="note">' + e(which) + " playable now and still becoming "
                     + ("teaching tools" if len(building) > 1 else "a teaching tool")
                     + ". The gameplay came first, on purpose; the teaching is being added one game at a "
                     "time. Each card says what the game has so far and what we are considering.</p>")
    parts.append('<div class="games" style="--cols:' + str(min(len(games), 4)) + '">'
                 + "\n".join(game_block(g, i) for i, g in enumerate(games)) + "</div>")
    fb = fam.get("feedback_doc", "").strip()
    if fb:
        parts.append('<section class="ask"><h2>Help us make them educational</h2><p>How could we turn '
                     "these into games students learn from? What would you have them teach, and how? "
                     "If you have used one with students, tell us how it went. Play them, then add your "
                     'ideas to the shared document.</p><p><a class="btn" href="' + e(fb)
                     + '" target="_blank" rel="noopener">Add Your Feedback (Google Doc)</a></p></section>')
    return (BANNER + '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            "<title>" + e(fam["name"]) + " · Applet Library</title>\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;700;800&display=swap" rel="stylesheet">\n'
            "<style>" + CSS + "</style>\n</head>\n<body>\n<main class=\"wrap\">\n"
            + "\n".join(parts) + "\n</main>\n"
            '<script src="../site-header.js" data-current="games" defer></script>\n'
            "</body>\n</html>\n")


START, END = "<!-- families:start (written by make-notes.py) -->", "<!-- families:end -->"


def library_cards(fams, index_html: str) -> str:
    """The games section of the library page: one card per family, its icon made of the
    family's own icons. A family whose games are all still being built is marked so."""
    cards = []
    for fam in fams:
        games = [load_game(x, index_html) for x in fam["games"]]
        icons = "".join('<span class="mini">' + g["icon"] + "</span>" for g in games)
        wip = all(g["teaching"]["status"] != "ready" for g in games)
        names = ", ".join(g["name"] for g in games)
        cards.append(
            '        <a class="card" href="' + fam["id"] + '/">\n'
            '          <span class="tile fam n' + str(len(games)) + '">' + icons + "</span>\n"
            "          <span><b>" + html.escape(fam["name"])
            + (' <span class="wip">Under construction</span>' if wip else "") + "</b>"
            '<span class="blurb">' + html.escape(fam["blurb"]) + "</span>"
            '<span class="blurb members">' + html.escape(names) + "</span></span>\n"
            "        </a>")
    return START + "\n" + "\n".join(cards) + "\n        " + END


def main() -> int:
    check = "--check" in sys.argv
    index_html = (HERE / "index.html").read_text(encoding="utf-8")
    fams = json.loads((HERE / "families.json").read_text(encoding="utf-8"))["families"]
    stale = 0
    i, j = index_html.find(START), index_html.find(END)
    if i < 0 or j < 0:
        raise SystemExit("make-notes: index.html has no families markers")
    lib = index_html[:i] + library_cards(fams, index_html) + index_html[j + len(END):]
    if lib != index_html:
        stale += 1
        if check:
            print("stale: index.html (the games section)")
        else:
            (HERE / "index.html").write_text(lib, encoding="utf-8")
            print("wrote index.html (the games section)")
    for fam in fams:
        out = HERE / fam["id"] / "index.html"
        new = page(fam, index_html)
        old = out.read_text(encoding="utf-8") if out.exists() else ""
        if new == old:
            continue
        stale += 1
        if check:
            print("stale: " + str(out.relative_to(HERE)))
        else:
            out.parent.mkdir(exist_ok=True)
            out.write_text(new, encoding="utf-8")
            print("wrote " + str(out.relative_to(HERE)))
    if check:
        print("all family pages current" if not stale else str(stale) + " stale")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
