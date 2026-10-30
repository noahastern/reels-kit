---
name: signoff
description: Finish a video once the creator approves it. Renders the full-resolution finals, saves Keeps into their blocks and sounds, writes the video's retro with proposed new defaults, and offers a DM automation when the video genuinely fits. Use when someone runs /signoff, or replies to a revision with an approval like "it's done", "ship it", "looks perfect, export it" or "that's final". They should never need to type the command.
---

# Sign-off: export and learn

1. **Render the finals** at full resolution, 4K portrait unless they ask
   otherwise:
   `npx hyperframes@0.8.150 render --resolution portrait-4k --fps <their fps> --quality delivery -o project/renders/picture.mp4`,
   then `python3 <plugin>/scripts/make_mix.py` into
   `videos/<name>/exports/<name>-final-4k-sfx.mp4` and `-music.mp4`. Run the
   flow check on the final. Delete `project/renders/picture.mp4`.
2. **Keeps into the library.** For each Keep from this video's rounds: copy
   the block to `blocks/` (with a preview still) or the sound to
   `sounds/sfx/` and `sounds/catalog.md`. Ask before adding anything they
   didn't mark as a Keep.
3. **Retro.** Write `videos/<name>/retro.md` from `templates/retro.md`: what
   each round changed, in their words, and which notes should become
   defaults. Propose each new default in one line. Only the ones they say yes
   to go into the "My defaults" section of their `CLAUDE.md`.
4. **Clean up.** Revisions stay in `revisions/` unless they ask you to clear
   them.
5. **DM automation.** Read `reference/dm-automation.md` and offer one only if
   this video genuinely fits. If it doesn't, say nothing about it.

Close with where the finals are and the retro's proposed defaults.
