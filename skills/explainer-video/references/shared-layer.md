# The shared layer

> Step 04 detail: read while the main agent builds each piece, after the user has picked the look.
> The shared layer holds style only. Keep it thin and fast; hand it in as soon as segments can start.

Same stage, same clock. Shots finished one at a time, each with its own setup, can each be signed
off and still fall apart played back to back. The shared layer prevents that; everything else
stays open.

## The pieces

- **Project skeleton**: the Remotion project from `template/`: the word clock (`words.json` mapped
  to frames), segment folders that register themselves (`src/segments/sNN/`), still and render
  commands. If a segment is made in another tool, decide how its clip comes back: format, frame
  rate, and the word it starts on.
- **Stage background**: the 2D ground from the style sheet, with a sample frame per common framing.
- **Presenter frame**: keying and color correction, the background behind the presenter, the frame,
  its states (large, corner, hidden) and the switches between them. Skip if there is no presenter.
- **Color, type and texture tokens**: a tokens file (`template/src/shared/tokens.ts`), a type
  sample, the light direction and ground texture. Fonts are files and have loaded in a render.
- **Screen frames**: how terminal screens, screenshots and browser captures sit on the stage. Match
  the film: dark screens in a light film become two black holes.
- **Sound standard**: loudness and ducking, room tone at edits, a short list of what each kind of
  sound means, where music enters and leaves, and one file the user can simply listen to.
- **Entry and exit frames**: what the first and last frames of every segment look like. By default
  the bare stage with the presenter in the agreed position. Make one sample image. Segments cannot
  see each other; this is their only agreement.
- **Review board**: stills of every piece on one board, shown to the user with segment 1.

## What stays out

- **Drawing kits.** How a picture is drawn is staging, invented per beat. The shared layer holds
  no brushes.
- **Sample stagings.** Segment 1 already proves the look can be built.
- **Ready-made parts**: no cards, objects or layouts ready to assemble. Handed ready-made parts,
  every segment reaches for them and the film looks the same. The layer holds capabilities, not
  layouts.
