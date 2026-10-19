import {Config} from '@remotion/cli/config';

// Stills and review renders: JPEG frames are faster; switch to 'png' if you need transparency.
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
