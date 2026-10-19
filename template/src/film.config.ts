// Film-wide settings. Change them once here, never inside a segment: the format in Step 02 (from the
// kickoff answers), the locked voiceover in Step 03.

export const FPS = 60;
export const WIDTH = 1920; // 1920 x 1080 unless the kickoff chose another size
export const HEIGHT = 1080;

// The locked voiceover in public/, e.g. 'voiceover.wav'. null = silent (the sample has no audio).
export const VOICEOVER: string | null = null;
