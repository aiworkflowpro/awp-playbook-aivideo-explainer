# Step 08: Retrospective

Video: 16:17

More in the video: 23:27 (outside experts), 25:37 (what to change next time).

> **Who**: the main agent, right after delivery (and after publishing, if the platform shows
> retention)
> **In**: the whole film folder; the Skill folder
> **Out**: `retro/retro.md`, `retro/skill-changes.md`, `handoff/08-retrospective.md`; later
> `retro/audience.md`

## Goal

Save everything and write down how this look's edit turned out. Every conversation with the agent
and the Skill teaches a small lesson. Fine-tune those lessons into the Skill so the same problem
does not return. Fine-tune, never rebuild: the framework stays and a few exact lines change.

Read first: every `handoff/` page ("Judgment calls", "Open ends") and `deliver/notes.md`.

## Do

1. **Save everything.** Commit the film folder (plan, briefs, reports, review notes, handoff pages,
   `app/`, deliverables). Delete nothing without asking. The next film may start from this code
   and shared pieces if the user chooses; its look is still chosen for its own topic.
2. `retro/retro.md`: the look and how it held up (what it carried well, where it fought the
   content); what the builders did best and worst; where time and quota went; which tools failed
   or were skipped; what the user said at each gate and the principle behind it. Then lessons,
   one sentence each, with the step and the evidence (a time code, a file). One sighting is a
   note; the same problem in two films is a rule.
3. **Give each lesson a place**: a line on the step page where it happened; a number in
   `config.json`; an idea worth keeping in your own notes file (described generally, without this
   film's content or colors); or a small change to the Skill itself.
4. `retro/skill-changes.md`: one block per change: file and section, the line now, the line after,
   why. Keep each small. A change that needs a new file, step or order is a question for the user.
5. **Bring in outside eyes** when lessons point at the Skill itself, or every few films. From
   inside, a Skill cannot see its blind spots. Hand the Skill folder and `retro/retro.md` to the
   strongest model you have, in a fresh session at its highest effort. Better still, ask expert
   sources: put authoritative books on animation, easing, film and directing theory into a
   notebook tool and ask from the Skill's own framework ("this step says X; what do experts say?").

   ```text
   You are a senior practitioner of long explainer videos made in code by AI agents. Audit this Agent Skill: {{skill folder}}. Read SKILL.md, then steps/, then references/. What happened on a real film: {{retro/retro.md}}.
   Find what I might not see: where the Skill leaves an agent guessing, where it locks down what should stay open, where files contradict each other, where it scores instead of watching, and where it lags behind how the industry works (name the practice and who uses it; never invent sources).
   Fine-tune only: do not rewrite or restructure the Skill, and do not propose new files or steps. Return at most twelve small, exact edits, biggest effect first, each with file and section, the evidence (quote the line), the new text, and how sure you are.
   ```

   Check every answer yourself; drop what you cannot verify and anything that only adds rules.
6. Show the changes to the user. Changing the Skill is their call: apply only what they approve, to
   a copy they keep (an installed plugin is replaced by its next update). Never change the Skill
   in the middle of a film.
7. **After publishing** (if the platform shows retention): at about 48 hours and again at 7 days,
   open audience retention, impressions and click-through, and compare with the channel's own
   similar videos. Map every clear drop and rewatch to its time code, picture and sentence. The
   curve says where, never why: propose a reason and a change the next film can test. A few hours
   after publishing, if click-through is clearly low, try the backup cover; change one thing at a
   time. Write it all into `retro/audience.md`.

## Pass when

- The film folder is committed; nothing was deleted without asking.
- `retro/retro.md` says how the look held up; every lesson names its step and evidence and has a
  place or "dropped, because...".
- Every proposed change to the Skill is small and exact.

## Hand off

`handoff/08-retrospective.md`: one row per lesson (lesson, step, evidence, where it goes, status:
applied / waiting for the user / dropped). After publishing, one row per drop or rewatch. This is
the last step; the next film starts again at Step 01.
