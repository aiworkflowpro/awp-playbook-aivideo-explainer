# Step 01: Preflight

Video: 10:25

> **Who**: the main agent, with `scripts/preflight.py`
> **Out**: `plan/tools.md`, `handoff/01-preflight.md`, `progress.md`

## Goal

Get the agent's hands ready before anything is built: every tool the film will use runs, reliably,
from the film folder. Sub-agents do most of the building later, and a sub-agent that hits a broken
tool rarely says so: it skips the tool and acts the picture out itself (no screenshot works, so it
draws a fake page) and the film turns monotonous. So prove every tool here. Also find out whether
this is a new film or a resumed one. Make nothing visual; spend and install nothing without a yes.

Read first: `SKILL.md`, `config.json`, and `templates/handoff.md` (the `progress.md` section).

## Do

1. Run the preflight in the film folder:

   ```bash
   python3 <skill-folder>/scripts/preflight.py
   ```

   Required: Node.js 18+ with `npm` and `npx`, `ffmpeg` and `ffprobe`, `git`, Python 3.11+.
   Optional: a local Whisper (openai-whisper or whisper.cpp) for word timings; if the user already
   has word timings it is not needed, and installing it is the user's call. Add `--json` for
   machine output, `--project <film-folder>` when resuming.
2. Ask in one line which tools beyond the basics may be used, or read them from the user's first
   message: capture (screenshots, screen recordings), generation (images, video, music, voice),
   and a second model that can watch video (used in Step 06). List them in `plan/tools.md`: tool,
   what for, the command, paid or free.
3. Run each tool once for real, on the smallest job that proves it (one screenshot of a public
   page, one image, one short clip). Write down the command that worked. A paid call runs only
   after a yes.
4. Run the same jobs from a sub-agent (or a fresh chat). Permissions, logins and sandboxes often
   differ; a tool that works only in the main session is not ready.
5. Run each tool as many times at once as you plan to run builders (`segment_agents_at_once`). If
   it errors under load (rate limits, one shared browser), find the number that works and write
   it down; Step 05 sends no more.
6. A failing tool gets fixed now. If it cannot be, take it out of `plan/tools.md`, tell the user
   what the film loses and the fallback (for example, the user supplies the screenshots).
7. **Resuming**: read `progress.md` and the newest handoff page. Report the last finished step,
   decisions waiting for the user, which builders were out, and the step to resume from. Never
   redo finished work.
8. If anything required fails, stop: fix what you can, list the rest in one message with install
   commands, and do not go on to Step 02.

## Pass when

- Every required tool is found; Whisper is found or the word timings are covered.
- Every tool in `plan/tools.md` ran a real job from the film folder and from a sub-agent, with the
  working command and the number that can run at once.
- Nothing paid ran, and nothing was installed, without a yes.

## Hand off

`handoff/01-preflight.md`: the preflight output, the tool table (tool, what for, command, how many
at once, paid or free) and every fallback. Start `progress.md`. Next: Step 02.
