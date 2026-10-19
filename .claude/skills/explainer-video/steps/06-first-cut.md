# Step 06: First cut

Video: 15:58

Steps 6 and 7 share this time code: the video covers them in one breath. More in the video: 21:09
(why scoring fails, who should watch).

> **Who**: the main agent; a viewer who did not build the film; then the user
> **In**: all segments merged, the locked voice, the sound standard, `plan/materials.md`
> **Out**: `plan/sound.md`, the first cut at review resolution, `review/first-cut.md`,
> `handoff/06-first-cut.md`

## Goal

Join the segments into a rough cut with sound and picture in sync: fix the seams, align color
across joins, mix voice, effects and music, render the whole film. The first cut is the skeleton,
not the finished film. Then have it watched. Whether it is good is a feeling and is never scored:
a viewer who did not build it watches straight through and says in sentences what it felt; you
watch once; the user watches. Do not raise the effort here; save it for Step 07.

Read first: `references/review.md`, the "Sound" section of `references/aesthetics.md`,
`templates/review-notes.md`.

## Do

1. **Seams before the render.** For each join, export a few frames either side; check that one
   segment's last frame is the next one's first, the presenter position matches, nothing floats.
   Fix small problems in the first and last frames now. Sameness between segments waits for Step 07.
2. **Sound**, in order, each with a result before the next: baseline (voice loudness, gaps),
   effects, music, mix and master. Effects from real recordings first, matched to the material on
   screen; generated sound is optional and paid use is asked about. Be restrained: little during
   explanation, music at openings, reveals, section changes and the end, ducking under speech.
   Master to the targets in `config.json` (about -14 LUFS, true peak under -1 dBTP); a limiter and
   a second measurement often help. Judge sound by measurement and listening, not by a model's
   description.
3. Align color and brightness across joins, then render the whole film at review resolution. No
   low-resolution draft: small type and thin lines only show at real size.
4. Run the hard-fault check and look at every flagged time:

   ```bash
   python3 <skill-folder>/scripts/check_render.py out/film.mp4 --out review/check-first-cut.md
   ```

5. **A different pair of eyes**, in order of preference: a second model that can take video, given
   the whole file; a fresh sub-agent (video if its model can watch it, else frames at one-second
   spacing plus the transcript); a brand-new chat. Never the session that built it. Paste, filled in:

   ```text
   You are a viewer, not an editor. Watch this film once, straight through, like someone who clicked on it: {{file or frames}}. It promises: {{promise}}. It is for: {{audience}}.
   Answer in plain sentences with time codes (m:ss): where you were hooked; where you drifted; where you did not understand; where something pulled you out; where it felt cheap or like a slideshow; where parts look or move the same; whether you would keep watching, and why.
   No scores, ratings or tables. Say only what you saw; if unsure whether something is a glitch, say so. End with "good enough" or "fix these three things, because...".
   ```

6. Reproduce any reported jump or freeze on stills or by measurement before fixing it: a model
   watching video samples frames and can see a jump that is not there.
7. Watch the first cut yourself once, without pausing, and write what you feel. Some notes exist
   only at this scale: joins that do not line up, every segment staged the same way.
8. `review/first-cut.md` (`templates/review-notes.md`): builders' weak spots, seam problems, the
   viewer's notes as written, yours. This is input for the polish, not the full list.
9. **Gate: the user watches the first cut.** Record their words with a time; they are the most
   important input for Step 07.

## Pass when

- Every join was checked on both sides; loudness and true peak meet the targets; music ducks.
- The cut plays end to end at the right resolution, frame rate and length.
- A viewer who did not build the film watched it whole and wrote what it felt, with no scores.
- The user's words are recorded.

## Hand off

`handoff/06-first-cut.md`: seams (join, what you saw, what you did), sound (time, what it marks,
loudness), known problems (time code, problem, severity), integrated loudness and true peak, and
who watched. If the user does not watch, go on from the viewer's notes, say why, and stop again
before sign-off in Step 07. Next: Step 07, in a brand-new session at higher effort.
