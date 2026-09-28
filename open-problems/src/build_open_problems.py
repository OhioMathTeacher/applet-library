"""Build ~/Repos/applet-library/open-problems/: an index plus one page per open problem.
Every picture is computed from real data here, so the numbers on the pages are the numbers in the math."""
import math, os
from html import escape

OUT = os.path.expanduser('~/Repos/applet-library/open-problems')
os.makedirs(OUT, exist_ok=True)

INK, MUTED, RULE = '#1E1B4B', '#4A4870', '#E3E6EA'
INDIGO, ORANGE, GREEN, GRAY = '#4F46E5', '#F97316', '#16A34A', '#9CA3AF'

def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

PRIMES = [p for p in range(2, 4000) if isprime(p)]

def svg(w, h, label, body):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="Nunito Sans, Arial, sans-serif">{body}</svg>')

def text(x, y, s, size=14, fill=MUTED, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'

# ---------- pictures ----------

def pic_goldbach():
    W, H, L, B, T, R = 720, 400, 60, 50, 20, 20
    N = 3000
    pts = [(n, sum(1 for p in PRIMES if p <= n - p and isprime(n - p))) for n in range(4, N + 1, 2)]
    ymax = max(c for _, c in pts) + 5
    sx = lambda n: L + (n / N) * (W - L - R)
    sy = lambda c: H - B - (c / ymax) * (H - B - T)
    body = f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>'
    for c in range(0, ymax + 1, 20):
        body += f'<line x1="{L}" x2="{W-R}" y1="{sy(c):.1f}" y2="{sy(c):.1f}" stroke="{RULE}"/>' + text(L - 8, sy(c) + 4, c, 12, anchor='end')
    for n in range(0, N + 1, 500):
        body += text(sx(n), H - B + 18, f'{n:,}', 12)
    for n, c in pts:
        col = ORANGE if n % 3 == 0 else INDIGO
        body += f'<circle cx="{sx(n):.1f}" cy="{sy(c):.1f}" r="1.6" fill="{col}" fill-opacity="0.75"/>'
    body += text((L + W - R) / 2, H - 10, 'Even number', 13, INK, weight=700)
    body += f'<text transform="translate(16 {(T + H - B) / 2}) rotate(-90)" font-size="13" fill="{INK}" text-anchor="middle" font-weight="700">Ways to write it as prime + prime</text>'
    return svg(W, H, 'Goldbach comet: for each even number up to 3,000, the number of ways to write it as a sum of two primes. The counts grow and spread into bands; multiples of 3 form the top band.', body)

def pic_twins():
    cell, pad = 56, 10
    W = H = cell * 10 + pad * 2
    twin = set()
    for p in PRIMES:
        if p + 2 <= 100 and isprime(p + 2): twin |= {p, p + 2}
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for i in range(100):
        n = i + 1; x = pad + (i % 10) * cell; y = pad + (i // 10) * cell
        fill, col, wt = '#FFFFFF', '#9CA3AF', 400
        if isprime(n): fill, col, wt = '#E0E7FF', INK, 700
        if n in twin: fill, col, wt = ORANGE, '#FFFFFF', 700
        body += f'<rect x="{x+2}" y="{y+2}" width="{cell-4}" height="{cell-4}" rx="8" fill="{fill}" stroke="{RULE}"/>'
        body += text(x + cell / 2, y + cell / 2 + 7, n, 20, col, weight=wt)
    return svg(W, H, 'A hundred chart. Primes are shaded; primes that belong to a twin pair (3 and 5, 5 and 7, 11 and 13, 17 and 19, 29 and 31, 41 and 43, 59 and 61, 71 and 73) are orange.', body)

def pic_legendre():
    W, rowh, L, R = 720, 40, 120, 70
    rows = 10
    H = rows * rowh + 30
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for n in range(1, rows + 1):
        a, b = n * n, (n + 1) ** 2
        y = 10 + (n - 1) * rowh
        x0, x1 = L, W - R
        body += text(L - 12, y + 22, f'{a} to {b}', 14, INK, 'end', 700)
        body += f'<rect x="{x0}" y="{y+8}" width="{x1-x0}" height="20" rx="10" fill="#EEF2FF"/>'
        ps = [p for p in PRIMES if a < p < b]
        for p in ps:
            px = x0 + (p - a) / (b - a) * (x1 - x0)
            body += f'<circle cx="{px:.1f}" cy="{y+18}" r="7" fill="{ORANGE}"/>'
        body += text(W - R + 14, y + 23, f'{len(ps)} prime{"s" if len(ps) != 1 else ""}', 13, MUTED, 'start')
    return svg(W, H, 'Ten strips, each running from one perfect square to the next (1 to 4, 4 to 9, up to 100 to 121). Orange dots mark the primes in each strip. Every strip has at least two.', body)

def pic_gilbreath():
    rows = []
    r = PRIMES[:14]
    for _ in range(10):
        rows.append(r); r = [abs(r[i + 1] - r[i]) for i in range(len(r) - 1)]
    cell = 44
    W = cell * 14 + 20; H = cell * len(rows) + 20
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for ri, row in enumerate(rows):
        for ci, v in enumerate(row):
            x = 10 + ci * cell + ri * cell / 2; y = 10 + ri * cell
            if ri == 0: fill, col = INK, '#FFFFFF'
            elif ci == 0: fill, col = ORANGE, '#FFFFFF'
            elif v == 0: fill, col = '#F3F4F6', '#9CA3AF'
            else: fill, col = '#E0E7FF', INK
            body += f'<rect x="{x+2:.1f}" y="{y+2}" width="{cell-4}" height="{cell-4}" rx="7" fill="{fill}"/>'
            body += text(x + cell / 2, y + cell / 2 + 6, v, 16, col, weight=700)
    return svg(W, H, 'Gilbreath triangle. Top row: the first 14 primes. Each row below lists the differences between neighbors in the row above. The first number of every row after the top is 1 (orange).', body)

def steps196(n, cap=300):
    k = 0
    while k < cap:
        n = n + int(str(n)[::-1]); k += 1
        if str(n) == str(n)[::-1]: return k
    return None

def pic_196():
    W, H, L, B, T, R = 720, 360, 50, 46, 20, 16
    data = [(n, steps196(n)) for n in range(10, 200)]
    ymax = 26
    bw = (W - L - R) / len(data)
    sy = lambda v: H - B - v / ymax * (H - B - T)
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for v in range(0, ymax + 1, 5):
        body += f'<line x1="{L}" x2="{W-R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{RULE}"/>' + text(L - 8, sy(v) + 4, v, 12, anchor='end')
    for i, (n, s) in enumerate(data):
        x = L + i * bw
        if s is None:
            body += f'<rect x="{x:.1f}" y="{T}" width="{max(bw-0.6,1):.1f}" height="{H-B-T}" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 3"/>'
            body += text(x + bw / 2 - 30, T + 14, '196: ?', 14, '#DC2626', 'end', 700)
        else:
            col = ORANGE if s >= 20 else INDIGO
            body += f'<rect x="{x:.1f}" y="{sy(s):.1f}" width="{max(bw-0.6,1):.1f}" height="{H-B-sy(s):.1f}" fill="{col}"/>'
    for n in (10, 50, 100, 150, 199):
        body += text(L + (n - 10 + 0.5) * bw, H - B + 18, n, 12)
    body += text((L + W - R) / 2, H - 8, 'Starting number', 13, INK, weight=700)
    body += f'<text transform="translate(14 {(T + H - B) / 2}) rotate(-90)" font-size="13" fill="{INK}" text-anchor="middle" font-weight="700">Steps to a palindrome</text>'
    return svg(W, H, 'Bar chart of reverse-and-add steps to reach a palindrome for starting numbers 10 through 199. Most need only a few steps; 89 and 98 need 24 and 187 needs 23. 196 is marked with a question mark: no palindrome has ever been found.', body)

def pic_erdos():
    W, H, L, bar = 720, 250, 20, 680
    def seg(x, y, w, h, fill, label, col=INK):
        return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" fill="{fill}" stroke="#FFFFFF" stroke-width="2" rx="4"/>'
                + (text(x + w / 2, y + h / 2 + 6, label, 17, col, weight=700) if w > 30 else ''))
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    body += text(L, 26, 'One whole', 14, MUTED, 'start', 700)
    body += f'<rect x="{L}" y="36" width="{bar}" height="44" fill="none" stroke="{GRAY}" stroke-dasharray="5 4" rx="4"/>'
    for i in range(5):
        body += seg(L + i * bar / 5, 36, bar / 5, 44, INDIGO if i < 4 else '#FFFFFF', '1/5' if i < 4 else '', '#FFFFFF')
    body += text(L, 112, '4/5, as four fifths', 14, MUTED, 'start', 700)
    body += text(L, 150, '4/5, as three unit fractions', 14, MUTED, 'start', 700)
    x = L
    for d, fill in ((2, ORANGE), (4, '#FDBA74'), (20, GREEN)):
        w = bar / d
        body += seg(x, 162, w, 44, fill, f'1/{d}', '#FFFFFF' if fill != '#FDBA74' else INK)
        x += w
    body += text(x + 8, 190, '← 1/20', 14, GREEN, 'start', 700)
    body += text(L, 238, '1/2 + 1/4 + 1/20 = 10/20 + 5/20 + 1/20 = 16/20 = 4/5', 15, INK, 'start', 700)
    return svg(W, H, 'Fraction bars. Four fifths of a bar is shaded. Below it, the same length is split into one half, one fourth, and one twentieth, which add to exactly four fifths.', body)

def sdiv(n): return sum(d for d in range(1, n) if n % d == 0)

def pic_perfect():
    W, H, L, B, T, R = 720, 380, 50, 50, 20, 16
    N = 30
    data = [(n, sdiv(n)) for n in range(1, N + 1)]
    ymax = 45
    bw = (W - L - R) / N
    sy = lambda v: H - B - v / ymax * (H - B - T)
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    for v in range(0, ymax + 1, 10):
        body += f'<line x1="{L}" x2="{W-R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="{RULE}"/>' + text(L - 8, sy(v) + 4, v, 12, anchor='end')
    for i, (n, s) in enumerate(data):
        x = L + i * bw
        col = GREEN if s == n else (ORANGE if s > n else '#A5B4FC')
        body += f'<rect x="{x+3:.1f}" y="{sy(s):.1f}" width="{bw-6:.1f}" height="{H-B-sy(s):.1f}" fill="{col}" rx="3"/>'
        body += f'<line x1="{x+1:.1f}" x2="{x+bw-1:.1f}" y1="{sy(n):.1f}" y2="{sy(n):.1f}" stroke="{INK}" stroke-width="2.5"/>'
        body += text(x + bw / 2, H - B + 16, n, 11, INK if s >= n else MUTED, weight=700 if s >= n else 400)
    lx = L + 10
    for lab, col in (('Deficient: factors add to less', '#A5B4FC'), ('Abundant: factors add to more', ORANGE), ('Perfect: exactly equal', GREEN)):
        body += f'<rect x="{lx}" y="{T}" width="14" height="14" fill="{col}" rx="3"/>' + text(lx + 20, T + 12, lab, 12, INK, 'start')
        lx += 225
    body += text((L + W - R) / 2, H - 10, 'Each bar: the number’s factors (not itself) added up. Dark line: the number itself.', 12, MUTED)
    return svg(W, H, 'For 1 through 30, bars show the sum of each number’s factors (not counting itself), with a line at the number itself. 6 and 28 are perfect; 12, 18, 20, 24 and 30 are abundant; the rest are deficient.', body)

def pic_runner():
    # Three runners, speeds 1, 2, 4 laps per minute. Find a moment when the speed-1 runner is at least 1/3 lap from both others.
    t = 0.5
    pos = [t % 1, (2 * t) % 1, (4 * t) % 1]
    W, H, cx, cy, r = 720, 400, 250, 215, 140
    body = f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E0E7FF" stroke-width="26"/>'
    def xy(frac, rr=r):
        a = -math.pi / 2 + 2 * math.pi * frac
        return cx + rr * math.cos(a), cy + rr * math.sin(a)
    a0, a1 = pos[0] - 1 / 3, pos[0] + 1 / 3
    (x0, y0), (x1, y1) = xy(a0), xy(a1)
    body += f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="#FED7AA" stroke-width="26"/>'
    for (p, col, lab) in ((pos[0], ORANGE, 'A'), (pos[1] - 0.035, INDIGO, 'B'), (pos[2] + 0.035, GREEN, 'C')):
        x, y = xy(p)
        body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>' + text(x, y + 6, lab, 16, '#FFFFFF', weight=700)
    body += text(cx, cy - r - 36, 'B and C, both at the start', 13, INK, weight=700)
    body += text(cx, cy - 6, 'Start/finish at top', 13, MUTED)
    body += text(cx, cy + 14, 'Moment shown: 30 seconds', 13, MUTED)
    lx = 450
    body += text(lx, 70, 'Three runners, one track', 17, INK, 'start', 700)
    for i, (col, lab) in enumerate(((ORANGE, 'A runs 1 lap per minute'), (INDIGO, 'B runs 2 laps per minute'), (GREEN, 'C runs 4 laps per minute'))):
        body += f'<circle cx="{lx+8}" cy="{104+i*30}" r="8" fill="{col}"/>' + text(lx + 24, 109 + i * 30, lab, 14, INK, 'start')
    body += text(lx, 220, 'Shaded arc: everywhere within', 14, MUTED, 'start')
    body += text(lx, 240, 'a third of a lap of A. Here', 14, MUTED, 'start')
    body += text(lx, 260, 'B and C are both at the start,', 14, MUTED, 'start')
    body += text(lx, 280, 'outside it. A is “lonely.”', 14, MUTED, 'start')
    return svg(W, H, 'A circular track with three runners who started together at the top: A at 1 lap per minute, B at 2, C at 4. At 30 seconds, B and C are both back at the start while A is exactly half a lap away, so A is lonely.', body), t

# ---------- pages ----------

runner_svg, runner_t = pic_runner()

PROBLEMS = [
 dict(slug='goldbach', name="Goldbach's Conjecture", color='#EF4444', tag='Primes · Grades 6–8',
  claim='Every even number bigger than 2 can be made by adding two primes.',
  tryit=['10 = 3 + 7', '28 = 11 + 17', '100 works six different ways'],
  pic=pic_goldbach(),
  caption='Each dot is an even number and how many ways it splits into two primes. The count keeps growing, and never hits zero.',
  known=['Goldbach wrote it in a letter to Euler in 1742.', 'Computers have checked even numbers into the billions of billions. Every one works, but checking isn’t proving.'],
  ask=['Which even numbers can be made the most ways?', 'Why do we only ask about even numbers?']),

 dict(slug='twin-primes', name='Twin Prime Conjecture', color='#F97316', tag='Primes · Grades 6–8',
  claim='Primes that are just 2 apart, like 11 and 13, keep showing up forever.',
  tryit=['3 and 5', '17 and 19', '41 and 43'],
  pic=pic_twins(),
  caption='Primes up to 100 are shaded. Twin pairs are orange. They get rarer, but do they ever stop?',
  known=['We’ve known for over 2,000 years that primes never run out.', 'Since 2013 we know primes keep coming within 246 of each other forever. Getting that down to 2 is the unsolved part.'],
  ask=['Look at the number between each twin pair: 4, 6, 12, 18, 30… What do you notice?', 'Can three primes in a row be 2 apart, like 3, 5, 7? Ever again?']),

 dict(slug='legendre', name="Legendre's Conjecture", color='#CA8A04', tag='Primes and squares · Grades 7–9',
  claim='Between any two perfect squares that sit next to each other, there’s always a prime.',
  tryit=['Between 4 and 9: 5, 7', 'Between 16 and 25: 17, 19, 23', 'Between 100 and 121: five primes'],
  pic=pic_legendre(),
  caption='Each strip runs from one square to the next. Orange dots are primes. Every strip has at least two so far.',
  known=['In 1912 it made a famous list of four prime problems that seemed out of reach. All four are still unsolved.', 'We do know there’s always a prime between any number and its double.'],
  ask=['How long is each strip? Can you predict the next one’s length?', 'Which strip has the fewest primes? Could one ever have none?']),

 dict(slug='gilbreath', name="Gilbreath's Conjecture", color='#16A34A', tag='Primes and subtraction · Grades 5–8',
  claim='List the primes. Subtract neighbors to make a new row. Keep going. Every new row starts with 1.',
  tryit=['2, 3, 5, 7, 11…', '1, 2, 2, 4…', '1, 0, 2…'],
  pic=pic_gilbreath(),
  caption='The primes on top, then rows of differences. The first number of every row is 1, in orange.',
  known=['Norman Gilbreath noticed it in 1958, doodling on a napkin.', 'Computers have checked hundreds of billions of rows. It has never failed.'],
  ask=['Why do the rows fill up with 0s and 2s?', 'Start with a different list, like 1, 2, 4, 8, 16. Does it still work?']),

 dict(slug='196', name='The 196 Problem', color='#0D9488', tag='Addition · Grades 4–7',
  claim='Reverse a number and add. Repeat until it reads the same both ways. Does 196 ever get there?',
  tryit=['57 + 75 = 132', '132 + 231 = 363 ✓', '196 + 691 = 887…'],
  pic=pic_196(),
  caption='How many steps each starting number from 10 to 199 needs. Most need one or two. 196 has never finished.',
  known=['Computers have followed 196 for hundreds of millions of digits. Still no palindrome.', 'Nobody has proved that any number never gets there.'],
  ask=['Which two-digit numbers finish in one step? Why those?', '89 and 98 take the same number of steps. Why?']),

 dict(slug='erdos-straus', name='Erdős–Straus Conjecture', color='#2563EB', tag='Fractions · Grades 5–8',
  claim='Any fraction with 4 on top can be split into three fractions with 1 on top.',
  tryit=['4/5 = 1/2 + 1/4 + 1/20', '4/7 = 1/2 + 1/15 + 1/210'],
  pic=pic_erdos(),
  caption='Four fifths of a bar, rebuilt from a half, a fourth, and a twentieth. Same length exactly.',
  known=['Ancient Egyptians wrote fractions this way almost 4,000 years ago.', 'Computers have checked it for more numbers than there are grains of sand on Earth.'],
  ask=['Try 4/9. What’s your first move?', 'If you can split 4/5, can you split 4/10 for free?']),

 dict(slug='odd-perfect', name='Odd Perfect Numbers', color='#7C3AED', tag='Factors · Grades 5–8',
  claim='A number is perfect when its factors add up to it, like 6 = 1 + 2 + 3. Is any perfect number odd?',
  tryit=['6 = 1 + 2 + 3', '28 = 1 + 2 + 4 + 7 + 14', 'Next: 496, then 8,128'],
  pic=pic_perfect(),
  caption='Bars show each number’s factors added up. The dark line is the number itself. Only 6 and 28 match exactly.',
  known=['About fifty perfect numbers are known. Every one is even.', 'People have wondered about odd ones for more than 2,000 years.'],
  ask=['Sort 1 to 30: factors add to less, more, or exactly?', 'Can an odd number’s factors ever add to more than it? (Try 945.)']),

 dict(slug='lonely-runner', name='Lonely Runner Conjecture', color='#DB2777', tag='Rates and motion · Grades 7–10',
  claim='Runners start together on a round track, all at different speeds. Will every runner, at some moment, be far from everyone else?',
  tryit=['2 runners: far means half a lap', '3 runners: far means a third of a lap', '4 runners: a quarter'],
  pic=runner_svg,
  caption='After 30 seconds, B and C are back at the start while A is halfway around. A is lonely.',
  known=['It’s proved for up to seven runners.', 'For eight or more, nobody knows.'],
  ask=['Where is each runner after half a minute? A third of a minute?', 'Act it out: three students, three speeds. Freeze! Who’s lonely?']),
]

CSS = """
:root{--ink:#1E1B4B;--muted:#4A4870;--rule:#E3E6EA;--accent:#4F46E5;--soft:#EEF2FF;--bg:#FAFAF7;--card:#FFFFFF}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:"Nunito Sans","Segoe UI",Roboto,Arial,sans-serif;font-size:19px;line-height:1.5}
.stripe{height:6px;background:linear-gradient(90deg,#EF4444,#F97316,#EAB308,#22C55E,#3B82F6,#8B5CF6)}
.wrap{max-width:900px;margin:0 auto;padding:28px 18px 56px}
a{color:var(--accent);font-weight:700;text-decoration:none}
a:hover{text-decoration:underline}
.crumb{font-size:15px;margin-bottom:26px}
.tag{display:block;font-size:14px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:var(--c);margin-bottom:8px}
h1{font-family:Rubik,"Segoe UI",Arial,sans-serif;font-size:clamp(32px,5.5vw,52px);line-height:1.08;margin-bottom:18px}
.claim{font-family:Rubik,"Segoe UI",Arial,sans-serif;font-weight:600;font-size:clamp(22px,3.4vw,30px);line-height:1.3;border-left:8px solid var(--c);padding:4px 0 4px 20px;margin-bottom:30px}
figure{background:var(--card);border-radius:18px;padding:16px;box-shadow:0 6px 20px rgba(30,27,75,.07)}
figure svg{width:100%;height:auto;display:block}
figcaption{font-size:17px;color:var(--muted);margin-top:10px;text-align:center}
.row{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.box{background:var(--card);border-radius:16px;padding:18px 22px;box-shadow:0 4px 14px rgba(30,27,75,.05)}
h2{font-family:Rubik,"Segoe UI",Arial,sans-serif;font-size:14px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips span{background:var(--soft);border-radius:999px;padding:6px 14px;font-weight:700;font-variant-numeric:tabular-nums}
.box p{margin-bottom:8px}
.ask{margin-top:18px;background:#FFF7ED;border-left:8px solid #F97316;border-radius:0 16px 16px 0;padding:18px 22px}
.ask p{font-size:21px;font-weight:700;margin-bottom:6px}
.nav{display:flex;justify-content:space-between;gap:12px;margin-top:34px;font-size:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin-top:26px}
.card{display:block;background:var(--card);border-top:6px solid var(--c);border-radius:14px;padding:18px 20px;color:var(--ink);font-weight:400;box-shadow:0 4px 14px rgba(30,27,75,.06)}
.card:hover{text-decoration:none;box-shadow:0 8px 22px rgba(30,27,75,.12)}
.card b{display:block;font-family:Rubik,"Segoe UI",Arial,sans-serif;font-size:21px;margin-bottom:6px}
.card small{display:block;font-size:12px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:var(--c);margin-bottom:6px}
.lede{font-size:21px;color:var(--muted);max-width:700px}
.pdf{display:inline-block;margin-top:18px;background:var(--accent);color:#fff;border-radius:999px;padding:10px 20px}
.pdf:hover{text-decoration:none;opacity:.9}
footer{margin-top:44px;font-size:14px;color:var(--muted)}
@media (max-width:640px){.row{grid-template-columns:1fr}}
"""

HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,400;0,700;0,800;1,400&family=Rubik:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body><div class="stripe"></div><div class="wrap">'''

FOOT = '''<footer>Written for middle-grades teachers by Todd Edwards, Miami University. Every picture on these pages was computed from the real numbers.</footer></div></body></html>'''

def page(i, p):
    prev_p = PROBLEMS[i - 1] if i > 0 else None
    next_p = PROBLEMS[i + 1] if i + 1 < len(PROBLEMS) else None
    h = HEAD.format(title=f"{p['name']} · Open Problems")
    h += f'<div style="--c:{p["color"]}"><p class="crumb"><a href="index.html">← All eight open problems</a></p>'
    h += f'<span class="tag">{escape(p["tag"])} · Unsolved</span><h1>{escape(p["name"])}</h1>'
    h += f'<p class="claim">{escape(p["claim"])}</p>'
    h += f'<figure>{p["pic"]}<figcaption>{escape(p["caption"])}</figcaption></figure>'
    h += '<div class="row"><div class="box"><h2>Try it</h2><div class="chips">' + ''.join(f'<span>{escape(t)}</span>' for t in p['tryit']) + '</div></div>'
    h += '<div class="box"><h2>What we know</h2>' + ''.join(f'<p>{escape(t)}</p>' for t in p['known']) + '</div></div>'
    h += '<div class="ask"><h2>Ask your students</h2>' + ''.join(f'<p>{escape(t)}</p>' for t in p['ask']) + '</div>'
    h += f'<p style="margin-top:22px"><a class="pdf" href="pdf/{p["slug"]}.pdf">Detailed one-pager (PDF)</a> <span style="color:var(--muted);font-size:16px;margin-left:8px">History, why it’s unsolved, and more classroom ideas</span></p>'
    h += '<div class="nav">'
    h += f'<span>{"<a href=%s>← %s</a>" % (prev_p["slug"] + ".html", escape(prev_p["name"])) if prev_p else ""}</span>'
    h += f'<span>{"<a href=%s>%s →</a>" % (next_p["slug"] + ".html", escape(next_p["name"])) if next_p else ""}</span></div></div>'
    return h + FOOT

def index():
    h = HEAD.format(title='Open Problems for Middle School')
    h += '<h1>Open Problems for Middle School</h1>'
    h += ('<p class="lede">Eight unsolved problems that your students can understand, try by hand, and explore with technology. '
          'Nobody knows the answers, so when students gather evidence and make conjectures here, they are doing real mathematics.</p>')
    h += '<a class="pdf" href="open-problems-handout.pdf">Download the handout (PDF)</a>'
    h += '<div class="grid">'
    for p in PROBLEMS:
        h += (f'<a class="card" style="--c:{p["color"]}" href="{p["slug"]}.html"><small>{escape(p["tag"])}</small>'
              f'<b>{escape(p["name"])}</b>{escape(p["claim"])}</a>')
    h += '</div>'
    return h + FOOT

open(os.path.join(OUT, 'style.css'), 'w').write(CSS.strip() + '\n')
open(os.path.join(OUT, 'index.html'), 'w').write(index())
for i, p in enumerate(PROBLEMS):
    open(os.path.join(OUT, p['slug'] + '.html'), 'w').write(page(i, p))
print('wrote', len(PROBLEMS) + 1, 'pages to', OUT)
