import type React from 'react';
import {Composition} from 'remotion';
import {FILM_FRAMES, wordRange} from './clock';
import {FPS, HEIGHT, WIDTH} from './film.config';
import {Film, SegmentPreview} from './Film';
import {SEGMENTS} from './segments/registry';

// "Film" is the whole video; each segment also gets its own composition (s01, s02, ...) for
// stills and segment renders:  npx remotion still src/index.ts s02 out/s02-0300.png --frame=300
export const Root: React.FC = () => (
	<>
		<Composition id="Film" component={Film} durationInFrames={FILM_FRAMES} fps={FPS} width={WIDTH} height={HEIGHT} />
		{SEGMENTS.map((def) => (
			<Composition
				key={def.id}
				id={def.id}
				component={SegmentPreview}
				defaultProps={{id: def.id}}
				durationInFrames={wordRange(def.words[0], def.words[1]).durationInFrames}
				fps={FPS}
				width={WIDTH}
				height={HEIGHT}
			/>
		))}
	</>
);
