"""Detailed one-page PDF per open problem, in the handout style. Reuses the pictures from build_open_problems.py."""
import os, runpy
from html import escape
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))  # the detail-*.html working copies land here too
g = runpy.run_path(os.path.join(HERE, 'build_open_problems.py'))
PROBLEMS, OUT = g['PROBLEMS'], g['OUT']
PDF_DIR = os.path.join(OUT, 'pdf')
os.makedirs(PDF_DIR, exist_ok=True)
SITE = 'https://ohiomathteacher.github.io/applet-library/open-problems/'

DETAIL = {
 'goldbach': dict(
  tryit=['4 = 2 + 2', '10 = 3 + 7 = 5 + 5', '28 = 5 + 23 = 11 + 17', '100 = 3 + 97 = 11 + 89 = 17 + 83 = 29 + 71 = 41 + 59 = 47 + 53'],
  known=['Christian Goldbach proposed it in a 1742 letter to Leonhard Euler.',
         'Computers have checked every even number up to 4 billion billion (4 × 10¹⁸). No exceptions.',
         'In 2013 Harald Helfgott proved a “weak” version: every odd number greater than 5 is the sum of three primes.'],
  why='Checking numbers, no matter how many, is evidence, not proof. The picture suggests bigger numbers have more and more ways to work, which makes a failure seem very unlikely. But no one has found an argument that covers every even number at once.',
  classroom=['Give each group a different even number to split every possible way. Pool the results into a class table and graph it: you have built your own “comet.”',
             'Ask: Which even numbers have the most ways? (Look at multiples of 6.)',
             'Ask: Why only even numbers? What goes wrong with odd ones?'],
  words=[('Prime', 'a whole number greater than 1 whose only factors are 1 and itself'), ('Conjecture', 'a statement believed true but not yet proved')]),
 'twin-primes': dict(
  tryit=['3 and 5', '5 and 7', '11 and 13', '17 and 19', '29 and 31', '41 and 43', '59 and 61', '71 and 73'],
  known=['Euclid proved over 2,000 years ago that there are infinitely many primes. Whether there are infinitely many twins is still unknown.',
         'In 2013 Yitang Zhang proved that some gap under 70 million repeats forever. A worldwide collaboration soon brought it down to 246.',
         'So primes keep coming within 246 of each other forever. Exactly 2 apart is the open question.'],
  why='Primes thin out as numbers grow, so twins get rarer. The evidence says they never run out, but getting from “some gap of at most 246” down to a gap of exactly 2 is the step no one knows how to take.',
  classroom=['Shade the primes on a hundred chart, then circle the twin pairs. Where do twins sit?',
             'Every twin pair after 3 and 5 has a multiple of 6 between them (6, 12, 18, 30…). Ask students to notice it, then explain why it must happen.',
             'Ask: Can three numbers spaced by 2, like 3, 5, 7, ever all be prime again? (No: one of them is always a multiple of 3.)'],
  words=[('Twin primes', 'two primes that differ by 2'), ('Infinitely many', 'however many you list, there is always another')]),
 'legendre': dict(
  tryit=['1 to 4: 2, 3', '4 to 9: 5, 7', '9 to 16: 11, 13', '16 to 25: 17, 19, 23', '100 to 121: 101, 103, 107, 109, 113'],
  known=['It is named for the French mathematician Adrien-Marie Legendre. In 1912 Edmund Landau listed it, with Goldbach and twin primes, among four prime problems that seemed out of reach. All four are still open.',
         'A related fact is proved: there is always a prime between any number and its double (Pafnuty Chebyshev, around 1850).',
         'There is always a prime between two consecutive cubes, but this has only been proved for very large numbers.'],
  why='The gap from one square to the next keeps growing, which should make primes easier to find there. But primes also have long gaps between them, and no one has proved the prime gaps never outgrow the gaps between squares.',
  classroom=['Have students draw the strips on graph paper, one per row, and count the primes in each.',
             'Ask: How long is the strip that starts at 5 × 5? At 6 × 6? Can you predict any strip’s length? (It’s always one more than twice the number being squared.)',
             'Ask: Which strip has the fewest primes so far? Could a strip ever have none?'],
  words=[('Perfect square', 'a whole number times itself, like 1, 4, 9, 16'), ('Consecutive', 'one right after another')]),
 'gilbreath': dict(
  tryit=['Primes: 2, 3, 5, 7, 11, 13, 17…', 'Differences: 1, 2, 2, 4, 2, 4…', 'Next row: 1, 0, 2, 2, 2…', 'Next row: 1, 2, 0, 0…'],
  known=['Norman Gilbreath noticed it in 1958 while doodling on a napkin. François Proth had claimed a proof in 1878, but it was flawed.',
         'Andrew Odlyzko checked it in 1993 for the first 340 billion primes.',
         'Some mathematicians suspect it has less to do with primes than with any list that starts with 2, keeps growing, and has small, irregular gaps.'],
  why='The pattern depends on the gaps between primes staying fairly small and irregular. Proving that takes more knowledge about prime gaps than anyone currently has.',
  classroom=['Build the triangle together on the board. It needs only subtraction, so every student can contribute a number.',
             'Ask: Why do the rows fill up with 0s and 2s? What does a row of 0s and 2s turn into?',
             'Try a different starting list, like 1, 2, 4, 8, 16, or the class’s birthdays in order. Does “always 1” survive? That tests whether the primes matter.'],
  words=[('Difference', 'the larger number minus the smaller'), ('Neighbors', 'numbers next to each other in the list')]),
 '196': dict(
  tryit=['57 + 75 = 132', '132 + 231 = 363 (done in 2 steps)', '89 takes 24 steps, ending at 8,813,200,023,188', '196 → 887 → 1,675 → 7,436 → …'],
  known=['Computers have followed 196 for hundreds of millions of digits without finding a palindrome.',
         'A number that never reaches a palindrome is called a Lychrel number. No one has proved that one exists in our base-ten system.',
         'In some other number systems, like binary, certain numbers have been proved to never reach a palindrome.'],
  why='Each step makes the number longer, and carrying scrambles the digits in hard-to-predict ways. There’s no known way to know what happens at step one billion without doing the first billion steps.',
  classroom=['Give each group a range of starting numbers (10–29, 30–49…). Pool the results: which are fast, which are slow, which seem stuck?',
             'Ask: Which two-digit numbers finish in one step? Why those? (Add the two digits.)',
             'Ask: 89 and 98 take the same number of steps. Why?'],
  words=[('Palindrome', 'a number that reads the same both ways, like 363'), ('Reverse', 'write the digits in the opposite order')]),
 'erdos-straus': dict(
  tryit=['4/5 = 1/2 + 1/4 + 1/20', '4/7 = 1/2 + 1/15 + 1/210', '4/6 = 1/2 + 1/7 + 1/42'],
  known=['Paul Erdős and Ernst Straus proposed it in 1948.',
         'It has been checked by computer for every denominator up to a hundred million billion (10¹⁷).',
         'Writing fractions as sums of unit fractions is ancient. Egyptian scribes did it around 1650 BCE, so these are called Egyptian fractions.'],
  why='Mathematicians have methods that work for most denominators, including every even one. But a few stubborn families of numbers aren’t covered by any known method, and no one has found one approach that always works.',
  classroom=['Try the greedy method: take away the biggest unit fraction that fits, then repeat. Try 4/5, then 4/13. When does it need more than three pieces?',
             'Ask: If you can split 4/5, can you split 4/10 for free? (Double every bottom number.)',
             'Use fraction strips so students can see the pieces fit exactly.'],
  words=[('Unit fraction', 'a fraction with 1 on top, like 1/2 or 1/20'), ('Denominator', 'the bottom number of a fraction')]),
 'odd-perfect': dict(
  tryit=['6: 1 + 2 + 3 = 6 (perfect)', '28: 1 + 2 + 4 + 7 + 14 = 28 (perfect)', '12: 1 + 2 + 3 + 4 + 6 = 16 (abundant)', '15: 1 + 3 + 5 = 9 (deficient)'],
  known=['Euclid, around 300 BCE, found a recipe that makes even perfect numbers. Leonhard Euler later proved every even perfect number comes from that recipe.',
         'About fifty perfect numbers are known. Every one is even.',
         'No odd perfect number exists below 10¹⁵⁰⁰, a 1 followed by 1,500 zeros. Any odd one would need many different prime factors.'],
  why='Odd numbers usually fall short, since their factors are spread thin, but not always: 945 is the smallest odd number whose factors add to more than itself. So odd numbers can pass their own value, and no one can rule out one landing exactly on it.',
  classroom=['Sort 1 through 30 into deficient, perfect, and abundant. What do the abundant numbers have in common?',
             'Ask: Are there odd abundant numbers? (Yes, but the first is 945. A great surprise for students who conjecture “never.”)',
             'Ask: What happens with 8, 16, 32? (Their factors always add to one less.)'],
  words=[('Factor', 'a number that divides evenly into another'), ('Abundant / deficient', 'factors add to more than / less than the number')]),
 'lonely-runner': dict(
  tryit=['2 runners: “far” means half a lap', '3 runners: a third of a lap', '4 runners: a quarter of a lap', 'Speeds 1, 2, 4 laps a minute: at 30 seconds, A is lonely'],
  known=['It was first posed in the late 1960s and 1970s, in the study of how lines of sight get blocked, and later renamed the lonely runner conjecture.',
         'It has been proved for up to seven runners (2008).',
         'The distance can’t be made any bigger: some speeds make runners exactly that far apart and no farther.'],
  why='Each new runner adds another speed that can get in the way, and the ways runners bunch up get complicated fast. The methods that work for seven runners don’t stretch to every number of runners.',
  classroom=['Act it out: three students walk a circle at one, two, and four steps per clap. Freeze! Who’s lonely?',
             'Connect to rates: where is each runner after half a minute? A third of a minute? It’s fractions of a lap in disguise.',
             'Ask: With two runners, when are they farthest apart? Can you predict it from their speeds?'],
  words=[('Lap', 'one full trip around the track'), ('Rate', 'distance per unit of time, like laps per minute')]),
}

SHORT = {'gilbreath': '', 'odd-perfect': ''}

CSS = """
@page { size: letter; margin: 0.5in 0.55in; }
:root { --ink:#1d232b; --muted:#5b6570; --rule:#e3e6ea; --accent:#4f46e5; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Source Sans 3", "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: var(--ink); font-size: 10.2pt; line-height: 1.36; }
a { color: var(--accent); text-decoration: none; font-weight: 600; }
header { display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; border-bottom: 2px solid var(--ink); padding-bottom: 7px; margin-bottom: 10px; }
h1 { white-space: nowrap; font-size: 21pt; letter-spacing: -0.3px; line-height: 1.1; }
.tag { font-size: 8.4pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--c); margin-bottom: 2px; }
.meta { text-align: right; font-size: 8.6pt; color: var(--muted); line-height: 1.5; white-space: nowrap; }
.claim { font-size: 12.5pt; font-weight: 600; border-left: 4px solid var(--c); padding: 3px 0 3px 12px; margin-bottom: 10px; }
.top { margin-bottom: 12px; break-inside: avoid; }
figure svg { max-height: 2.75in; margin: 0 auto; }
.try { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
figure { border: 1px solid var(--rule); border-radius: 8px; padding: 6px; }
figure svg { width: 100%; height: auto; display: block; }
figcaption { font-size: 8.4pt; color: var(--muted); margin-top: 4px; }
h2 { font-size: 8.6pt; text-transform: uppercase; letter-spacing: 1.2px; color: var(--muted); margin-bottom: 5px; break-after: avoid; }
.try li { list-style: none; background: #f5f7ff; border-radius: 999px; padding: 3px 11px; font-weight: 600; font-variant-numeric: tabular-nums; }
.sec { margin-bottom: 9px; break-inside: avoid; }
.sec ul { padding-left: 16px; color: #333b44; }
.sec li { margin-bottom: 3px; }
.why { background: #f5f7ff; border-left: 3px solid var(--accent); border-radius: 0 6px 6px 0; padding: 7px 11px; color: #333b44; }
.class { background: #fff7ed; border-left: 3px solid #f97316; border-radius: 0 6px 6px 0; padding: 7px 11px; }
.class ul { padding-left: 16px; color: #333b44; }
.words { display: grid; grid-template-columns: max-content 1fr; gap: 2px 12px; color: #333b44; }
.words b { color: var(--ink); }
footer { margin-top: 8px; font-size: 8.2pt; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 5px; }
"""

def html_for(p, d):
    h = f'<!doctype html><html><head><meta charset="utf-8"><title>{escape(p["name"])}</title><style>{CSS}</style></head><body style="--c:{p["color"]}">'
    h += f'<header><div><div class="tag">{escape(p["tag"])} · Unsolved</div><h1>{escape(p["name"])}</h1></div>'
    h += '<div class="meta">Open Problems for Middle School<br>TCE 412M · Todd Edwards</div></header>'
    h += f'<p class="claim">{escape(p["claim"])}</p>'
    h += f'<div class="top"><figure style="{SHORT.get(p["slug"], "")}">{p["pic"].replace("<svg ", "<svg style=\"max-height:2.2in\" ", 1) if p["slug"] in SHORT else p["pic"]}<figcaption>{escape(p["caption"])}</figcaption></figure>'
    h += '<h2 style="margin-top:10px">Try it</h2><ul class="try">' + ''.join(f'<li>{escape(t)}</li>' for t in d['tryit']) + '</ul></div>'
    h += '<div class="sec"><h2>What mathematicians know</h2><ul>' + ''.join(f'<li>{escape(t)}</li>' for t in d['known']) + '</ul></div>'
    h += f'<div class="sec"><h2>Why it’s still unsolved</h2><p class="why">{escape(d["why"])}</p></div>'
    h += '<div class="sec class"><h2>Try this with students</h2><ul>' + ''.join(f'<li>{escape(t)}</li>' for t in d['classroom']) + '</ul></div>'
    h += '<div class="sec"><h2>Words to know</h2><div class="words">' + ''.join(f'<b>{escape(a)}</b><span>{escape(b)}</span>' for a, b in d['words']) + '</div></div>'
    h += f'<footer>Online, with the other seven problems: <a href="{SITE}{p["slug"]}.html">{SITE.replace("https://", "")}{p["slug"]}.html</a> · The picture was computed from the real numbers.</footer></body></html>'
    return h

pages = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium-browser'); pg = b.new_page()
    for p in PROBLEMS:
        tmp = os.path.join(HERE, f'detail-{p["slug"]}.html')
        open(tmp, 'w').write(html_for(p, DETAIL[p['slug']]))
        pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle')
        out = os.path.join(PDF_DIR, f'{p["slug"]}.pdf')
        pg.pdf(path=out, format='Letter', print_background=True, prefer_css_page_size=True)
        pages[p['slug']] = out
    b.close()
import subprocess
for s, f in pages.items():
    n = subprocess.run(['pdfinfo', f], capture_output=True, text=True).stdout
    print(s, [l for l in n.splitlines() if l.startswith('Pages')])
