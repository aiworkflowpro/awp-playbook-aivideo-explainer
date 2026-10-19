# Step 02: Kickoff

Video: 11:40

> **Who**: the main agent; the user answers one round of questions
> **In**: the voiceover or script, topic, links, footage; `plan/tools.md`
> **Out**: `plan/context.md`, `plan/materials.md`, `app/` set to the film's format,
> `handoff/02-kickoff.md`

## Goal

Find out what the film should make clear and how it should feel, so nothing downstream is
guessed. The kickoff is an interview: resolution, 16:9 or 9:16, long-form or a short, 30 or 60
fps, and the feeling the film should give are settled here as the frame for everything after.
Take stock of the assets, then set the project up with those numbers. The narration is locked in
Step 03, not here.

Read first: the previous handoff (tool table) and `templates/handoff.md`.

## Do

1. Tell the user in two lines what is coming: eight steps, one handoff page each, four points where
   they look (the look and segment 1, the first cut, the final sign-off), and that effort level
   matters and only they can change it (`SKILL.md`).
2. Make no visuals before the answers; a look made first pulls the user toward whatever you made.
3. One round, ten questions at most. Skip what the narration already answers and note where each
   inferred answer came from. Give two to four options per question, each a sentence on what the
   film would become, plus "tell me in a sentence" and a default, so "all defaults" is valid:
   - format: resolution (1080p), shape (16:9 or 9:16), destination, frame rate (60 or 30);
   - topic and audience; what the viewer should feel and remember at the end;
   - what they want and do not want, including techniques they dislike;
   - length; presenter on camera, in a corner, or not at all; music and sound effects;
   - which tools may be used, whether paid generation is allowed, and up to what limit;
   - which of the four gates they want to see themselves.
4. Write the "feel" answer down word for word. It goes into the style sheet and every brief: a
   builder who only knows what to explain only explains; one who knows what the viewer should feel
   aims higher.
5. `plan/context.md`: who the film serves, the format, the audience's knowledge in three tiers
   (knows it / has heard of it / new to it), the viewing device (mostly phones), open questions
   with a default each.
6. `plan/materials.md`: each asset with path, what it is, which narration lines it can serve,
   source, license. Open each one. The list is a starting point, not a boundary; gaps are filled
   by builders later. If the user is on camera, check the footage first (key edges, framing, skin
   tone).
7. Copy `template/` into `app/` (if only the Skill folder is installed, clone the repository into
   a temp folder and copy its `template/`), initialize git, and set `FPS`, `WIDTH`, `HEIGHT` in
   `app/src/film.config.ts`. Run `npm install` and `npm run still`: one frame proves the toolchain
   at the chosen size. A 9:16 film is composed vertically, never cropped from 16:9.
8. The template is Remotion. With another code-to-video tool, set the same numbers and rebuild the
   same pieces; the workspace script and shared layer here assume Remotion.

## Pass when

- Every question has the user's words or "not answered, default X".
- Nothing visual was made before the answers.
- Every asset in the list was opened and has a license.
- `app/` renders a still at the chosen size and frame rate.

## Hand off

`handoff/02-kickoff.md`: questions (question, options, choice, the user's words) and assets (asset,
spec, where it can go, usable or not). The user's words go into "User's requests" with a time;
every later page carries them. Next: Step 03.
