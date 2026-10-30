---
name: notes
description: Apply a creator's review notes to the current video and log every Keep and Don't to their brand feedback, so the next first pass already knows. Use when someone runs /notes, or answers a review by number ("keep 2, lose 3, 1 is too slow") or describes changes to a revision.
---

# Notes: a review round

This loop is what makes video 10 better than video 1. Every note teaches the
kit something.

If their reply is an approval with no changes ("it's done", "ship it"),
follow the `signoff` skill instead.

1. **Find the video and round.** The newest folder under `videos/` with a
   `revisions/vN-review.md`, unless they name another.
2. **Save their words** to `revisions/vN-notes.md`, verbatim, before changing
   anything.
3. **Read each note against the numbered review.** If a note is ambiguous
   ("make it pop more"), ask one short question, or make your best reading and
   say what you chose.
4. **Apply them**, then run the checks and the flow check from the `edit`
   skill, render `v(N+1)`, and write `v(N+1)-review.md` with what changed at
   the top.
5. **Log what they taught** in `brand/feedback.md`, in their own words, with
   the video name and time:
   - **Keep:** something they liked and want again.
   - **Don't:** something they rejected, and why if they said. A Don't never
     comes back in any video.
   - A plain fix to this video only ("move it up a bit") is not a rule. Log it
     only if they say "always" or it's the second time.
6. If a note changes the brand itself (a color, a font, the box style),
   propose the change to `brand/brand.css` and the style guide and wait for
   their yes.

Tell them in two or three lines what changed and what you logged, then end
with the same line as every hand-over: "Send me more notes, or tell me it's
done and I'll export the finals."
