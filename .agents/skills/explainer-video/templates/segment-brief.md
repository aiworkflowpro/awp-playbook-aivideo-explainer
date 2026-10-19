# Brief: segment {{sNN}} · {{title}} ({{time range}})

> Filled in by the main agent, saved as `briefs/sNN.md`. Keep it short. It gives a framework, not
> constraints: the more it says about form, the more alike the segments get.

You build one segment of an explainer video. Think like a viewer: they should understand it and
want to keep watching. Inside the world rules below, how this segment is staged is your call, and
you have the model's full range. Read this, then start building; do not reply with only a plan.

## 1. Goal

By the end of this segment the viewer should understand: **{{goal}}**
They should feel: {{feeling}}
How it builds: {{argument order}}
Enters with: {{first frames}} · Leaves with: {{last frames}} · Presenter: {{state}}

## 2. Narration slice

Words {{range}}, {{start}}-{{end}}. Read the whole script first (`{{path to the script}}`), so your
first and last lines land in the right tone.

| Beat | Start | Sentence |
|---|---|---|
| {{sNN-b01}} | {{m:ss.s}} | {{sentence}} |

Beats are cut at breaths; which ones share one idea is your call. Hang everything on words
(`app/public/words.json`), never on seconds.

## 3. World rules (must follow)

Few on purpose. Problems with any of them go back to the main agent.

- The lock list and style sheet: `plan/lock-list.md`, `plan/style-sheet.md`; the shared layer in
  `app/src/shared/` is read-only.
- Your folder: `app/src/segments/{{sNN}}/` only. First and last frames follow the entry and exit
  convention. No sound or music tracks inside the segment; list sound moments in your report.
- Copyright: nothing licensed NC, ND or SA or without a stated license; log every asset's source
  and license. Ask before anything that costs money.
- {{one line on the riskiest thing about this content, never how to draw it}}

## 4. Suggestions (take, combine, replace or invent)

- Tools that work (`plan/tools.md`): {{list}}. Materials: `plan/materials.md`; search for more if
  you need them.
- Reference moments (optional): {{a few, each with what they do well; or "design it yourself"}}.
- Method: try two or three different ideas per beat as rough stills, pick one with a reason
  (`references/presentation-ideas.md`); review the whole segment as a still strip; render at most
  once. Quality guides: `references/quality-standard.md`, `references/aesthetics.md`.
- Corrections from the main agent, if any, appear in `briefs/{{sNN}}-notes.md`.

## 5. Report back

`reports/{{sNN}}.md`, one screen (`templates/review-notes.md` helps):

- **How you staged each beat and what you used** (tools, materials, techniques), one line a beat,
  with the idea you picked and what you tried and dropped. The main agent compares these across
  segments to check they do not all look the same.
- Your first rough stills as soon as they exist (do not wait for approval) and the final strip.
- Assets: source, license, path, which beats use them. Sound moments (word, event).
- The three weakest spots, honestly, and what you need from the main agent.
- Your branch and last commit.
