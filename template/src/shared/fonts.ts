// Real font files, loaded by the renderer before the first frame (never system fonts).
// Put the files in public/fonts/ and list them here, then set typography.family in tokens.ts.

import {continueRender, delayRender, staticFile} from 'remotion';

type FontFile = {family: string; file: string; weight?: string; style?: string};

export const FONTS: FontFile[] = [
	// {family: 'Inter', file: 'fonts/Inter-Regular.woff2', weight: '400'},
	// {family: 'Inter', file: 'fonts/Inter-Bold.woff2', weight: '700'},
];

let started = false;

export const loadFonts = (): void => {
	if (started || FONTS.length === 0 || typeof document === 'undefined') {
		return;
	}
	started = true;
	const handle = delayRender('Loading fonts');
	Promise.all(
		FONTS.map((f) => {
			const face = new FontFace(f.family, `url(${staticFile(f.file)})`, {
				weight: f.weight ?? '400',
				style: f.style ?? 'normal',
			});
			return face.load().then((loaded) => {
				// Some TypeScript DOM lib versions omit FontFaceSet.add; every renderer browser has it.
				(document.fonts as unknown as {add: (font: FontFace) => void}).add(loaded);
			});
		}),
	)
		.then(() => continueRender(handle))
		.catch((err: unknown) => {
			console.error('Font failed to load', err);
			continueRender(handle);
		});
};
