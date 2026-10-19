# Step {{NN}}: {{step name}} · {{film title}}

> One page per step, saved as `handoff/{{NN}}-{{step-slug}}.md`. The top half is for the user: where
> the film is going and what is waiting for them. The bottom half is for the next agent: what it
> needs to continue without asking. Keep it short; link files instead of copying them.

Written {{date and time}} · status: {{done / waiting for the user / blocked}}
Merged steps: {{none, or which steps this page also covers}}

## For the user

### Where it stands

{{two or three sentences: what this step decided or produced, and how it feels}}

### Waiting for you

| # | Decision | Options | Default if you say nothing |
|---|---|---|---|
| 1 | {{...}} | {{...}} | {{...}} |

### This step at a glance

{{one table shaped by the step: tools (01), questions and assets (02), segments (03), looks and
segment 1 (04), segments and status (05), seams, sound, notes (06), problems and deliverables
(07), lessons (08)}}

## For the next agent

### User's requests

Carried forward from every earlier page, newest last. Only what the user actually said.

| # | Time | The user's words | Applies to |
|---|---|---|---|
| R1 | {{...}} | "{{...}}" | {{steps or whole film}} |

### Judgment calls

- {{what this step decided that the Skill did not prescribe, or changed, and why}}

### Open ends

- {{unfinished, known weak, or left for a later step}}

### Files and next

| Role | Path | Note |
|---|---|---|
| Read first | {{path and section}} | |
| Output | {{path}} | |

Next: {{the next step, and the first thing to do in it}}

---

## progress.md

Keep one `progress.md` at the root of the film folder; update it after every step and whenever a
builder goes out or comes back. When resuming, read it first, then the newest handoff page.

```markdown
# Progress: {{film title}}

| Step | Status | Waiting for the user | One line |
|---|---|---|---|
| 01 Preflight | done | - | all tools found; screenshots and images tried, 5 at once |
| 04 Lock the look | waiting | review segment 1 | look B picked |
| 05 Delegate | - | - | - |

## Out right now

| Segment | Who | Brief | Workspace | Sent |
|---|---|---|---|---|
| s02 | sub-agent | briefs/s02.md | ../my-film-segments/s02 | {{time}} |
```
