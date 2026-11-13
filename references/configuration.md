# Project configuration

The input is a UTF-8 JSON object. Choose a `template` value: `spotlight`, `launch`, `orbit`, `kinetic`, `prism`, or `storybook`; `prepare --template` overrides this field. Missing selection defaults to storybook for backward compatibility. Image and audio paths resolve relative to the configuration file; absolute local paths also work. Remote URLs are not fetched. Prepared jobs contain local asset copies.

| Field | Required | Constraints |
| --- | --- | --- |
| `brand` | Yes | 1–20 characters |
| `accent` | Yes | Six-digit hex color, such as `#1467DB` |
| `tagline` | Yes | 1–44 characters |
| `coverTitle`, `closingTitle` | Yes | 1–3 lines; maximum 20 characters per line |
| `cta` | Yes | Maximum 28 characters; use a truthful action |
| `holdSeconds` | No | Storybook only: 3–12 seconds, default 4; rounded to a whole frame |
| `pages` | Yes | Exactly 5 for spotlight/launch/orbit/kinetic/prism; 1–12 for storybook |
| `audio` | No | Optional `music` and `pageTurn` (storybook) or `transition` (spotlight/launch/orbit/kinetic/prism) objects |

Each page needs `image` (PNG/JPEG/WebP), `tag` (32 characters), `key` (36), `detail` (40), `title` (1–3 lines, 22 characters each), and `body` (1–3 lines, 44 characters each). Limits are maxima, not writing targets. Favor fewer words and inspect the final layout. Storybook headings shrink to the page width; spotlight, launch, orbit, kinetic and prism use fixed typography, so inspect line breaks and keep copy concise. English is the tested typography; other scripts require suitable installed fonts and a fresh visual check.

Example optional audio:

```json
{
  "audio": {
    "music": {
      "file": "audio/music.mp3",
      "source": "https://example.org/original-track-page",
      "license": "CC0-1.0",
      "gain": 0.3,
      "startSeconds": 0
    },
    "pageTurn": {
      "file": "audio/page-turn.wav",
      "source": "Original recording by the project owner",
      "license": "Owner-authorized commercial use",
      "gain": 1,
      "startSeconds": 0
    }
  }
}
```

The tool records the supplied license claim; it does not verify it. Gain range is 0–10. Music is trimmed/padded to video length, never automatically looped. The page-turn clip uses at most 1.4 seconds and aligns its measured energy peak with each turn midpoint. Provide a clean, single paper sound. Very short, empty or unsuitable clips need replacement.

## Storybook timeline

At 30 fps: cover holds 45 frames, opens in 45 frames. Each chapter holds `holdFrames`; each interior turn takes 42 frames. The cover closes in 42 frames and holds 60 more. Total frames:

`90 + pageCount * holdFrames + (pageCount - 1) * 42 + 102`

Five pages at four-second holds produce 960 frames / 32 seconds. The prepared job's `project.json` uses `holdFrames` and internal `file` names; the input example uses `holdSeconds` and `image` paths. To change the screenshot set, prepare a new job. To edit existing captions, modify the job JSON, then render again.

Only the 16:9 composition is implemented. Vertical/social variants require adapting layout and verifying all pages; do not claim that changing composition dimensions alone supports them.

## Launch regions and fixed timelines

`launch`, `spotlight`, `orbit`, `kinetic` and `prism` last 600, 360, 540, 480 and 540 frames respectively; `holdSeconds` does not alter them. Their audio cue frames come from `templates.json` and are copied into the job's `templateSpec`. The generated composition and mixer use the same selected specification.

A launch page can include `region: [x, y, width, height]` using fractions of the source image. For example `[0, 0, 1, 0.45]` focuses on the top 45%. The region must fit inside the image and have positive width/height. Unspecified regions show the full image. Region framing preserves aspect ratio and is used in feature close-ups; collage/closing phones always show the full screenshot. Regions are ignored by the other templates.

Spotlight reads the center (third) page's title/body as its hero explanation. Keep its tag and key labels short. Launch reads the first four pages as feature scenes and the fifth in its montage/closing pair. See templates.md for the complete role mapping.
