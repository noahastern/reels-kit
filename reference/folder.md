# The folder

`/onboard` builds this in an empty folder. It's laid out so the creator can
open it in Finder and see everything. Keep it that way: everything only Claude
needs goes in a video's `project/`.

```
my-reels/
  CLAUDE.md                     who they are, their platform, their defaults
  brand/
    style-guide.pdf             the visual brand guide (the one to open)
    style-guide.html            the same guide, editable
    brand.css                   colors, fonts, box style and safe area as variables
    fonts/
    references/                 the reels, frames and videos they fed in
    references.md               what's going on in each reference
    feedback.md                 every Keep and Don't, in their own words
  blocks/
    point-box.html              each block they kept...
    point-box.png               ...with a preview still beside it
  sounds/
    sfx/
    music/
    catalog.md                  what each sound is, its role and its license
  videos/
    2026-11-02-how-i-edit/      date first, so they sort in order
      raw/                      their footage, never changed
      storyboard/board.html     the shot-by-shot board
      revisions/
        v1-sfx.mp4, v1-music.mp4
        v1-review.md            the numbered list sent with v1
        v1-notes.md             what they said back
      exports/                  the full-resolution finals, nothing else
      retro.md                  what each round changed, proposed defaults
      project/                  the HyperFrames project, transcript, cut, mix
```
