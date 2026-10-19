# Step 04: Lock the look

Video: 13:45

> **Who**: the main agent (look, lock list, style sheet, shared layer); one builder for segment 1
> **In**: `plan/segments.md`, `plan/narration-logic.md`, the locked voice, `plan/materials.md`,
> `plan/tools.md`, the kickoff answers
> **Out**: `plan/looks/`, `plan/lock-list.md`, `plan/style-sheet.md`, `app/` with the shared layer,
> `briefs/s01.md`, `reports/s01.md`, `plan/shared-notes.md`, `handoff/04-lock-the-look.md`

## Goal

Fix one look for the whole film so segments built apart never clash; a disjointed film loses
viewers. Lock only the few things that make it one film, while locking is cheap, then test one
segment first: many looks do not suit a given film, and only a finished segment shows it.

**No ready-made look library ships with this repo.** You define your own look in this step, in
conversation with the model. If you have no preference, the neutral starter look below is the
fallback; it is a placeholder, plain on purpose.

Read first: `references/aesthetics.md`, `references/shared-layer.md`, and the lock list, style sheet
and segment brief templates.

## Do

**A conversation, not a form**

1. Give the model the locked narration, the logic map and the kickoff answers. Ask which two or
   three looks would carry THIS narration and why, each with its main risk. Keep its picks in
   `plan/looks/shortlist.md`; do not trim them to your own taste before the user sees them.
2. If the user has clips they may learn from, make contact sheets
   (`python3 <skill-folder>/scripts/contact_sheet.py references/ --out references/sheets/`) and judge
   on the sheets, not by watching. A reference positions the look; borrow grammar, not
   appearance, and keep it out of the briefs.
3. Make one **still** per shortlisted look, deliberately different, from real material (the real
   presenter frame, type set in code, a real screenshot). No staging samples.
4. **Gate 1: the user picks** one look, or names parts to mix. Choose by two questions: which makes
   the idea clearest, and which the tools can keep repeating for the whole film. Their words go
   into "User's requests". Build nothing more until they pick.

**Lock it, lightly**

5. `plan/lock-list.md` and `plan/style-sheet.md` from the templates (blank slots, fill in the
   chosen look). Lock the few things that never change: the voice and clock, stage, presenter
   frame, colors, fonts, captions, chapter marks, segment entry and exit, format. Lock nothing and
   you are back to the default AI look; lock everything and you get a slideshow. No staging, no
   techniques, no "only use X for Y".
6. Packaging, in `plan/packaging.md`: the promise in a sentence, a few titles and cover
   directions, a first frame that catches the cover. Cover, title, first frame and first 30
   seconds make one promise.
7. Build the **shared layer** yourself, thin and fast (`references/shared-layer.md`): skeleton and
   clock, stage, presenter frame, tokens, screen frames, sound standard, entry/exit frames. Fonts
   are real files. Check each piece on its first and last frame and across state changes.

**Test one segment first**

8. Freeze the shared layer and make segment 1's workspace:

   ```bash
   python3 <skill-folder>/scripts/mkworkspace.py --project app --freeze
   python3 <skill-folder>/scripts/mkworkspace.py --project app s01
   ```

9. Write the segment-1 brief from `templates/segment-brief.md` (Step 05 explains the parts). Say it
   is the pilot: it builds to final quality, sets the bar, and tests the look. Render once.
10. Watch it straight through, then on frames; notes in sentences, hardest look at the opening. If
    the look fights the content, say so now: going back costs one segment, not ten.
11. `plan/shared-notes.md`: the quality bar in words, shared-layer fixes, toolchain lessons (real
    time taken). Segment 1's frames, code and ideas never go into another brief.
12. **Gate 2: the user reviews** the look, style sheet, packaging, shared layer and segment 1,
    your notes first. Revise until a yes, then merge segment 1.

## The neutral starter look (a placeholder: replace it)

Warm light-gray ground, near-black text, one sans-serif family, one accent color used rarely, one
subject per frame with generous margins, short ease-out entrances and quiet holds, hard cuts or
brief cross-fades. The values live in `template/src/shared/tokens.ts`. It gets you a clean, readable film and nothing more.

## Pass when

- The model shortlisted the looks, each with a reason and a risk; the user picked before the
  shared layer or segment 1 began.
- The style sheet holds no staging or techniques; fonts load in a render.
- Segment 1 used the shared layer, was watched whole, and has written notes.
- The user said yes and segment 1 is merged.

## Hand off

`handoff/04-lock-the-look.md`: the looks (picked or not), packaging, shared pieces, segment 1 (a
line and a still per beat). If the look is overturned at Gate 2: new look, style sheet, shared
layer and segment 1. Next: Step 05.
