"""Turn the claude.ai deck's slide files into a public slideshow in applet-library."""
import json, os, re, shutil

S = '/tmp/claude-1000/-home-todd/809f938d-556a-45ed-8ce6-e49de72764ae/scratchpad'
SRC = os.path.join(S, 'artifact-files/3e4f7dcf-7f40-4911-8566-b7cdd630c7e1/project')
OUT = os.path.expanduser('~/Repos/applet-library/tce412-routines-conjecturing')
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'handouts'), exist_ok=True)

BLOBS = {
    'dea984ffe2b874b1e64496558997f523': ('gs-act1.jpg', 'gs-act1.jpg'),
    '4993e329d18671e387ef3ae41d17bf7d': ('gs-info.jpg', 'gs-info.jpg'),
    'e2bcc87d35320a7d538c551e6721098a': ('slidepics/goldbach.png', 'goldbach.png'),
    'fa21dc5d9f7c3c06c2c2c1b3f10e7cd7': ('slidepics/twin-primes.png', 'twin-primes.png'),
    '56fc0787f4b30c493e4bc8809e0354b3': ('slidepics/legendre.png', 'legendre.png'),
    'ea369994cde6c36052a92f8eb18a4a6f': ('slidepics/gilbreath.png', 'gilbreath.png'),
    '5de85ec8c2f9f04b1b056da6b2e873a5': ('slidepics/196.png', '196.png'),
    '45fe414d065924b0cea607e711165765': ('slidepics/erdos-straus.png', 'erdos-straus.png'),
    '09ef38674b241cce0bfea53254a21002': ('slidepics/odd-perfect.png', 'odd-perfect.png'),
    '85db1e695648d7214e5f8ec9cd4e8910': ('slidepics/lonely-runner.png', 'lonely-runner.png'),
    '9fcd1d2aea5174f27a92b61be9226683': ('loops-qr.png', 'loops-qr.png'),
}
for src, dst in BLOBS.values():
    shutil.copy(os.path.join(S, src), os.path.join(OUT, 'img', dst))

deck = json.load(open(os.path.join(SRC, 'deck.json')))
slides = []
for sid in deck['order']:
    h = open(os.path.join(SRC, 'slides', f'{sid}.html')).read().strip()
    h = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: 'img/' + BLOBS[m.group(1)][1], h)
    assert '/_blob/' not in h, sid
    # every link opens in a new tab so the slideshow stays put
    h = h.replace('<a href=', '<a target="_blank" rel="noopener" href=')
    slides.append(h)

PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Routines &amp; Conjecturing · TCE 412M</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="__FONTS__" rel="stylesheet">
<style>
html,body{margin:0;height:100%;background:#0F0D2E;overflow:hidden;font-family:'Nunito Sans',Arial,sans-serif}
#stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}
.slide{position:absolute;inset:0}
.slide[hidden]{display:none}
.slide>section{position:absolute;inset:0;box-sizing:border-box;width:1920px;height:1080px;overflow:hidden}
.slide *{box-sizing:border-box;margin:0}
.slide h1{font-size:96px;font-weight:600;line-height:1.1}
.slide h2{font-size:64px;font-weight:600;line-height:1.15}
.slide h3{font-size:44px;font-weight:600;line-height:1.2}
.slide p{font-size:32px;line-height:1.4}
.slide a{color:inherit}
.slide hr{border:0;width:100%}
.slide aside{display:none}
#bar{position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;align-items:center;gap:14px;padding:8px;
  font:14px 'Nunito Sans',Arial,sans-serif;color:#C7D2FE;opacity:0;transition:opacity .25s}
body:hover #bar,#bar:focus-within{opacity:1}
#bar button{background:#312E81;color:#fff;border:0;border-radius:999px;padding:6px 14px;font:inherit;cursor:pointer}
#notes{position:fixed;left:16px;right:16px;bottom:52px;max-height:34vh;overflow:auto;background:rgba(15,13,46,.94);color:#E0E7FF;
  border:1px solid #4F46E5;border-radius:12px;padding:14px 18px;font:17px/1.5 'Nunito Sans',Arial,sans-serif;display:none}
body.show-notes #notes{display:block}
</style></head><body>
<div id="stage">
__SLIDES__
</div>
<div id="notes"></div>
<nav id="bar"><button id="prev" aria-label="Previous slide">←</button><span id="count"></span><button id="next" aria-label="Next slide">→</button>
<button id="nbtn">Notes (N)</button><button id="fs">Full screen (F)</button>
<a href="handouts/" style="color:#FDBA74">Handouts</a></nav>
<script>
const slides=[...document.querySelectorAll('.slide')], stage=document.getElementById('stage');
let i=0;
function fit(){const s=Math.min(innerWidth/1920,innerHeight/1080);stage.style.transform=`scale(${s}) translate(-50%,-50%)`;}
function show(n){i=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,k)=>s.hidden=k!==i);
  document.getElementById('count').textContent=`${i+1} / ${slides.length}`;
  const a=slides[i].querySelector('aside');document.getElementById('notes').textContent=a?a.textContent:'(No notes for this slide.)';
  history.replaceState(null,'','#'+(i+1));}
addEventListener('resize',fit);
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(i+1)}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(i-1)}
  else if(e.key==='Home')show(0); else if(e.key==='End')show(slides.length-1);
  else if(e.key==='n'||e.key==='N')document.body.classList.toggle('show-notes');
  else if(e.key==='f'||e.key==='F')toggleFs();});
function toggleFs(){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}
document.getElementById('prev').onclick=()=>show(i-1);document.getElementById('next').onclick=()=>show(i+1);
document.getElementById('nbtn').onclick=()=>document.body.classList.toggle('show-notes');document.getElementById('fs').onclick=toggleFs;
stage.addEventListener('click',e=>{if(e.target.closest('a'))return;show(e.clientX>innerWidth/2?i+1:i-1)});
let tx=null;addEventListener('touchstart',e=>tx=e.touches[0].clientX);addEventListener('touchend',e=>{if(tx===null)return;const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(d<0?i+1:i-1);tx=null});
fit();show((parseInt(location.hash.slice(1))||1)-1);
</script></body></html>
'''
fonts = deck['faces']['rubik']['href']
html = PAGE.replace('__FONTS__', fonts).replace('__SLIDES__', '\n'.join(f'<div class="slide" hidden>{s}</div>' for s in slides))
open(os.path.join(OUT, 'index.html'), 'w').write(html)

HANDOUTS = [('TCE412-Math-Routines-Field-Guide.pdf', 'Math Routines Field Guide', 'Four routines from the reading, more to explore, nVoke, and the moves that make any routine work.'),
            ('TCE412-Orbit-Explorer-Task.pdf', 'Conjecturing with Orbit Explorer', 'The task card: 3n − 1 by hand, then bigger numbers in the applet, then a conjecture.'),
            ('TCE412-Open-Problems-for-Middle-School.pdf', 'Open Problems for Middle School', 'Eight unsolved problems your students can try, each linked to its own page.')]
for f, _, _ in HANDOUTS:
    shutil.copy(os.path.expanduser(f'~/Documents/{f}'), os.path.join(OUT, 'handouts', f))
cards = ''.join(f'<a class="card" href="{f}"><b>{t}</b><span>{d}</span></a>' for f, t, d in HANDOUTS)
open(os.path.join(OUT, 'handouts', 'index.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Handouts · Routines &amp; Conjecturing</title>
<link href="{fonts}" rel="stylesheet">
<style>body{{margin:0;background:#FAFAF7;color:#1E1B4B;font:18px/1.5 'Nunito Sans',Arial,sans-serif}}
.stripe{{height:6px;background:linear-gradient(90deg,#EF4444,#F97316,#EAB308,#22C55E,#3B82F6,#8B5CF6)}}
.wrap{{max-width:820px;margin:0 auto;padding:32px 18px}} h1{{font-family:Rubik,Arial,sans-serif;font-size:38px;margin:0 0 6px}}
p{{color:#4A4870;margin:0 0 22px}} a{{color:#4F46E5;font-weight:700;text-decoration:none}}
.card{{display:block;background:#fff;border-left:6px solid #4F46E5;border-radius:0 12px 12px 0;padding:16px 20px;margin-bottom:14px;color:#1E1B4B;font-weight:400;box-shadow:0 4px 14px rgba(30,27,75,.06)}}
.card b{{display:block;font-family:Rubik,Arial,sans-serif;font-size:21px;margin-bottom:4px}} .card span{{color:#4A4870}}</style></head>
<body><div class="stripe"></div><div class="wrap"><h1>Routines &amp; Conjecturing: handouts</h1>
<p>TCE 412M guest session, Tuesday 29 September 2026 · <a href="../">Back to the slides</a></p>{cards}
<p style="margin-top:22px">Reading: Newell &amp; Orton (2018), <a href="https://www.jstor.org/stable/10.5951/teacchilmath.25.2.0094">“Classroom Routines: An Invitation for Discourse”</a>, <i>Teaching Children Mathematics</i> 25(2), 94–102.<br>
More open problems: <a href="../open-problems/">applet-library/open-problems</a></p></div></body></html>''')
print('slides:', len(slides), '->', OUT)
