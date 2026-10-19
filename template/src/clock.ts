// The clock: every word of the locked voiceover has a start and an end (public/words.json).
// Things on screen hang on words, never on seconds, so builders working apart land on the same beat.

import data from '../public/words.json';
import {FPS} from './film.config';

export type Word = {text: string; start: number; end: number};

type WordsFile = {source?: string; duration?: number; words: Word[]};

const file = data as WordsFile;

export const WORDS: Word[] = file.words;

export const secondsToFrame = (seconds: number): number => Math.round(seconds * FPS);

const lastIndex = WORDS.length - 1;
const clampIndex = (i: number): number => Math.min(Math.max(0, Math.floor(i)), lastIndex);

/** Absolute frame where word i starts. */
export const wordStartFrame = (i: number): number => secondsToFrame(WORDS[clampIndex(i)].start);

/** Absolute frame where word i ends. */
export const wordEndFrame = (i: number): number => secondsToFrame(WORDS[clampIndex(i)].end);

/** Last frame of the film: the end of the audio, or the end of the last word. */
export const FILM_FRAMES: number = Math.max(
	1,
	secondsToFrame(file.duration ?? (WORDS.length ? WORDS[lastIndex].end : 1)),
);

/**
 * Frames covered by the words from..to (inclusive). Segments tile without gaps: a segment runs
 * from its first word to the start of the next segment's first word; the first segment starts at
 * frame 0 and the last one runs to the end of the film.
 */
export const wordRange = (from: number, to: number): {from: number; durationInFrames: number} => {
	const start = from <= 0 ? 0 : wordStartFrame(from);
	const end = to >= lastIndex ? FILM_FRAMES : wordStartFrame(to + 1);
	return {from: start, durationInFrames: Math.max(1, end - start)};
};

/** Index of the first word whose text matches (case-insensitive, punctuation ignored), from a given index. */
export const findWord = (text: string, fromIndex = 0): number => {
	const norm = (s: string) => s.toLowerCase().replace(/[^\p{L}\p{N}']/gu, '');
	const target = norm(text);
	for (let i = Math.max(0, fromIndex); i < WORDS.length; i++) {
		if (norm(WORDS[i].text) === target) {
			return i;
		}
	}
	return -1;
};
