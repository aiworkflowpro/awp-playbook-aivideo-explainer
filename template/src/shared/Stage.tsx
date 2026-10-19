import type React from 'react';
import {AbsoluteFill} from 'remotion';
import {colors, typography} from './tokens';

/**
 * The bare stage every segment stands on: background, base type, safe area.
 * Placeholder: in Step 04 give it the film's real texture and light. Segments do not restyle it.
 */
export const Stage: React.FC<{children?: React.ReactNode}> = ({children}) => (
	<AbsoluteFill
		style={{
			backgroundColor: colors.stage,
			color: colors.ink,
			fontFamily: typography.family,
			fontSize: typography.body,
		}}
	>
		{children}
	</AbsoluteFill>
);
