import type React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {PresenterFrame, Stage, colors, layout, motion, typography} from '../../shared';
import {useClock} from '../types';
import type {SegmentDef} from '../types';

// A 5-second example segment on the sample words.json: each label lands on its own word.
// Delete this folder when your first real segment exists.

const UNKNOWNS = [
	{label: 'Known knowns.', word: 0},
	{label: 'Known unknowns.', word: 2},
	{label: 'Unknown knowns.', word: 4},
	{label: 'Unknown unknowns.', word: 6},
];

const Label: React.FC<{label: string; startFrame: number; active: boolean}> = ({label, startFrame, active}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const pop = spring({frame: frame - startFrame, fps, config: motion.spring});
	return (
		<div
			style={{
				fontSize: typography.title,
				fontWeight: typography.weightBold,
				color: active ? colors.accent : colors.ink,
				opacity: pop,
				transform: `translateY(${(1 - pop) * 40}px)`,
			}}
		>
			{label}
		</div>
	);
};

const Picture: React.FC = () => {
	const frame = useCurrentFrame();
	const {at} = useClock();
	const lineStart = at(8);
	const lineOpacity = interpolate(frame, [lineStart, lineStart + motion.enter], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const current = UNKNOWNS.reduce((acc, u, i) => (frame >= at(u.word) ? i : acc), -1);
	return (
		<Stage>
			<AbsoluteFill style={{padding: layout.safe, justifyContent: 'center', gap: 24}}>
				{UNKNOWNS.map((u, i) => (
					<Label key={u.label} label={u.label} startFrame={at(u.word)} active={i === current && frame < lineStart} />
				))}
				<div style={{marginTop: 48, fontSize: typography.body, color: colors.muted, opacity: lineOpacity}}>
					Eight steps that keep a long video together.
				</div>
			</AbsoluteFill>
			<PresenterFrame />
		</Stage>
	);
};

export const segment: SegmentDef = {
	id: 's01',
	title: 'Example',
	words: [0, 15],
	component: Picture,
};
