import type React from 'react';
import {colors, layout} from './tokens';

type Props = {
	/** 'agreed' = the default position between segments; 'large' and 'corner' are the other states. */
	state?: 'agreed' | 'large' | 'corner' | 'hidden';
	/** A presenter video or image, e.g. <OffthreadVideo src={staticFile('presenter.mp4')} />. Empty = a placeholder box. */
	children?: React.ReactNode;
};

const boxes = {
	agreed: layout.presenter,
	large: {x: 560, y: 120, width: 800, height: 840},
	corner: {x: 1560, y: 760, width: 280, height: 240},
} as const;

/**
 * Where the presenter (an avatar, your own recording, or nobody) sits. One frame for the whole film,
 * so every segment enters and leaves with the presenter in the same place.
 * Placeholder: replace the box styling and positions in Step 04.
 */
export const PresenterFrame: React.FC<Props> = ({state = 'agreed', children}) => {
	if (state === 'hidden') {
		return null;
	}
	const b = boxes[state];
	return (
		<div
			style={{
				position: 'absolute',
				left: b.x,
				top: b.y,
				width: b.width,
				height: b.height,
				borderRadius: 24,
				overflow: 'hidden',
				backgroundColor: colors.surface,
				border: `2px solid ${colors.line}`,
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'center',
				color: colors.muted,
				fontSize: 28,
			}}
		>
			{children ?? 'presenter'}
		</div>
	);
};
