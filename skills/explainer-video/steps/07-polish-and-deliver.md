# Step 07: Polish & deliver

Video: 15:58

Steps 6 and 7 share this time code. More in the video: 25:37 (effort levels and the polish pass).

> **Who**: a brand-new session at high effort (the polish), then the main agent (second pass,
> delivery)
> **In**: the first cut and project; the user's words on it; `review/first-cut.md`; segment
> reports; packaging, captions, word timings; the materials list
> **Out**: `briefs/polish.md`, `review/polish-report.md`, the final cut, `review/second-pass.md`,
> master, captions, chapters, cover, `deliver/notes.md`, `handoff/07-polish-and-deliver.md`

## Goal

Take out the small faults the first cut still has (bugs in transitions, continuity slips) and
deliver. Hand the whole film to a brand-new session with an empty context and the effort turned
up. Thirty minutes do not fit one context at full quality, but once the first cut stands the film
is on disk and the look is set, so a fresh context can spend all its attention on one job:
watching the whole film and finding what repeats across it. It comes cold, so it is attached to
nothing: it leaves what is good alone, fixes shared problems once, and lifts any stretch that has
gone samey.

Read first: `references/review.md`, `references/quality-standard.md`, and "Delivery" in
`references/captions.md`.

## Do

1. **Turn the user's notes into a brief** (`briefs/polish.md`). Each note goes in first, in their
   words, with four lines: what they saw, what they want underneath, where it applies, what
   "fixed" looks like. Similar spots are fixed together. The rest of the brief gives the purpose,
   the current state, `review/first-cut.md`, the segment reports and the tools. It does not
   prescribe what to watch first or how to fix.
2. **Open a brand-new session** in the film folder and turn the effort up before handing it the
   brief (Claude Code: `/effort high`, or `xhigh` / `max` if affordable; elsewhere the equivalent
   setting). Only the user can change it: ask, and wait for the yes.
3. One session watches the whole film start to end; do not split the polish back into segments.
   Leave what is good alone: changing a good shot is a regression. Fix recurring problems in the
   shared layer once.
4. **Sameness is a defect now.** Several segments in a row with the same kind of picture or rhythm,
   or one composition held too long: change the staging, even of a whole stretch.
5. Whole-film fix habits, as a starting point: things put into a container land fully inside it;
   settled things are square; no text is cut off; a too-fast move starts earlier rather than being
   compressed; overlap instead of an empty beat. If a move's start changes, move its sound.
6. Stills first: compare before and after; once they converge, render the whole film once. Paid
   generation still pauses and asks.
7. **Second pass.** The main agent checks fixed frames and joins as stills, then watches the whole
   film again for regressions. The new version is not automatically better: if a section got
   worse, compare old and new section by section without knowing which is which, and keep the
   winner. Remaining problems go back to the same polish session, or a new one with the same brief.
8. When both passes are clean, show the user for **final sign-off**.
9. **Deliver.** Render the master at the kickoff's resolution and check it:

   ```bash
   python3 <skill-folder>/scripts/check_render.py deliver/master.mp4 --out deliver/check-master.md
   ```

10. Captions are the ones finished in Step 03: export the format the platform wants, spot-check a
    few lines, never transcribe again, never burn them in. Chapters come from each segment's start
    time in `words.json`.
11. `deliver/notes.md`: main choices; outside material and models used; generated content (with
    anything the platform asks to disclose); credits and a sources list for every third-party
    asset; what is still not good enough; your last review. Uploading, publishing and deleting
    are the user's call: ask first.

## Pass when

- Every user note has an outcome, and the polish report says how it was understood and applied.
- The polish ran in a new session at higher effort, watched the whole film, left good work alone
  and checked sameness.
- The second pass found no new high or medium problems; fixed problems did not return.
- The master plays end to end at the right spec and the hard-fault report is clean or explained.
- Captions match the final audio; the sources list covers every third-party asset.

## Hand off

`handoff/07-polish-and-deliver.md`: problems (time code, problem, fix, second pass) and
deliverables (path, spec, check). Next: Step 08.
