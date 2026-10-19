# AGENTS.md

This repository ships one Agent Skill, `explainer-video`, that helps an AI coding agent make a
long explainer video (16:9, minutes rather than seconds) from a voiceover or script, in code,
on the user's own computer. It accompanies the AI Workflow Pro video on making long videos
with AI agents. The method is eight steps, from preflight to retrospective, built on four kinds
of unknowns.

This repository is a toolkit, not a film project. The user's film lives in its own folder. It is a
framework edition: it ships no fixed style and no look library. The user defines their own look in
Step 04 (the model shortlists, the user picks from stills), and a neutral starter look is the
fallback. Briefs give a few world rules and treat everything else as suggestions.

## What is here

All paths are relative to the repository root.

```text
awp-playbook-aivideo-explainer/
├── skills/explainer-video/      the Skill; the only source of truth
│   ├── SKILL.md                 entry point: the eight steps, the four unknowns, the gates
│   ├── steps/                   one page per step, 01-preflight.md to 08-retrospective.md
│   ├── references/              quality standard, review, aesthetics, shared layer,
│   │                            presentation ideas (a method), captions
│   ├── templates/               segment brief, style sheet, lock list, segments, review notes, handoff
│   ├── prompts/start-a-film.md  the prompt to start a film
│   ├── scripts/                 Python 3.11+ helpers, standard library only
│   └── config.json              format defaults, loudness targets, transcription engine
├── template/                    a minimal Remotion starter project, copied into each film
├── .claude/skills/              copy of skills/ for agents opened in this repo (do not edit)
├── .agents/skills/              copy of skills/ for agents opened in this repo (do not edit)
├── .claude-plugin/              Claude Code plugin and marketplace manifests
├── .codex-plugin/               Codex plugin manifest
├── .cursor-plugin/              Cursor plugin manifest
└── gemini-extension.json        Gemini CLI extension manifest
```

## Install the Skill for the user

Do this when the user asks to install or set up the Skill. Pick the line for the agent you are.

| Agent | Install |
|---|---|
| Claude Code | `/plugin marketplace add aiworkflowpro/awp-playbook-aivideo-explainer`, then `/plugin install explainer-video@awp-playbook-aivideo-explainer` |
| Codex | `codex plugin marketplace add aiworkflowpro/awp-playbook-aivideo-explainer`, then `codex plugin add explainer-video@awp-playbook-aivideo-explainer` |
| Cursor | copy `skills/explainer-video/` into the project's `.cursor/skills/` |
| Gemini CLI | `gemini extensions install https://github.com/aiworkflowpro/awp-playbook-aivideo-explainer` |
| Any agent that reads Agent Skills | `npx skills add aiworkflowpro/awp-playbook-aivideo-explainer` |

If none of these work, clone the repository and copy `skills/explainer-video/` into the folder
your agent loads Skills from (for example `~/.claude/skills/` or `.agents/skills/` in the
project). The Skill folder is self-contained: every path inside it is relative to the folder.

After installing, run the preflight and show the user the result:

```bash
python3 <skill-folder>/scripts/preflight.py
```

## Start a film

1. Make a new folder for the film, outside this repository, and start the agent there.
2. Paste the prompt from `skills/explainer-video/prompts/start-a-film.md`, or say
   "make an explainer video from this voiceover" so the Skill triggers.
3. The Skill runs Step 01 (preflight: every tool the film will use is tried for real), then
   Step 02, the kickoff: one round of questions on the format, the audience and the feel, and a
   request for what is missing, such as the voiceover or script (and, optionally, clips the user is
   allowed to learn from).

The minimum kit: a voiceover or a script, an agent, a tool that turns code into video
(Remotion, via `template/`), and the ability to open a fresh conversation. Optional: two or three
clips the user is allowed to learn from.

## Rules for this repository

- Do not write into this repository while helping the user. Their film goes into its own folder.
- `skills/explainer-video/` is the source. `.claude/skills/` and `.agents/skills/` are copies made
  from it before each release; never edit the copies by hand.
- Scripts use only the Python standard library and call `ffmpeg`, `ffprobe`, `git` and, if
  installed, Whisper. Every script has `--help`.
- Nothing in the Skill needs a paid API. Image, video and music generation are optional, bring
  your own, and the agent asks the user before any paid generation.
- Remotion has its own license: free for individuals and small teams; larger companies need a
  company license. See `template/README.md` and https://www.remotion.dev/license.
