import type React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {PresenterFrame, Stage, colors, motion, typography} from '../../shared';
import {useClock} from '../types';
import type {SegmentDef} from '../types';

// Seed for a new segment. mkworkspace.py copies this folder to src/segments/sNN/ and replaces
// __SEGMENT_ID__. Set `title` and `words` from plan/segments.md, then build the picture.
// Stay inside this folder; the shared layer is read-only.

const Picture: React.FC = () => {
	const frame = useCurrentFrame();
	const {at, firstWord} = useClock();
	const opacity = interpolate(frame, [at(firstWord), at(firstWord) + motion.enter], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	return (
		<Stage>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity}}>
				<div style={{fontSize: typography.heading, color: colors.muted}}>__SEGMENT_ID__</div>
			</AbsoluteFill>
			<PresenterFrame />
		</Stage>
	);
};

export const segment: SegmentDef = {
	id: '__SEGMENT_ID__',
	title: 'Untitled',
	words: [0, 0],
	component: Picture,
};
