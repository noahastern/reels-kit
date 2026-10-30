---
name: edit
description: Edit a creator's talking-head video with their brand kit, from raw footage or a finished cut to a first pass. Cuts dead space and retakes on the waveform, sends a shot-by-shot board for review, then builds graphics, captions, zooms, sound effects and music in HyperFrames and hands over a numbered review. Use when someone runs /edit or drops footage into videos/ and describes what they want.
---

# Edit: from footage to a first pass

The creator is the editorial director. They decide what goes on screen and
when; you have the craft to build it. Propose, let them direct, and never make
a creative call that their `brand/feedback.md` already rules out.

The plugin's docs are in `reference/` and its scripts in `scripts/`, two levels
up from this skill's base directory. Read these before the first video in a
session: `reference/craft.md`, `reference/cutting.md`, `reference/sound.md`,
`reference/block-types.md`, `reference/folder.md`.
On Windows, run the scripts with `python` (or `py`) wherever the docs say
`python3`.

Every time, read the creator's `CLAUDE.md`, `brand/brand.css`,
`brand/feedback.md`, `brand/references.md` and the last `retro.md` under
`videos/`. Their Don'ts never come back. Their "My defaults" win over the
plugin's. Check every creative call against "What my videos should feel like"
in their `CLAUDE.md`.

If there's no `brand/` folder, stop and suggest `/onboard` first.

## 1. Set up

Their footage is in `videos/<date-name>/raw/` (create the folder from what
they dropped in if needed). Ask for the vision in plain language if they
haven't given it.

- Scaffold the HyperFrames project in `videos/<name>/project/`:
  `HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes@0.8.150 init project --video <clip> --resolution portrait --skip-transcribe --non-interactive`,
  then copy in their `brand.css`, fonts and the blocks it will use. A video
  keeps its own copies, because HyperFrames renders from its own folder.
- `ffprobe` every clip: resolution, frame rate, rotation, audio. Phones and
  some cameras store portrait video rotated; ffmpeg applies it on decode.
- Extract the voice as WAV and transcribe:
  `npx hyperframes@0.8.150 transcribe <wav> -d project --engine parakeet --language en`.
  Fix misheard words in `text` only.
- **Clipping:** find stretches where the voice hits full scale. Repair them
  (`reference/sound.md`) and tell them which words were affected.
- **Light:** measure the brightness of each stretch of footage. Takes filmed
  minutes apart often differ by 5–15% (window light). Note it for the board
  and the grade.

## 2. Cut

Skip this if they gave you a finished cut; then find their own jump cuts
(`scripts/find_jump_cuts.py`) and only tighten when asked.

From raw footage, follow `reference/cutting.md`:
1. Read the transcript as a script. Group repeated lines into takes.
2. Pick the best take of each line, or the best halves of two takes spliced
   at a comma. Write the picks to `project/cut/picks.json` with a reason each.
3. `python3 <plugin>/scripts/plan_cut.py` finds frame-accurate cut points on
   the waveform. Read its map at every join and fix anything wrong by hand.
4. `python3 <plugin>/scripts/render_cut.py` writes `project/cut-tight.mov`.
5. Check every join: audio identical to the raw with no lag, the first frame
   of each shot matches its source frame, no clicks, no word clipped at either
   end.

## 3. Shot-by-shot board

Before building anything, plan what goes on screen in each shot: which block,
which words it types or lands on, the motion and the sound. Snapshot each
planned graphic on the shot's footage.

Zooms go on the board only where they asked for one or their "My defaults"
place them. If they've never said how they like zooms, ask once, on the board.

Write `project/cut/notes.json` and run
`python3 <plugin>/scripts/make_board.py` to make
`videos/<name>/storyboard/board.html`: one card per shot with its first and
last frame, the words, the take and kind of join, light changes, and the
planned graphic. Under the shots, list everything dropped, with times. Send it
and wait, ending with one line so they know what to say: "Change anything you
want, or say go and I'll build it." Any clear yes ("go", "looks good", "build
it") is a go.

## 4. Build the first pass, without stopping

Build everything on the approved board, plus captions, sounds and music,
following `reference/craft.md`.
- Each graphic is its own sub-composition in `project/compositions/`. Read
  the `hyperframes-core` skill before writing composition HTML.
- Every id inside a composition starts with the composition's name and is
  unique across the whole video.
- Every sound lives in `project/sounds.json` (`reference/sound.md`). The
  `<audio>` tags in `index.html` (for Studio) and the final mix both come from
  it.
- Music: pick a track and list two alternatives in the review.

## 5. Check it yourself

- `npx hyperframes@0.8.150 check`.
- Snapshot every graphic with the unsafe zones shaded: text on the face,
  collisions, anything cut off or outside the safe area.
- After rendering, check zooms and timing on frames pulled from the render.
- Check each sound is audible at its time.
- **Flow check** on every render they get: transcribe the render's audio fresh
  and read it start to finish. Nothing repeats, every sentence is complete,
  no doubled or missing word at a join, no click or room-tone jump at a join,
  no graphic says the same thing twice. Fix it before handing over.

## 6. Hand it over

Render at 1080p for review rounds (faster), mix with
`python3 <plugin>/scripts/make_mix.py`, and save to `videos/<name>/revisions/`
as `v1-sfx.mp4` and `v1-music.mp4`, plus `v1-review.md` (template in
`templates/review.md`): a numbered list of every element, its time and what it
is, so they can answer by number ("keep 2, lose 3, 1 is too slow"). Then open
HyperFrames Studio (`npm run dev` in `project/`) so they can watch it play on
their footage and scrub it themselves.

End with one line so they never need a command: "Send me notes (by number
is easiest), or tell me it's done and I'll export the finals." Then act on
whatever they reply:
- **Notes:** follow the `notes` skill.
- **A clear approval** ("it's done", "ship it", "perfect, export it"): follow
  the `signoff` skill.
- **Praise that might not mean final** ("love it!"): ask "Want me to export
  the finals?"
