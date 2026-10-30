# Sound

## The palette

Every graphic gets a subtle sound, 12–24dB under the voice. The creator's
`sounds/catalog.md` says which file plays each role.

| Role | When |
|---|---|
| typing | under typed text, for as long as it types |
| pop | something appears |
| whoosh | movement; start it early by its build-up so the peak lands on the move |
| paper slide | a box opens |
| ping | a payoff, a number landing |
| click | a click on screen |
| error | a "no", something crossed out |

Check each new sound's onset and level before using it: trim silence at the
head, and note its peak so the volume in `sounds.json` is right.

## sounds.json

Every sound in a video lives in `project/sounds.json`:

```json
{
  "voice": "voice.wav",
  "sfx": [
    {"id": "hook-pop", "file": "assets/sfx/pop.wav", "at": 0.0, "ms": 0, "dur": 0.4, "vol": 0.05, "note": "hook text on frame 0"}
  ],
  "music": {"file": "assets/music/track.wav", "ms": 0, "vol": 0.09, "fade_out": 1.5}
}
```

`at` is when it starts on the video's timeline, `ms` where in the file it
starts, `dur` how much plays (with a 40ms fade out), `vol` linear gain.
Optional `music.dip`: `{"at", "down", "back", "up", "db"}` dips the bed under
a moment and brings it back.

`scripts/make_mix.py` builds both deliveries from it. Write every delay out
literally in a filter graph (`adelay=7074|7074`), never through a shell
variable: zsh reads `$at[t1]` as an array index and silently breaks the mix.

After mixing, check:
- integrated loudness and true peak (`ebur128=peak=true`)
- no more full-scale samples than the voice had
- each sound is audible at its time

## Mic clipping

When the voice hits the ceiling on a word, the clip is in the recording, and
AAC smears the flat tops so a plain declipper misses most of them. Repair
only that word:
1. `asoftclip=type=hard:threshold=0.95` to re-flatten the peaks.
2. `adeclip=arorder=16:threshold=3` to rebuild them.
3. Lower the word to match their clean takes of it (often about -5dB).
4. `highshelf=f=4500:g=-7` to take off the leftover fizz.
5. `alimiter=limit=0.891:latency=true`. `latency=true` matters: without it
   the repair lands 2ms late and smears where it blends.

Crossfade the repair in and out over 40ms into `voice-fixed.wav`. Then check:
it lines up with the original (0–1 sample lag), there are no flat-topped
runs, and everything outside the window is bit-identical. Tell the creator
which words were affected.

## Music

Light, instrumental, about 15dB under the voice. Only tracks the creator has a
license for. Pick one and list two alternatives in the review.
