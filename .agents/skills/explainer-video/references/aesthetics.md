# Aesthetics basics

Read when picking the look and building the shared layer (Step 04), and when building a segment
(Step 05); Step 06 reads "Sound". This is a set of basics to apply with judgment, not a template
and not an acceptance test. Numbers are rough starting points; change them for this film and say
why. Whether it is good is decided by watching (`quality-standard.md`). Each section ends with
signs it looks cheap: the defaults a model slides into first. When you catch one, ask: did I
choose this for this content, or is it the handy default? If it is really needed, use it on purpose.

## Video is not a web page

Video is compressed, watched small and cannot be lingered on. Web sizes disappear in it. On a
1920-wide frame, titles are roughly 64-120 px, body text 28-42 px, borders 2-4 px, margins 60-140
px, and faint decorative layers need more opacity than on the web. Check readability at phone width
(about 390 px). For small-window feeds go one size up.

## Type

- One face performs at a time; the other recedes. Pair across kinds (serif with sans, sans with
  mono) and be able to say what the pairing expresses; if you cannot, it was random.
- Decide the mood before the font, and distrust your first reflex: it is usually the model's
  default. Contrast in weight reads better than a small step.
- Few words per screen; text that stays three seconds is read in two. Emphasize one or two words.
- Stacked numbers use tabular figures or they jitter. Fonts are real files bundled for the
  renderer, never system fonts.

**Cheap**: the same common sans everywhere; two similar sans faces side by side; a small tracked
label over every title; numbering (01/02/03) on things with no order; gradient-filled titles; web
sizes in video.

## Color

- Decide one background, one foreground and one accent first, for the whole film. Do not invent
  colors element by element.
- Avoid pure black and pure white; tint the neutrals slightly toward the accent. Keep the accent
  rare so that it means "look here".
- Avoid full-screen linear gradients on dark grounds (video compression bands them); local light
  or flat color holds up better. A light ground needs some texture or structure or it looks blank.
- Each film's palette comes from its own topic, not the last film's. Same meaning, same color.
- Avoid more than a few light-dark flips in a second, and any full-screen white flash.

**Cheap**: the purple-blue gradient; neon on near-black; an untouched UI-kit palette; the accent on
everything; floating bokeh.

## Composition and layout

- Decide what the viewer sees first and build the frame around it. One visual owner per shot; two
  equal actions in a beat means none leads.
- Keep key content inside a safe margin. Separate lead from support by size, weight, position,
  contrast or motion, using at least two together.
- Anchor to edges and zones rather than "centered and floating". Put text in the graphic: a name on
  the shape it names, a value on the line it measures.
- Vertical frames are recomposed, not cropped. Density is ideas per screen, not element count; both
  overfilling and emptiness are faults. If 2D explains it, use 2D.
- Change the picture, not the room: keep one set of light, type and line weight.

**Cheap**: a centered stack of title, subtitle and identical cards; the same rounded card and soft
shadow on everything; a block of text floating in a sea of space; fake window dots; pie charts and
six-panel dashboards.

## Depth and texture

- A background is never an empty void. A quiet tint, grain, faint structure or topic-related
  pattern gives it life without stealing the show.
- Give flat pictures a sense of depth with soft shadows, a consistent light direction, and a little
  blur on what is out of focus. Never place an image bare: a frame, a shadow or a slow move.
- Joins are clean: corners meet edge to edge or overlap on purpose. The settled frame shows this
  best and is checked least.
- A little unevenness (texture, grain, light falloff) separates designed motion from "first attempt,
  too clean". Use glow and glass sparingly.

**Cheap**: frosted glass or glow on everything; a shine sweeping across every word; equalizer-bar
decoration; flat images with no treatment.

## Presenter and frame

- The presenter should seem to sit in a space designed for the film, sharing its light and color.
  Three states usually cover it: large (making a point), corner (giving way to content), hidden
  (full-screen demo). Switch with the content and give each change time.
- Check keying edges first (fringes, hair). Align framing across jump cuts or two heads ghost.

**Cheap**: pasted on a flat color or a random image; white fringes; resizing for no reason.

## Camera and motion

- Every shot has a job and every move a purpose: push in to see, pull out for the whole, move
  across to bring in the next thing. When a shot has been held too long, change the camera or the
  focus, not the number of things on screen.
- Easing is emotion: confident, dreamy, playful. Entrances usually decelerate, exits accelerate; do
  not use one curve for the whole film. Speed is weight: small things over short distances are
  quick, large things crossing the frame get time. Start earlier rather than compress to unreadable.
- Settle, then stay still or move only slightly. The frame is mostly stable, with visible big moves
  on the word they belong to; full-screen moves only at section changes.
- Everything comes from somewhere: an origin, a path, a landing. Stagger things a few frames apart
  rather than all at once. A move starts just before its word and settles soon after it.
- Transitions: A leaves the way B arrives (same axis and direction) so the eye need not jump. Match
  weight to importance: light within a sentence, heavier between sections, heaviest between
  chapters. A cross-fade says "continue", a hard cut "interrupt". Transitions grown from content
  beat generic ones.
- Better no motion than bad motion. Avoid big full-screen scaling, large rotations or fast
  reversals as defaults.

**Cheap**: every element fading up from below; bounce everywhere; linear moves (fine for counters
and scrolling); ambient wobble on everything; a cut on every beat; a full-screen reset as a
transition; hard vanishes; a template with new colors, delivered.

## Pacing and story

- Open on something real in the first seconds, in the viewer's language, not internal names.
- Vary shot length: faster before a climax, a breath every so often. End quietly.
- Be bold in one place and quiet elsewhere. Design the still first, then the motion. Do not force a
  newly learned technique into every film.

## Sound

- The voice is first, events give weight, music is air and always sits under the voice. Aim for the
  loudness targets in `config.json` (about -14 LUFS, true peak under -1 dBTP); no dead silence.
- Each physical event gets one sound on its frame, matching its material (paper sounds like paper).
  Little or nothing during explanation. Effects are quiet, layered sparingly and never stacked
  three times.
- Compare effect peaks by dBFS and voice and music by LUFS; do not mix them. Generated effects
  often arrive too quiet; normalize before mixing. If you cannot hear it, measure it.

## Self-checks

- Shrink the frame to black-and-white blocks: if it could be anyone's, it is too generic.
- Would I make this same plan for any similar film? Then rewrite it.
- Does every element have a verb? If you cannot say what it is doing, it is not finished.
