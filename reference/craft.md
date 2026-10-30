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
- The hook has a camera move (a small push or a punch-in), not a static frame.

## Zooms

- **Punch-ins** are static: one scale and offset, no drift. They cut in and
  out exactly on the creator's jump cuts, with the eyes in the same spot
  across the cut. Alternate them to hide jump cuts where the head barely moves.
- **Zoom ramps**: on a turn in what they say, ease in about 10% around the
  eyes, hold, and ease out right after the next cut. Two or three a video.
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
