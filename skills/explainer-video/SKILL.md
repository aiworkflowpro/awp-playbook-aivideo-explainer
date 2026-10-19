---
name: explainer-video
description: 'Use when the user wants an explainer, tutorial, product or motion-graphics video made in code from a voiceover, script, topic or URL, especially a long one of several minutes. Triggers include "make an explainer video", "turn this voiceover into a video", "make a tutorial video", "motion graphics in code", "make a video with Remotion", "edit a long video with AI". Eight steps: Preflight, Kickoff, Narration & segments, Lock the look, Delegate, First cut, Polish & deliver, Retrospective. A framework edition: it locks the narration, the format and one look, delegates each segment of about three minutes to a fresh sub-agent with a brief that gives a framework rather than constraints, and judges the cut by watching it, never by scoring it. Output is a rendered video file plus captions, chapters and a sources list, made locally with Remotion and FFmpeg. Not for editing an existing timeline in a video editor, and not for avatar-only talking-head videos.'
license: MIT
---

# Explainer Video

Make an explainer video from a voiceover, in code, that still holds up after the first minute.

One conversation can hold a minute of decisions, not thirty: it starts out good and gets worse
toward the end, until the film is a slideshow. So this Skill locks a small framework of what is
already known, hands each segment to a fresh context, and judges the result by watching it.

**This is a framework edition.** It gives you the order of work, the gates, the checks and the
shapes of the hand-offs. It does not give you a fixed style or a catalog of techniques. You define
your own look in Step 04; if you do not care to, a plain starter look is the fallback. Where a
step leaves room, that room is on purpose: use your own judgment and the model's initiative, and
explore. Too many constraints make a rigid, low-quality film; too few slide back to the AI look.

## Who you are

You direct one film, and you are also its designer, animator, editor, sound designer and finisher.
Every viewer has seen the "AI-made" default (Inter, a purple-blue gradient, three centered cards,
everything fading up from below, pure black). They want a film that looks like a person with taste
made it for this exact script. Every trade-off goes back to three questions: will they keep
watching, will they understand it, does it look like careful work? Whether it is good is judged by
watching (`references/quality-standard.md`), never by a score.

## The eight steps

| Step | Page | Produces | User gate |
|---|---|---|---|
| 01 Preflight | `steps/01-preflight.md` | every tool tried for real, from a sub-agent too | none |
| 02 Kickoff | `steps/02-kickoff.md` | format, audience, feel, materials; project set to that format | answers |
| 03 Narration & segments | `steps/03-narration-and-segments.md` | locked voice, word timings, proofed captions; segments and beats | only if content is cut |
| 04 Lock the look | `steps/04-lock-the-look.md` | 2-3 looks as stills, lock list, style sheet, thin shared layer, segment 1 finished | **pick the look**; **review segment 1** |
| 05 Delegate | `steps/05-delegate.md` | one brief and one fresh sub-agent per segment, five at once | none |
| 06 First cut | `steps/06-first-cut.md` | joined and mixed film, watched by a viewer who did not build it | **watch the first cut** |
| 07 Polish & deliver | `steps/07-polish-and-deliver.md` | polish in a brand-new session; master, captions, chapters | **final sign-off** |
| 08 Retrospective | `steps/08-retrospective.md` | everything saved; lessons fine-tuned into the Skill | the user's yes to any change |

Order matters: nothing visual before the kickoff answers; the narration is locked before the
look; segment 1 is finished before the other segments go out.

## The four unknowns

The steps follow a way of working with AI that sorts what you have not told the model by whether
you know the question and the answer (from an Anthropic article on human-AI collaboration).

| Unknown | In a film | What the Skill does |
|---|---|---|
| Known knowns | format, captions, the clock | locks them once: the steps, the format, the voice as the clock, one look |
| Known unknowns | you know the feel, not how to make it | a brief that gives a framework; sub-agents explore |
| Unknown knowns | taste: you know it when you see it | watched, never scored, by someone who did not build it |
| Unknown unknowns | what you did not know to ask | test one segment first; outside audit of the Skill; fine-tune, never rebuild |

## World rules and suggestions

This split runs through the whole Skill, in every brief.

- **World rules** are what a builder must follow: the few things that make it one film (the clock,
  the format, the locked look, the segment entry and exit, copyright, asking before paid tools).
  Keep them few, and write them once in the lock list.
- **Suggestions** are everything else: presentation methods, layouts, tools, reference moments,
  numbers in the references. Take them, combine them, replace them or invent something better.
- Builders report **how** they staged each beat and **what** they used, so the main agent can see
  whether segments are starting to look alike. If they are, say so in a notes file; do not add
  rules.
- The main agent does not design the segments and does not lock the steps more tightly than the
  film needs. When the Skill and the film disagree, the film wins; write down what changed and why.

## Core method

- **Lock the spine first.** The final voiceover (and presenter footage, if any) is the spine. Once
  processed it is locked; if it moves, everything after it is rebuilt.
- **The voice is the clock.** Things on screen hang on words, not seconds. Two levels of names: a
  **segment** (cut by meaning, about three minutes, `s01`...) and a **beat** (one change on screen,
  cut at breaths, usually 1.5-4 s, `s01-b01`...). Whoever builds a segment decides which beats
  share one idea.
- **Split it.** Each segment is built in its own fresh context by its own sub-agent (or a fresh
  chat). A longer film is not harder, only longer.
- **Segments are built on their own.** A builder gets the whole script but never another segment's
  frames; otherwise it copies them or strains to avoid them. Seams and sameness are fixed later by
  a pass that sees the whole film.
- **Clear beats pretty.** First understand what the beat is really about, then choose how to show
  it (`references/presentation-ideas.md`).
- **Lock the look, free the staging.** Lock only the stage, the presenter frame, color, type,
  captions and chapter marks. How each beat is drawn stays open.
- **Test one segment first.** Segment 1 is built to finished before the rest and reviewed with the
  shared layer. If it passes, it stays and the others aim at its quality, not its ideas.
- **Build what is needed.** Code-drawn pictures, screen recordings, real screenshots, licensed
  stock, generated material if you have the tool: all fair. Ask before anything that costs money.
  Log every asset with source and license. The hard edge is copyright.
- **Fix the tool when it breaks.** Never route around it silently: that makes a monotonous film.
- **Stills before video.** Iterate on still frames and contact sheets; render once a segment has
  converged.
- **Taste is watched, not measured.** Code checks hard faults only (format, loudness, flashes,
  black or frozen stretches). "Good" is a feeling, written in sentences by someone who did not
  build it.
- **Verify on the finished film.** Defects live in transitions and joins, not in settled frames.
- **Fine-tune, never rebuild.** Lessons go back into the Skill as small, exact changes with the
  user's yes.

## Effort, sub-agents, fresh chats

- Plan and delegate with your strongest model at high effort. Builders can run a notch lower.
- Polish the first cut in a brand-new session with an empty context at high effort. Never hand the
  whole film to one session at the highest effort: it fills up, compresses, and the end is weaker.
  Only the user can change the effort setting: tell them at the kickoff and again at Steps 05 and 07.
- No sub-agents? A brand-new chat per segment is a clean desk too. A film that fits in one
  conversation need not be split.

## How to work

- **Every step**: read the previous handoff page, then this step's page, then act. Small films may
  merge steps; the handoff says which.
- **One handoff page per step** (`templates/handoff.md`), plus `progress.md` kept current.
- **Gates.** The user looks at four points: the look and segment 1 (Step 04), the first cut
  (Step 06), final sign-off (Step 07). Stop and wait for a yes. If the user hands everything over,
  review yourself and put your notes into the delivery.
- **User notes.** Record the user's words with a time, find the principle behind each, fix it at
  its source and in every similar spot.
- **Requirements versus judgment.** What the user said is a requirement. Everything in this Skill,
  numbers included, is judgment. Copyright and asking before paid generation, uploading,
  publishing or deleting always hold.
- **Before you start**: ask once for what is missing (narration, format, facts only from the
  user's material). Defaults: 16:9, 1080p, 60 fps (`config.json`).

## The film folder

Work in a folder made for the film, never inside the Skill folder.

```text
my-film/
├── progress.md   plan/   audio/   references/   briefs/   reports/
├── review/   handoff/   app/ (Remotion project from template/)   deliver/   retro/
```

## References

`references/` holds the quality standard, review method, aesthetics basics, shared layer,
presentation ideas and captions; `templates/` holds the segment brief, segments, style sheet, lock
list, review notes and handoff; `prompts/start-a-film.md` starts a film; `scripts/` holds
`preflight.py`, `transcribe_words.py`, `contact_sheet.py`, `mkworkspace.py`, `check_render.py`
(each has `--help`). Each step page names what to read.
