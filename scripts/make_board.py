"""The shot-by-shot board: one card per shot with its first and last frame, words, take, join,
light and planned graphic, then everything that was dropped. One self-contained HTML file.

    python3 make_board.py shots.json notes.json <raw clip> storyboard/board.html [--title "..."] [--brand brand.css]

With --brand, the board takes the creator's accent, box and ink colors from their brand.css.

notes.json:
    {"shots": [{"take": "...", "join": "...", "light": "...", "on_screen": "...",
                "on_screen_still": "path/to/snapshot.png"}, ...],
     "dropped": [{"at": "0:17.8-0:21.6", "what": "..."}, ...]}
Every field is optional.
"""
import argparse, base64, html, json, os, re, subprocess, tempfile
from fractions import Fraction

ap = argparse.ArgumentParser()
ap.add_argument('shots'); ap.add_argument('notes'); ap.add_argument('source'); ap.add_argument('out')
ap.add_argument('--title', default='Shot-by-shot board')
ap.add_argument('--brand', help="the creator's brand.css")
args = ap.parse_args()

# neutral unless the creator's brand.css says otherwise
light = {'bg': '#f6f6f4', 'ink': '#1c1c1c', 'muted': '#6a6a6a', 'line': '#e2e2df', 'accent': '#1c1c1c', 'card': '#fff'}
dark = {'bg': '#1c1c1c', 'ink': '#f2f2f0', 'muted': '#a0a0a0', 'line': '#3a3a3a', 'accent': '#f2f2f0', 'card': '#262626'}
if args.brand:
    brand = dict(re.findall(r'--([\w-]+):\s*(#[0-9a-fA-F]{3,8})\s*;', open(args.brand, encoding='utf-8').read()))
    for key, var in (('bg', 'box-bg'), ('ink', 'ink'), ('accent', 'accent')):
        if var in brand:
            light[key] = brand[var]
    for key, var in (('bg', 'box-dark'), ('ink', 'ink-on-dark'), ('accent', 'accent')):
        if var in brand:
            dark[key] = brand[var]
css_vars = lambda c: ' '.join(f'--{k}:{v};' for k, v in c.items())

shots = json.load(open(args.shots, encoding='utf-8'))
notes = json.load(open(args.notes, encoding='utf-8'))
if isinstance(notes, list):  # a bare list of shot notes
    notes = {'shots': notes}
FPS = float(Fraction(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                                      '-of', 'default=nw=1:nk=1', args.source], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True).stdout.split()[0]))
stills = tempfile.mkdtemp()
for k, s in enumerate(shots):
    for tag, fr in (('in', s['src_in'] + 2), ('out', s['src_out'] - 3)):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{fr / FPS:.4f}', '-i', args.source, '-frames:v', '1',
                        '-vf', 'scale=360:-2', '-q:v', '4', os.path.join(stills, f's{k+1}-{tag}.jpg')], check=True)


def img(path):
    kind = 'png' if path.lower().endswith('.png') else 'jpeg'
    return f'data:image/{kind};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def tc(fr):
    return f"{fr / FPS:05.2f}"


cards, t = [], 0
for k, s in enumerate(shots):
    n = s['src_out'] - s['src_in']
    nt = (notes.get('shots') or [{}] * len(shots))[k]
    rows = ''.join(f'<dt>{label}</dt><dd>{html.escape(nt[key])}</dd>' for key, label in
                   (('take', 'Take'), ('join', 'Cut in'), ('light', 'Light'), ('on_screen', 'On screen'), ('compare', 'Note')) if nt.get(key))
    plan = f'<figure><img src="{img(nt["on_screen_still"])}" alt="Planned graphic, shot {k+1}"><figcaption>on screen</figcaption></figure>' if nt.get('on_screen_still') else ''
    cards.append(f"""
<article class="shot">
  <div class="frames">
    <figure><img src="{img(f'{stills}/s{k+1}-in.jpg')}" alt="Shot {k+1} first frame"><figcaption>first frame</figcaption></figure>
    <figure><img src="{img(f'{stills}/s{k+1}-out.jpg')}" alt="Shot {k+1} last frame"><figcaption>last frame</figcaption></figure>
    {plan}
  </div>
  <div class="meta">
    <div class="head"><span class="num">{k+1}</span><span class="time">{tc(t)}–{tc(t + n)} · {n / FPS:.2f}s</span></div>
    <p class="words">“{html.escape(s['text'])}”</p>
    <dl>{rows}</dl>
  </div>
</article>""")
    t += n

dropped = ''.join(f"<li><span class='time'>{html.escape(d['at'])}</span> {html.escape(d['what'])}</li>" for d in notes.get('dropped', []))

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(args.title)}</title>
<style>
:root {{ {css_vars(light)} }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ {css_vars(dark)} }} }}
:root[data-theme="dark"] {{ {css_vars(dark)} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 -apple-system, system-ui, sans-serif; }}
main {{ max-width:880px; margin:0 auto; padding:32px 16px 64px; }}
h1 {{ font-size:28px; margin:0 0 4px; }}
.sub {{ color:var(--muted); margin:0 0 28px; }}
.shot {{ display:grid; grid-template-columns:auto 1fr; gap:20px; background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; margin-bottom:16px; }}
.frames {{ display:flex; gap:8px; }}
figure {{ margin:0; }}
figure img {{ width:120px; aspect-ratio:9/16; object-fit:cover; border-radius:8px; display:block; }}
figcaption {{ font-size:12px; color:var(--muted); text-align:center; margin-top:4px; }}
.head {{ display:flex; align-items:baseline; gap:12px; }}
.num {{ font-weight:800; font-size:22px; color:var(--accent); }}
.time {{ color:var(--muted); font-variant-numeric:tabular-nums; font-size:14px; }}
.words {{ font-size:18px; font-weight:600; margin:6px 0 12px; }}
dl {{ display:grid; grid-template-columns:max-content 1fr; gap:4px 12px; margin:0; font-size:14px; }}
dt {{ color:var(--muted); }}
dd {{ margin:0; }}
h2 {{ font-size:18px; margin:32px 0 8px; }}
ul {{ padding-left:18px; }} li {{ margin-bottom:6px; }}
@media (max-width:620px) {{ .shot {{ grid-template-columns:1fr; }} figure img {{ width:100%; max-width:150px; }} }}
</style></head>
<body><main>
<h1>{html.escape(args.title)}</h1>
<p class="sub">{len(shots)} shots · {t / FPS:.2f}s</p>
{''.join(cards)}
{'<h2>What was dropped</h2><ul>' + dropped + '</ul>' if dropped else ''}
</main></body></html>"""
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
open(args.out, 'w', encoding='utf-8').write(page)
print('wrote', args.out)
