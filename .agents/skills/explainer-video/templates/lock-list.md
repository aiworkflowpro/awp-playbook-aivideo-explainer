# {{film title}}: lock list

> Step 04 output, saved as `plan/lock-list.md`. These are the film's **world rules**: the few
> things every builder must follow. Lock little, and lock it firmly. Lock nothing and you are
> back to the default AI look; lock everything and you get a slideshow. Everything not on this
> list is open: how things are drawn, the metaphor, the camera, transitions inside a segment,
> pacing. Changing a locked item needs the user's yes.

| Item | Locked as | Why | Locked in |
|---|---|---|---|
| The voice | `audio/voiceover.wav`, final | everything hangs on it | Step 03 |
| The clock | `audio/words.json`; things on screen hang on words, never on seconds | builders land on the same beat | Step 03 |
| Captions | `audio/captions.srt`, proofed; a separate track, never burned in | burned-in captions cannot be fixed | Step 03 |
| Format | {{aspect, fps, resolution}} (`app/src/film.config.ts`) | | Step 02 |
| Stage and background | {{ground: color or flat texture, light direction, grain}} | one stage for every segment | Step 04 |
| Presenter and frame | {{treatment, background, frame, states}} or "none" | | Step 04 |
| Colors | {{background, foreground, one accent; light or dark}} | | Step 04 |
| Fonts | {{faces and files}} | | Step 04 |
| Chapter marks | {{what they look like}} | | Step 04 |
| Entry and exit frames | {{what the first and last frames of every segment show}} | segments never see each other | Step 04 |
| Sound standard | {{loudness target, where music may enter}} | | Step 04 |
| Quality bar | segment 1 as approved, in words: {{...}} | the others aim at it | Step 04 |

## Not locked (on purpose)

How things get drawn; which method or tool a beat uses; where the presenter appears within the
frame's states; transitions inside a segment.
