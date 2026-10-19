# Step 05: Delegate

Video: 14:30

More in the video: 18:09 (the task card, the experiment with a strict one).

> **Who**: the main agent; one builder per segment (sub-agent, or a fresh chat each)
> **In**: `plan/segments.md`, the locked voice, `plan/lock-list.md`, `plan/style-sheet.md`,
> `plan/shared-notes.md`, the shared layer, `plan/materials.md`, `plan/tools.md`
> **Out**: `briefs/sNN.md`, `reports/sNN.md`, branches merged, `handoff/05-delegate.md`

## Goal

Hand the rest of the film to sub-agents, one brief each. About three minutes is what a builder can
carry from start to end at full quality, so a 30-minute film is about ten builders, five at once
by default and never more than Step 01 proved. A longer film is not harder, only longer.

The brief is what makes it work. It gives a framework, not constraints: the goal, the feel, a few
world rules, and leave to explore. In the video's experiment an airtight card lost to one that gave a framework
and few constraints; every extra rule narrows the builder and makes segments alike. The main agent writes briefs and checks what comes back; it does not design the
segments.

Read first: `templates/segment-brief.md`, `references/presentation-ideas.md`, `templates/review-notes.md`.

## Do

1. Segment 1 is not rebuilt. Apply the user's Step 04 notes on its branch, then merge. Its frames,
   code and report never go into another brief.
2. Workspace for each segment, from the frozen shared layer, never from main:

   ```bash
   python3 <skill-folder>/scripts/mkworkspace.py --project app s02
   ```

3. Write each brief by filling `templates/segment-brief.md`. It carries:
   - the **goal** and the feeling, in the viewer's terms ("make them want to keep watching");
   - the **narration slice with timings** (beats from `plan/segments.md`) and a pointer to the
     whole script, so the builder knows the story;
   - **world rules** (must follow): the few locked things (lock list, style sheet, the clock, the
     entry and exit frames, copyright, ask before paid tools). Keep them few;
   - **references** (optional): a handful of moments worth a look, tools that work, materials,
     leave to search for more. Suggestions: take, combine, replace or invent;
   - **what to report back**.

   A brief never carries another segment's frames, a list of forms or techniques, or "fade every
   segment in and out, captions at the bottom, ease between every shot". Add one line about the
   riskiest thing in this content, never how to draw it.
4. A builder works beat by beat: understand what the viewer should get and feel; try two or three
   truly different ideas (`references/presentation-ideas.md`), as rough stills; pick one with a
   reason; build. It may choose any means inside the locked look and the clock. It reports its
   first rough stills early; the main agent glances for quality and writes corrections into
   `briefs/sNN-notes.md`, never into a running chat.
5. The report states **how each beat was staged and what tools were used** (and what was tried and
   dropped), the still strip, assets with source and license, sound moments (no audio tracks
   inside a segment), the three weakest spots and what it wants from the main agent. One screen.
6. Builders stay inside `app/src/segments/sNN/`; the shared layer is read-only. Problems with it
   go to the main agent, who fixes them once.
7. Send as many builders at once as `plan/tools.md` allows; more segments go in rounds. Remind the
   user about effort before the first goes out. No sub-agents: one fresh chat per segment, in
   sequence. A film that fits in one conversation is built in one.
8. **Collect for quality.** Regenerate the still strip from the current commit yourself and check it
   against the quality bar and the entry/exit frames. When a report and the frames disagree, the
   frames win. Send back only if clearly below the bar; after two rounds, change approach.
9. **Compare the reports, not the segments.** Read the "how staged" lines side by side. If most
   beats use the same device, layout or tool, write that in the notes for the polish or send the
   weakest back with one sentence; do not add rules to the brief.
10. Accepted: add assets to `plan/materials.md`, merge the branch, note the commit.

## Pass when

- Every brief has goal, narration slice, a short list of world rules, optional references, and
  what to report back; none holds another segment's frames or a list of forms.
- Never more builders ran at once than the tools allow.
- Each report says how every beat was staged and with what; the main agent read them side by side.
- Every new asset has source, license, path and segment; paid items were asked about first.
- Entry and exit frames match the convention; at most one render per segment; branches merged.

## Hand off

`handoff/05-delegate.md`: one row per segment (time, one line on the picture, status: building /
accepted / sent back, a still), the weakest three, branch and commit, and any sameness you
noticed. Next: Step 06.
