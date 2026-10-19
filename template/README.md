# Film template (Remotion)

A minimal starting point for the picture of an explainer film. Step 02 of the Skill copies this
folder into your film as `app/` and sets the film's format; Step 04 builds the shared layer on top
of it.

```bash
cp -R template my-film/app
cd my-film/app
npm install
npm run still     # out/s01.png, one frame of the example segment
npm run render    # out/film.mp4, the whole film
npm run studio    # preview in the browser
```

Needs Node.js 18+ and npm. Remotion downloads its own headless browser on the first still or
render; FFmpeg comes bundled with Remotion.

## What is in it

- **The clock** (`src/clock.ts`): reads `public/words.json` (one start and end per word, from
  `scripts/transcribe_words.py`) and maps words to frames at 60 fps. Segments ask "when does word
  212 start", never "what happens at 41.3 seconds".
- **Segments that register themselves** (`src/segments/registry.ts`): every folder
  `src/segments/sNN/` with an `index.tsx` exporting `segment` is picked up in order, so builders
  working in parallel never edit a shared list. `src/segments/_template/` is the seed that
  `scripts/mkworkspace.py` copies for a new segment.
- **A thin shared layer** (`src/shared/`): the stage, the presenter frame, color / type / motion
  tokens, and a font loader. All placeholders (a neutral starter look: light-gray ground, dark text, one accent), to be
  replaced with the look you pick in Step 04.
  Segment builders treat it as read-only.
- **A 5-second example segment** (`src/segments/s01/`), timed to the sample `words.json`.
- **Compositions**: `Film` (the whole video) and one per segment (`s01`, `s02`, ...), for stills
  and segment renders.

## Using your own voiceover

1. Copy the locked `audio/voiceover.wav` and `audio/words.json` into `public/` (replace the
   sample). Never edit the copies; fix the originals and copy again.
2. Set `VOICEOVER = 'voiceover.wav'` in `src/film.config.ts`.
3. Delete `src/segments/s01/` once your first real segment exists, and set each segment's
   `words` range from `plan/segments.md`.

## A segment

```tsx
import {useCurrentFrame} from 'remotion';
import {Stage, PresenterFrame} from '../../shared';
import {useClock, type SegmentDef} from '../types';

const Picture = () => {
  const frame = useCurrentFrame();      // 0 = this segment's first frame
  const {at} = useClock();
  const shown = frame >= at(212);       // appears exactly on word 212
  return <Stage>{shown && <div>...</div>}<PresenterFrame /></Stage>;
};

export const segment: SegmentDef = {id: 's02', title: 'Why it drifts', words: [180, 431], component: Picture};
```

Stills of any segment frame:

```bash
npx remotion still src/index.ts s02 out/s02-0300.png --frame=300
```

The film renders at 1920 x 1080 unless the kickoff chose another size: set `WIDTH` and `HEIGHT`
in `src/film.config.ts` (for example 1080 x 1920 for 9:16, or 2560 x 1440 for a 1440p master),
or pass `--scale` to `remotion render`.

## License

This template's code is MIT (see `LICENSE-CODE` at the repository root). It depends on
[Remotion](https://www.remotion.dev), which has its own license: free for individuals and small
teams; larger companies need a company license. Read the terms at
<https://www.remotion.dev/license> before you use it for work.
