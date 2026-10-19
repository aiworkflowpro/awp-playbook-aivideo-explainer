// Design tokens: the film's colors, type and motion, decided once in Step 04 (plan/style-sheet.md).
// Segments read these; they never hard-code their own.
//
// PLACEHOLDER: this is a neutral starter look (warm light-gray ground, near-black text, one accent),
// plain on purpose. Replace every value with the look you pick in Step 04.

export const colors = {
	stage: '#f3f2ef', // background of the bare stage
	surface: '#ffffff', // cards, panels, screen frames
	ink: '#1f2328', // main text
	muted: '#6b7280', // secondary text
	accent: '#1f6feb', // the one color that points at things; use it rarely
	line: '#d6d4cf',
} as const;

export const typography = {
	family: 'system-ui, sans-serif', // replace with the family loaded in fonts.ts
	familyMono: 'ui-monospace, monospace',
	title: 96,
	heading: 64,
	body: 40,
	caption: 28,
	weightRegular: 400,
	weightBold: 700,
} as const;

export const motion = {
	// Frames at 60 fps. Restrained: short ease-out entrances and quiet holds.
	enter: 18,
	exit: 12,
	hold: 30,
	spring: {damping: 200, mass: 0.6, stiffness: 120}, // smooth, no bounce
} as const;

export const layout = {
	safe: 96, // margin from the frame edge, in pixels at 1920 x 1080
	presenter: {x: 1340, y: 300, width: 480, height: 640}, // the agreed presenter position
} as const;
