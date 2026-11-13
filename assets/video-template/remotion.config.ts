import {Config} from '@remotion/cli/config';

// Keep capture deterministic on machines with asynchronous GPU compositing.
// This scene only needs CSS transforms; it does not need WebGL/GPU rendering.
Config.setChromiumFlags({
  'disable-gpu-rasterization': true,
  'disable-gpu-compositing': true,
});
Config.setVideoImageFormat('png');
Config.setCrf(12);
