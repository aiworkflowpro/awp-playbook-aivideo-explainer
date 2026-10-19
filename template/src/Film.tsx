import type React from 'react';
import {Html5Audio, Sequence, staticFile} from 'remotion';
import {wordRange} from './clock';
import {VOICEOVER} from './film.config';
import {SEGMENTS} from './segments/registry';
import {SegmentContext} from './segments/types';
import type {SegmentDef} from './segments/types';
import {loadFonts} from './shared';

loadFonts();

/** One segment in its own context, so useClock() is relative to the segment's first frame. */
export const SegmentShell: React.FC<{def: SegmentDef; startFrame: number}> = ({def, startFrame}) => {
	const Picture = def.component;
	return (
		<SegmentContext.Provider value={{id: def.id, startFrame, words: def.words}}>
			<Picture />
		</SegmentContext.Provider>
	);
};

/** The whole film: every registered segment at its place on the clock, plus the voiceover. */
export const Film: React.FC = () => (
	<>
		{SEGMENTS.map((def) => {
			const r = wordRange(def.words[0], def.words[1]);
			return (
				<Sequence key={def.id} name={def.id} from={r.from} durationInFrames={r.durationInFrames}>
					<SegmentShell def={def} startFrame={r.from} />
				</Sequence>
			);
		})}
		{VOICEOVER ? <Html5Audio src={staticFile(VOICEOVER)} /> : null}
	</>
);

/** A single segment for stills and segment renders, with its slice of the voiceover. */
export const SegmentPreview: React.FC<{id: string}> = ({id}) => {
	const def = SEGMENTS.find((s) => s.id === id);
	if (!def) {
		return null;
	}
	const r = wordRange(def.words[0], def.words[1]);
	return (
		<>
			<SegmentShell def={def} startFrame={r.from} />
			{VOICEOVER ? (
				<Sequence from={-r.from} layout="none">
					<Html5Audio src={staticFile(VOICEOVER)} />
				</Sequence>
			) : null}
		</>
	);
};
