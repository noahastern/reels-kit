---
name: onboard
description: Set up a creator's video brand kit in an empty folder before any editing. Asks the questions an editor would ask about what their videos should make people feel, collects references, and helps them design their own look (fonts, colors, boxes, blocks, sounds) with resources and live previews on their footage. Writes brand/, blocks/, sounds/, videos/, a CLAUDE.md and a visual style guide. Use when someone runs /onboard, starts the reels kit in a new folder, or wants to redo their brand.
---

# Onboard: build the brand kit

The creator designs their look, and you build it. Your job is to ask the
questions a good editor would, point them to the right resources, and show
every choice they make on their own footage so they can see it before they
commit. **Don't design it for them.** Taste is theirs. Craft is yours:
legibility on a phone, contrast over their footage, the safe area, how long
text needs on screen. Speak up on craft; stay out of taste unless they ask.

Keep each step short. One question at a time.

The plugin's shared docs are in its `reference/` folder and its scripts in
`scripts/`, two levels up from this skill's base directory. Read
`reference/folder.md` and `reference/block-types.md` before you start.

## 0. Check the folder and the tools

- The folder should be empty, or already hold a kit (then this is a redo: read
  what's there and change only what they ask).
- Check for `node` (22 or newer), `ffmpeg` and `ffprobe` (7 or newer),
  Python 3 with `numpy`, and Google Chrome (Microsoft Edge works on Windows).
  Say exactly what's missing and how to install it on their system. Don't
  install system software yourself.
- On Windows, run the plugin's scripts with `python` (or `py`) wherever the
  docs say `python3`.
- HyperFrames renders the videos. Its skills teach you how to write its
  compositions, and `/edit` needs them. They install for every AI tool on the
  machine (`npx hyperframes@0.8.150 skills`), so explain that and ask before
  running it.

## 1. Who they are

Ask, one at a time:
- Name and handle.
- Platform: Instagram Reels, TikTok or YouTube Shorts (sets the safe area,
  `reference/craft.md`).
- What they make, in a sentence, and who it's for.
- How they film: framing (tight, seated, waist up), camera or phone.
- **One of their videos**, raw or posted. Pull three frames from it with
  ffmpeg. Every preview from here on is shown on these frames.

## 2. What the videos should feel like

These are the questions an editor asks before touching a timeline. Ask them
one at a time, and don't accept the first vague word: "clean", "engaging",
"professional" and "fun" each mean ten different things. When you get one,
ask what it looks like on screen, or which video does it.

- Someone is scrolling and lands on your video. What should they feel in the
  first second: curious, called out, calm, amused, impressed?
- When it ends, what should they feel, and what do you want them to do?
- Who's watching, and where? On the couch at night, between meetings, on the
  train with the sound off? (That sets the pace and how much has to be read.)
- Should the editing be noticed, or invisible? Is the edit part of the show,
  or should it only make you look good?
- What's the rhythm of how you talk: rapid-fire, or lines that land with a
  pause? Do you ever want silence?
- What does text on screen do for you: repeat what you say, add what you
  don't say, or only mark the big moments?
- With the sound off, how would a stranger know it's your video?
- Which video (anyone's) did you last watch to the end, and what kept you?
- What would make you cringe if you saw it in your own video?

You don't need every question. Stop when you could explain their videos to
another editor. Write their answers, in their words, into the "What my videos
should feel like" section of `CLAUDE.md` (from `templates/CLAUDE.md`). Every
creative call in every video is checked against it.

## 3. References

Ask for 3–5 references: links, screenshots, reference frames, screen
recordings, their own past videos, anything. Instagram and TikTok links
usually can't be opened; ask for a screenshot or a screen recording instead.
For videos, pull frames and transcribe if useful.

For each one, name what's actually going on in plain words: the hook, the
pacing, how text appears, type, color, texture, motion, sound. Then ask what
they'd take from it and what they'd leave. Copy the files into
`brand/references/` and write `brand/references.md` (template in the plugin's
`templates/`).

## 4. See / never see

Ask which graphics and animations they love, and which they never want to see
(examples help: "bouncy emoji", "glitch transitions", "neon", "subtitles in
boxes"). Write the never list into `brand/feedback.md` as the first Don'ts, in
their own words.

## 5. They design the look

They choose; you show each choice on their frames, at real size, inside the
safe area, so they judge it the way a viewer will. If they get stuck or say
"you pick", offer two or three options, each tied to something they said in
step 2, and call them starting points.

1. **Fonts:** a header, a body and a caption face. Send them to look:
   - [Google Fonts](https://fonts.google.com): free, and open licenses that
     allow use in videos.
   - [Fontshare](https://www.fontshare.com): free display and sans faces,
     free for commercial use.
   - [Velvetyne](https://velvetyne.fr): free, open-source display faces with
     character.
   - [Font Squirrel](https://www.fontsquirrel.com): free fonts checked for
     commercial use.
   - A paid font is fine if its license covers video. Fonts that are only
     activated through an app (like Adobe Fonts) usually can't be used here,
     because HyperFrames needs the font file.

   They can send names or files. Render each candidate on their frame at
   caption size and box size, since a font that's lovely on a website can be
   unreadable at phone size over footage. Copy the chosen files into
   `brand/fonts/` and note each license in `brand/fonts/LICENSES.md`.
2. **Colors:** one accent, plus box and ink colors. They can bring hex codes,
   build a palette at [Coolors](https://coolors.co) or
   [Adobe Color](https://color.adobe.com), or pick colors from a reference or
   their own set (sample the pixels from a frame they choose). Show the
   palette over their footage and check that text has enough contrast on a
   phone.
3. **Box style:** ask them to describe it (radius, padding, shadow, flat or
   textured, light or dark), or point at a reference. Show it; adjust until
   they say yes.

Write `brand/brand.css` from `templates/brand.css`: every color, font and box
value as a CSS variable, plus the platform's safe area. Blocks only ever use
these variables, so a brand change re-skins everything.

## 6. Their first blocks

For each of the six block types in `reference/block-types.md`, ask how they
picture it: how it looks, how it comes in and out, and what it sounds like.
Build that, as a small HyperFrames composition using only `brand.css`
variables, and snapshot it on their frame with the unsafe zones shaded.
Adjust until it's theirs. If they have no picture of one, show one simple
version in their brand and let them react. Save each to `blocks/<type>.html`
with a `blocks/<type>.png` preview next to it.

## 7. Sound and music

- **Sound effects:** ask where they come from: their own files, a licensed
  library they pay for (like Epidemic Sound, through its connector if one is
  connected), or a free one: [Pixabay](https://pixabay.com/sound-effects/) (free to use, no
  credit needed) or [Freesound](https://freesound.org) (filter by the CC0
  license). Build a starter palette of 7 roles (typing, pop, whoosh, paper
  slide, ping, click, error; `reference/sound.md`), and let them hear two
  options for each. Save to `sounds/sfx/` and log each in
  `sounds/catalog.md` (from `templates/sounds-catalog.md`) with its source
  and license.
- **Music:** their own tracks, a licensed library, or none. Ask what it
  should feel like, using their answers from step 2. Nothing goes in
  `sounds/music/` without a license they confirm.

## 8. The style guide

Build `brand/style-guide.html`, then the PDF with
`python3 <plugin>/scripts/html_to_pdf.py brand/style-guide.html brand/style-guide.pdf`.
Pages: what the videos should feel like, the references, palette, fonts, each
block with its preview, the sound palette, and their Don'ts. Show it to them.
Change it until they say it's right.

## 9. Hand over

- Finish `CLAUDE.md` from `templates/CLAUDE.md`: who they are, what their
  videos should feel like, their platform and safe area, where everything
  lives, and an empty "My defaults" section that grows from each video's
  retro.
- Create the empty `videos/` folder.
- Tell them how a video works, in plain words: put footage in a new folder
  under `videos/` and run `/edit` with what you want. Claude sends a
  shot-by-shot board; say go. It sends a first pass; reply with notes, or say
  it's done and it exports the finals. No other commands to remember.

## 10. DM automation (ask once)

Read `reference/dm-automation.md`. Then: "You're ready to go. Want to set up a
DM automation for your videos? It's how creators do 'comment X and I'll send
you Y'." If they say no, write that in `CLAUDE.md` and never ask again unless
they bring it up.
