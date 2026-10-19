import type React from 'react';
import {createContext, useContext} from 'react';
import {wordEndFrame, wordStartFrame, WORDS} from '../clock';

/** What every segment folder exports from its index.tsx as `segment`. */
export type SegmentDef = {
	/** Folder name, e.g. 's01'. */
	id: string;
	title: string;
	/** First and last word of the segment in words.json (inclusive), from plan/segments.md. */
	words: [number, number];
	/** The segment's picture. Frame 0 is the segment's first frame. */
	component: React.FC;
};

type SegmentState = {id: string; startFrame: number; words: [number, number]};

export const SegmentContext = createContext<SegmentState>({id: '', startFrame: 0, words: [0, 0]});

/**
 * Inside a segment: word timings relative to the segment's own frame 0.
 *   const {at, endOf} = useClock();
 *   const t = at(12);            // frame where word 12 starts
 */
export const useClock = () => {
	const s = useContext(SegmentContext);
	return {
		id: s.id,
		words: WORDS,
		firstWord: s.words[0],
		lastWord: s.words[1],
		at: (wordIndex: number) => wordStartFrame(wordIndex) - s.startFrame,
		endOf: (wordIndex: number) => wordEndFrame(wordIndex) - s.startFrame,
	};
};
