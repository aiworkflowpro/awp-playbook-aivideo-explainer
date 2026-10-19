// Segments register themselves: every folder src/segments/sNN/ with an index.tsx exporting
// `segment` is picked up here, in order. Nobody edits a shared list, so builders working in
// parallel never collide. Folders starting with '_' (the _template seed) are skipped.

import type {SegmentDef} from './types';

const context = require.context('./', true, /^\.\/s\d{2}\/index\.tsx$/);

export const SEGMENTS: SegmentDef[] = context
	.keys()
	.sort()
	.map((key) => {
		const mod = context(key) as {segment?: SegmentDef};
		if (!mod.segment) {
			throw new Error(`${key} does not export "segment"`);
		}
		return mod.segment;
	});
