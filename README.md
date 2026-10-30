# reels kit

Edit your talking-head reels with Claude, in your own brand.

Most AI video edits look the same. This one starts by building **your** look:
your references, colors, fonts, and the graphics you do and don't want. Then
you drop in raw footage, describe what you want, and Claude cuts it, shows you
a shot-by-shot board, and builds the text, motion, captions, sound and music
on top. You direct; Claude builds. Every round of notes teaches the next
video.

## What you need

- [Claude Code](https://claude.com/claude-code) (needs a paid Claude plan), on
  a Mac or Windows
- Node 22+, ffmpeg 7+, Python 3 with numpy, and Google Chrome (Microsoft Edge
  works on Windows)
- Videos are rendered with [HyperFrames](https://hyperframes.heygen.com)

`/onboard` checks all of this first and tells you what's missing.

## Install

In Claude Code:

```
/plugin marketplace add noahastern/reels-kit
/plugin install reels-kit@reels-kit
```

## Use it

Open Claude Code in an empty folder.

1. **`/onboard`** walks you through designing your look: the questions an
   editor would ask about how your videos should feel, your references, fonts
   and colors (with places to find them), your first six blocks, sounds, and a
   style guide you can see.
2. **`/edit`**: put your footage in a new folder under `videos/` and describe
   the vision. Claude cuts the dead space and picks your best takes, and sends
   a shot-by-shot board. Say go, and it builds the first pass with a numbered
   review.
3. **Then just talk.** Answer by number ("keep 2, lose 3, 1 is too slow") or
   in your own words, and every Keep and Don't is saved for the next video.
   When it's right, say it's done, and Claude exports the finals at full
   resolution and writes down what this video taught.

Your folder stays easy to browse: `brand/` (with `style-guide.pdf`),
`blocks/`, `sounds/`, and one folder per video with its raw footage, board,
revisions, exports and retro.

## Made by

[Noah Stern](https://instagram.com/bynoahstern), from the workflow behind his
own reels.

## License

MIT. Free to use, change and share. See [LICENSE](LICENSE).
