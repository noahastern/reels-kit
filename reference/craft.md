# Craft defaults

Every first pass follows these without being asked. They come from dozens of
review rounds on real talking-head reels. A creator's own `CLAUDE.md` "My
defaults" and `brand/feedback.md` win over anything here.

## Safe area (1080×1920 frame)

Nothing important goes where the app's interface covers it. Check every
graphic's snapshot with the unsafe zones shaded red.

| Platform | Keep inside | Notes |
|---|---|---|
| Instagram Reels | x 60–940, y 290–1480 | The right edge only matters from y 1000 down (like/comment/share). |
| TikTok | x 60–920, y 250–1400 | The bottom UI is taller; the right column runs higher. |
| YouTube Shorts | x 60–920, y 250–1450 | |

The TikTok and Shorts numbers are approximate. If the creator can share a
screenshot of one of their posts in the app, measure from it and write the
real values into `brand/brand.css`.

- Text boxes sit on the chest, centered around (500, 1250), left of center so
  they clear the button column.
- Graphics at the top start below the safe line. Push the video in from the
  top (scale from the top edge) so the head clears them, never cut off at the
  forehead.
- No graphic covers the face, even a little.

## Timing

- A box appears about 0.5s before its first word. Never seconds ahead, and
  never sitting empty.
- Typed text types letter by letter on the spoken words. Every step of a list
  lands inside the sentence that describes it; step 1 never sits alone.
- Once the payoff is on screen, leave about 1s, then get out so captions come
  back. Long enough to read, no longer.
- Changes land on the creator's own jump cuts when one is near. Graphics cut
  out on them.
- Don't bring an old graphic back as a callback. A closing point gets its own
  callout.
- On screen means what they say. No stats, labels or filler text they don't
  say.

## Hook

- Something on screen from frame 0 that says why to stay. The news (the
  surprise, the claim, the challenge) lands within the first 5 seconds.

## Zooms

When to zoom, how far and how often is the creator's call: what they ask for
on the board, and their "My defaults". The kit never adds zooms on its own.
Whatever they choose is done right:

- **The eyes stay put across a cut.** When a zoom cuts in or out, or a move
  ends on a cut, the eyes land in the same spot on both sides. Work the offset
  out from where the eyes are on the frames either side, not by feel.
- **On the exact frame.** A zoom that changes on a cut changes on that frame.
  One or two frames off reads as a mistake. Find the jump cuts first
  (`scripts/find_jump_cuts.py`).
- **Two kinds, kept apart.** A punch-in is one scale and offset that holds
  still, with no drift. A ramp eases in, holds, and eases out. Don't blend
  them into one move.
- **Scale around the eyes, inside the safe area.** Never crop the forehead or
  chin under a graphic. When a graphic sits at the top, push in from the top
  edge so the head clears it.
- **No edges.** The picture fills the frame at every frame of a move. Clamp
  the offset so no black or empty edge ever shows.
- **Sharpness.** The apps show about 1080 wide, so 4K footage punches to 2x
  with no visible loss, and 1080p footage softens past about 1.2x. If a zoom
  they ask for will look soft, say so before building it.
- Check zooms on frames pulled from the render, not snapshots.
- Write zooms as `scale` plus `x`/`y` with `transformOrigin: "0px 0px"`. The
  renderer ignores CSS `transform-origin`.

## Boxes and text

- Boxes size to their text. Never a fixed width wider than the words.
- One idea per line. Don't split one idea over two lines on a full screen.
- One accent color. Emphasis words use it.
- Every value comes from `brand.css` variables.

## Captions

- Up to 3 words at a time in the lower third, wherever no graphic holds that
  space. Each word appears as it's said, whole (not typed letter by letter).
- About half a dozen emphasis words per video, in the accent.

## Sound

- Every graphic gets a subtle sound 12–24dB under the voice, by what it does
  (`reference/sound.md`).
- Writing and drawing sounds sit about 6dB under the pops.
- Two deliveries: sound effects only, and with music about 15dB under the
  voice.
- The voice is never limited, compressed or re-mixed by HyperFrames. The
  final mix is built with ffmpeg (`scripts/make_mix.py`).
- Loudness floor: the finished mix lands around -20.5 LUFS with true peaks
  under -1dBTP, by one master gain on everything, no limiter.

## Picture

- Measure brightness per shot. Match shots that differ (often 5–15% from
  window light) with a per-shot exposure that changes on the cuts.
- Grade only the footage, never the graphics.
