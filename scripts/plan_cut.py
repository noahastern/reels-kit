"""Turn (first word, last word) picks into frame-accurate cut points found on the waveform.

The transcript only says roughly where each word is. The cut points come from
islands of sound on the waveform: an in-point is the start of the island the
first word begins in, an out-point the end of the island the last word is in.
When the speech runs straight through (a splice mid-sentence), the cut goes in
the quietest dip between the two words instead.

Usage:
    python3 plan_cut.py transcript.json voice.wav picks.json shots.json --fps 30000/1001 [--tail 0.01]

picks.json is a list of {"from": first word index, "to": last word index, "why": "..."}.
--tail is how much fade to keep after the last clear sound of a shot: 0.01 is snappy
(cut as the word fades), 0.12 leaves a breath.
"""
import argparse, json, math, os, sys
from fractions import Fraction
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_level import Voice, HOP

ap = argparse.ArgumentParser()
ap.add_argument('transcript'); ap.add_argument('voice'); ap.add_argument('picks'); ap.add_argument('shots')
ap.add_argument('--fps', default='30000/1001')
ap.add_argument('--tail', type=float, default=0.010)
args = ap.parse_args()

FPS = float(Fraction(args.fps))
PRE = 0.020        # lead-in before the first sound of a shot
POST = args.tail   # tail after the last clear sound

words = json.load(open(args.transcript, encoding='utf-8'))
v = Voice(args.voice)
picks = json.load(open(args.picks, encoding='utf-8'))

def islands_at(strict_full=18, strict_high=14, soft_full=8, soft_high=6, merge=0.12, lead=0.04, tail=0.08):
    """Islands of clear voice, merged across short gaps, then grown into soft edges (s, f, breathy ends)."""
    strict = (v.full > v.floor + strict_full) | (v.high > v.hfloor + strict_high)
    soft = (v.full > v.floor + soft_full) | (v.high > v.hfloor + soft_high)
    out = []
    i = 0
    while i < len(strict):
        if strict[i]:
            j = i
            while j < len(strict) and strict[j]:
                j += 1
            if out and i - out[-1][1] < merge / HOP:
                out[-1][1] = j
            else:
                out.append([i, j])
            i = j
        else:
            i += 1
    res = []
    for a, b in out:
        if b - a < 0.04 / HOP:
            continue
        g = int(lead / HOP)
        while a > 0 and soft[a - 1] and g > 0:
            a -= 1; g -= 1
        g = int(tail / HOP)
        while b < len(soft) and soft[b] and g > 0:
            b += 1; g -= 1
        # hiss with no voice under it at an edge is a breath, not a word: keep only a consonant's worth
        body = v.full > v.floor + 12
        a0, b0 = a, b
        while a < b and not body[a]:
            a += 1
        while b > a and not body[b - 1]:
            b -= 1
        a = max(a0, a - int(lead / HOP))
        b = min(b0, b + int(0.03 / HOP))
        res.append((a * HOP, b * HOP))
    return res


islands = islands_at()


def island_of(w):
    """The island a word is in. Transcript times drift, so pick the island overlapping it most, else the nearest."""
    s, e = w['start'], max(w['end'], w['start'] + 0.08)
    best = max(islands, key=lambda ab: min(e, ab[1]) - max(s, ab[0]))
    if min(e, best[1]) - max(s, best[0]) > 0:
        return best
    return min(islands, key=lambda ab: min(abs(ab[0] - s), abs(ab[1] - e)))


def dip(t0, t1):
    return v.quietest(t0, t1)


def in_point(wi):
    isl = island_of(words[wi])
    if wi > 0 and island_of(words[wi - 1]) == isl:  # running speech: splice in the dip before this word
        ws = words[wi]['start']
        return dip(ws - 0.15, ws + 0.05), 'dip'
    return isl[0] - PRE, 'onset'


def out_point(wi):
    isl = island_of(words[wi])
    if wi + 1 < len(words) and island_of(words[wi + 1]) == isl:
        ns = words[wi + 1]['start']
        return dip(ns - 0.15, ns + 0.05), 'dip'
    return isl[1] + POST, 'offset'


def pieces(t0, t1, gap=0.05, loud=False):
    """Runs of sound between t0 and t1, split wherever it goes quiet for `gap` or longer.
    loud=True counts only clear voice, so a word's long soft fade isn't kept."""
    m = 15 if loud else 12
    snd = [(v.full[i] > v.floor + m) or (v.high[i] > v.hfloor + 10) for i in range(v.t2i(t0), v.t2i(t1))]
    out, s, q = [], None, 0
    for k, x in enumerate(snd):
        if x:
            if s is None:
                s = k
            q = 0
            e = k + 1
        elif s is not None:
            q += 1
            if q * HOP >= gap:
                out.append((t0 + s * HOP, t0 + e * HOP)); s = None
    if s is not None:
        out.append((t0 + s * HOP, t0 + e * HOP))
    return out


def breath(t0, t1):
    """A short run with hiss but hardly any voice under it."""
    return t1 - t0 < 0.3 and v.level(t0, t1) < v.floor + 16


def clean_out(t, kind):
    """Drop a short fragment after the last word (a breath, a lip smack, the first hum of the next take)."""
    if kind != 'offset':
        return t
    ps = pieces(t - 0.5, t, loud=True)
    while len(ps) > 1 and (ps[-1][1] - ps[-1][0] < 0.10 or breath(*ps[-1])):
        ps.pop()
    return ps[-1][1] + POST if ps else t


def clean_in(t, kind):
    if kind != 'onset':
        return t
    ps = pieces(t, t + 0.5, gap=0.08)
    while len(ps) > 1 and (ps[0][1] - ps[0][0] < 0.08 or breath(*ps[0])):
        ps.pop(0)
    if not ps:
        return t
    # an inhale right before the first word: keep at most a plosive's worth (k, t, p) of hiss
    i = v.t2i(ps[0][0])
    while i < v.t2i(ps[0][1]) and v.full[i] <= v.floor + 12:
        i += 1
    return max(ps[0][0], i * HOP - 0.04) - PRE


shots = []
for p in picks:
    a, ka = in_point(p['from'])
    b, kb = out_point(p['to'])
    a, b = clean_in(a, ka), clean_out(b, kb)
    fa = math.floor(a * FPS + 1e-6) if ka == 'onset' else round(a * FPS)
    fb = round(b * FPS)
    text = ' '.join(w['text'] for w in words[p['from']:p['to'] + 1])
    shots.append(dict(src_in=fa, src_out=fb, kind_in=ka, kind_out=kb, text=text, why=p.get('why', ''),
                      first=p['from'], last=p['to']))

json.dump(shots, open(args.shots, 'w', encoding='utf-8'), indent=1)


def row(t):
    s = ''
    for d in range(-200, 201, 20):
        i = v.t2i(t + d / 1000)
        f = v.full[i] - v.floor
        h = v.high[i] - v.hfloor
        s += ('|' if d == 0 else '') + ('#' if f > 20 else '+' if f > 12 else ('s' if h > 10 else '.'))
    return s


total = 0
for k, s in enumerate(shots):
    n = s['src_out'] - s['src_in']
    print(f"shot {k+1}: frames {s['src_in']}-{s['src_out']} ({n} fr, {n/FPS:.2f}s) in:{s['kind_in']} out:{s['kind_out']}")
    print(f"   in  {row(s['src_in']/FPS)}")
    print(f"   out {row(s['src_out']/FPS)}")
    print(f"   {s['text']}")
    total += n
print(f'total {total} frames, {total/FPS:.2f}s')
