---
name: onboard
description: Set up a creator's video brand kit in an empty folder before any editing. Walks them through references, look, fonts, colors, block styles, sounds and music, then writes brand/, blocks/, sounds/, videos/, a CLAUDE.md and a visual style guide. Use when someone runs /onboard, starts the reels kit in a new folder, or wants to redo their brand.
---

# Onboard: build the brand kit

The creator directs and you build. Your job here is to help them choose a look
on purpose, so their videos don't look like anyone else's. **Show, don't
ask:** every visual choice is made by looking at options rendered on a frame of
their own footage, never by filling in a form. Keep each step short. One
question at a time.

The plugin's shared docs are in its `reference/` folder and its scripts in
`scripts/`, two levels up from this skill's base directory. Read
`reference/folder.md` and `reference/block-types.md` before you start.

## 0. Check the folder and the tools

- The folder should be empty, or already hold a kit (then this is a redo: read
  what's there and change only what they ask).
- Check for `node` (18+), `ffmpeg`/`ffprobe`, `python3` with `numpy`, and
  Google Chrome (for snapshots and the style guide PDF). Say exactly what's
  missing and how to install it. Don't install system software yourself.
- HyperFrames renders the videos. Its skills install into every AI tool on the
  machine (`npx hyperframes@0.8.150 skills`), so ask before running it.

## 1. Who they are

Ask, one at a time:
- Name and handle.
- Platform: Instagram Reels, TikTok or YouTube Shorts (sets the safe area,
  `reference/craft.md`).
- What they make, in a sentence.
- How they film: framing (tight, seated, waist up), camera or phone.
- **One of their videos**, raw or posted. Pull three frames from it with
  ffmpeg. Every option from here on is shown on these frames.

## 2. References

Ask for 3–5 references: links, screenshots, reference frames, screen
recordings, their own past videos, anything. Instagram and TikTok links
usually can't be opened; ask for a screenshot or a screen recording instead.
For videos, pull frames and transcribe if useful.

For each one, name what's actually going on in plain words: the hook, the
pacing, how text appears, type, color, texture, motion, sound. Copy the files
into `brand/references/` and write `brand/references.md` (template in the
plugin's `templates/`). End with two or three lines on what the references
have in common. That's the direction.

## 3. See / never see

Ask which graphics and animations they love, and which they never want to see
(examples help: "bouncy emoji", "glitch transitions", "neon", "subtitles in
boxes"). Write the never list into `brand/feedback.md` as the first Don'ts, in
their own words.

## 4. Pick a direction

From the references, propose **three starting directions**, each in one line
(for example: clean editorial, paper collage, bold kinetic type). Build each
as a still on their frame: a hook line, a point box and a caption. Show the
three side by side. They pick one or mix two.

## 5. The look

Still on their frames, one choice at a time:
1. **Palette:** 2–3 options. One accent color only, plus box and ink colors.
2. **Fonts:** a header, a body and a caption face. Use fonts they have
   installed or Google Fonts (check the license allows embedding in video).
   Copy the font files into `brand/fonts/`.
3. **Box style:** radius, padding, shadow, flat or textured.

Write `brand/brand.css` from `templates/brand.css`: every color, font and box
value as a CSS variable, plus the platform's safe area. Blocks only ever use
these variables, so a brand change re-skins everything.

## 6. Their first blocks

For each of the six block types in `reference/block-types.md`, build two
versions **from scratch** in their brand, as small HyperFrames compositions
using only `brand.css` variables. Snapshot each on their frame with the unsafe
zones shaded. They pick one per type. Save the picks to `blocks/<type>.html`
with a `blocks/<type>.png` preview next to each.

## 7. Sound and music

- **Sound effects:** ask where they come from: their own files, an Epidemic
  Sound license (through its connector, if connected), or a free CC0 library
  they choose. Build a starter palette of 7 roles (typing, pop, whoosh, paper
  slide, ping, click, error; `reference/sound.md`). Let them hear two options
  for each, if they want. Save to `sounds/sfx/` and log each in
  `sounds/catalog.md` (from `templates/sounds-catalog.md`) with its source
  and license.
- **Music:** their own tracks, a licensed library, or none. Ask what mood.
  Nothing goes in `sounds/music/` without a license they confirm.

## 8. The style guide

Build `brand/style-guide.html`, then the PDF with
`python3 <plugin>/scripts/html_to_pdf.py brand/style-guide.html brand/style-guide.pdf`.
Pages: the direction and references, palette, fonts, each block with its
preview, the sound palette, and their Don'ts. Show it to them. Change it until
they say it's right.

## 9. Hand over

- Write `CLAUDE.md` from `templates/CLAUDE.md`: who they are, their platform
  and safe area, where everything lives, and an empty "My defaults" section
  that grows from each video's retro.
- Create the empty `videos/` folder.
- Tell them what's next in one line: put footage in a new folder under
  `videos/` and run `/edit`.

## 10. DM automation (ask once)

Read `reference/dm-automation.md`. Then: "You're ready to go. Want to set up a
DM automation for your videos? It's how creators do 'comment X and I'll send
you Y'." If they say no, write that in `CLAUDE.md` and never ask again unless
they bring it up.
