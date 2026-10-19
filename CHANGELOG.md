# Changelog

All notable changes that affect people using this repository are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-19

The first public release, with the video (https://www.youtube.com/watch?v=je8u-utnb5s).
Tagged `v1.0.0` and `video-aivideo-explainer`.

### Added

- The `explainer-video` Skill, a framework edition in the video's eight steps: Preflight, Kickoff,
  Narration & segments, Lock the look, Delegate, First cut, Polish & deliver, Retrospective; with
  the four kinds of unknowns behind them. It ships no ready-made look: you define your own in
  Step 04, with a neutral starter look as the fallback.
- References: quality standard, how to review a cut, aesthetics basics, the shared layer, a method
  for finding a presentation idea per beat, captions.
- Templates: segment brief (goal, narration slice, world rules, optional references, what to report
  back), segments, style sheet, lock list, review notes, handoff.
- The prompt to start a film: `prompts/start-a-film.md`.
- Scripts (Python 3.11+, standard library only): preflight, word-level transcription, contact
  sheets, per-segment workspaces, a hard-fault render check.
- A minimal Remotion starter project in `template/`, with placeholder tokens for a neutral starter
  look.
- Plugin manifests for Claude Code, Codex, Cursor and Gemini CLI, and in-repo copies of the Skill
  in `.claude/skills/` and `.agents/skills/`.
