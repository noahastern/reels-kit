# Cutting raw footage

The raw footage is never touched. The cut is written to
`project/cut-tight.mov`.

## Cut on the waveform, not the transcript

Transcript word times are only roughly right. After a pause, start times can
be 0.4s early, and end times often run on into the silence. Use the
transcript to find and name each sentence. Every cut point comes from the
waveform: `scripts/plan_cut.py` finds islands of sound and puts each in-point
at the start of the first word's island and each out-point at the end of the
last word's.

## Picking takes

When a line is said more than once, compare the takes:
- Is the sentence complete? Does it stop mid-word or trail off ("um")?
- Does it have every word that matters (a keyword, "next", a number)?
- Is there a stumble or restart?
- Which delivery is strongest?

When two are close, keep the last one; people redo a line until it's right.
**The best take is often half of each:** the first take has the right words,
a later one finishes cleanly. Splice them mid-sentence at a comma, where
there's a natural dip.

## Edges

- **Inhales:** a quick breath before a restart has hiss but hardly any voice.
  Drop it, or it doubles into the next take.
- **Plosives:** a "k", "t" or "p" before a word ("Claude") also looks like
  hiss. Keep about 40ms of it.
- **Fades:** a word's fade can run 200ms. How much of it to keep is taste.
  Snappy creators cut as the last word fades; others leave a breath. If the
  creator has a finished cut of their own, match its gaps. Otherwise ask
  "snappy or breathing?" once and write the answer into their `CLAUDE.md`.
- **Dead space** between sentences comes down to that same gap. Leave pauses
  they use for emphasis.

## Mechanics

- Whole frames only, the cut on a frame boundary inside the quiet, a 4ms fade
  on each side of every join.
- Re-encode with `libx264 -crf 12 -g 30 -keyint_min 30 -pix_fmt yuv420p` (a
  keyframe every second so HyperFrames can seek, 8-bit so the browser can
  decode it) and keep the audio as PCM.
- Map the transcript to the cut (`transcript-tight.json`), fixing words whose
  start fell on the wrong side of a cut.

## Checks, at every join

- The audio of each shot is identical to the raw, with 0 samples of lag.
- The first frame of each shot is its source frame.
- No click: the biggest sample step at the join is no bigger than nearby
  speech.
- No word clipped at either end: look at the level 50ms either side.
- The flow check: transcribe the cut fresh and read it. Nothing doubled,
  nothing missing.

## Using the scripts

```bash
# picks.json: [{"from": <first word index>, "to": <last word index>, "why": "..."}]
python3 <plugin>/scripts/plan_cut.py transcript.json voice.wav cut/picks.json cut/shots.json --fps 30000/1001
python3 <plugin>/scripts/render_cut.py <raw clip> cut-tight.mov cut/shots.json
python3 <plugin>/scripts/make_board.py cut/shots.json cut/notes.json <raw clip> ../storyboard/board.html --brand ../../../brand/brand.css
```

`plan_cut.py` prints a map of each join (`#` voice, `+` soft voice, `s` hiss,
`.` quiet, `|` the cut). Read it. If a join looks wrong, change that shot's
frames in `shots.json` by hand.
