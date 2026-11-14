---
name: screenshot-motion-skill
description: Create product videos from screenshots using card spotlight, dark launch-film, orbital gallery, kinetic graphics, prismatic folds, floating page stacks, or page-turn storybook templates, with editable copy, optional licensed audio, portable desktop editing packs, and native editable Storybook drafts for Jianying and CapCut on macOS. Use for screenshot promos, app launch videos, flipbooks, or extending this template library.
---

# Screenshot Motion Skill

Produce a real, editable video with one of seven implemented templates:

| Template | Effect | Screenshots | Duration |
| --- | --- | --- | --- |
| `spotlight` | Five cards unfold, the center screenshot becomes the hero, then the lineup returns | Exactly 5 | 12 seconds |
| `kinetic` | Bold type, split screens and graphic wipes | Exactly 5 | 16 seconds |
| `prism` | Accordion screens, layered glass reveals and light sweeps | Exactly 5 | 18 seconds |
| `orbit` | Neon orbital gallery, depth rotation and final lineup | Exactly 5 | 18 seconds |
| `launch` | Dark editorial promo with collage, feature close-ups, large headlines and CTA | Exactly 5 | 20 seconds |
| `flipstack` | Shared-spine multi-page riffle, camera push and front-facing page reveals | Exactly 5 | 20 seconds |
| `storybook` | Hardcover opens, illustrated spreads turn, cover closes | 1–12 | Configurable holds; 5 pages default to 32 seconds |

Read [template selection and mapping](references/templates.md) before arranging screenshots. Follow an explicitly selected effect. Otherwise recommend/select the closest match from the user's intent, preserving previous choices; do not default all requests to a book. The authoritative template registry is `templates.json`. This is an extensible library, not bundled finished demo videos.

## Inputs and decisions

Identify the product being promoted, the supplied screenshot order, and the output language from the request. Preserve previous choices. If the product is ambiguous, clarify before writing promotional claims; otherwise use reasonable defaults and proceed. Default: 1920×1080, 30 fps, four-second holds for storybook, English explanatory text, no spoken narration.

Inspect screenshots before writing copy. Use the real UI without inventing controls, customer counts, performance claims, prices or download addresses. The explanatory copy is a separate editable layer; text baked into screenshots cannot be changed by changing captions. Use user-provided or appropriately licensed media. Keep private screenshots and generated jobs outside the installed skill directory.

## User-facing interaction

Treat invocation as a request to produce the video. Ask for screenshots and product details only when missing; write the configuration and execute preparation, rendering, and mixing yourself when tools are available. Do not hand the user Python commands or require them to author JSON as the normal workflow. Check local dependencies and report concrete missing requirements. Honor execution permissions; explain any action the user must take when your environment cannot perform it.

Accept revision requests in natural language, update the generated project, and render a revised result. For screenshot or storybook duration changes, prepare a new job so composition metadata stays consistent. Keep technical commands in agent execution or developer troubleshooting, unless the user explicitly requests them. See [developer rendering commands](references/development.md) for manual usage.

## Create the video

1. Read [the configuration reference](references/configuration.md). Write a project JSON beside the user's assets, using the matching example in `examples/` as a starting point. Write short, concrete explanations, one feature per screenshot. Select `--template spotlight`, `--template launch`, `--template orbit`, `--template kinetic`, `--template prism`, `--template flipstack`, or `--template storybook`; the command below illustrates storybook. Respect the validated line limits.
2. Prepare an isolated job:
   ```sh
   python3 /path/to/screenshot-motion-skill/scripts/motion.py prepare --template storybook --config /path/to/project.json --out /path/to/new-job
   ```
   Existing jobs are never overwritten by `prepare`. The job contains its own renderer, copied screenshots and normalized configuration; it does not depend on the skill after preparation except for the helper CLI.
3. Install dependencies **inside the new job** using `npm install`. Node.js 22+ and Chrome/Chromium are required. Use `npm run studio` in that job for interactive preview.
4. Render representative still frames for the selected template first:
   ```sh
   python3 /path/to/screenshot-motion-skill/scripts/motion.py render --job /path/to/new-job --frame 150 --browser /path/to/chrome
   ```
   Inspect the resulting PNG. Correct copy, clipping or layout before a full render. Useful preview frames: spotlight 105/190/330; launch 60/150/250/355/450/550; orbit 45/170/270/380/490; kinetic 35/100/170/245/320/430; prism 70/150/240/330/470; flipstack 24/100/164/200/550; storybook 150 and `90 + holdFrames + 21` for the first turn midpoint. Choose frames within the job duration.
5. Render without `--frame`. This creates `out/video-silent.mp4`. Supply an existing browser explicitly if auto-discovery fails; the script does not download a browser.
6. Run `motion.py mix --job /path/to/new-job` to create `out/video.mp4`. Without audio inputs it makes a silent copy. For music, transition sounds or paper sounds, read [audio and licensing](references/audio-and-licensing.md). Do not add narration unless requested and a suitable authorized voice service is available.
7. Follow [the output checks](references/quality.md), inspect the rendered file rather than only source code, then return the actual video and job path. Be precise about whether narration, listening, or real-time playback was performed. If rendering is blocked, report the specific missing dependency; do not substitute a still image and call it a video.

## Desktop editing delivery

When the user requests a Jianying or CapCut project with replaceable screenshots or editable page text, use the **native editable Storybook** workflow in [editing export and compatibility](references/editor-export.md): `scripts/storybook_native.py`, plus `scripts/capcut_native.py` for CapCut using a local empty-project template. It creates native image/text layers with synchronized keyframes and restores the book layout instead of adding generic bottom subtitles. This mode currently supports Storybook on macOS; do not silently substitute it for another chosen template.

For other templates or a portable media delivery, use the clean render and editing pack workflow in the same reference. Complex motion remains baked into those clips. The separate `jianying.py` adapter wraps baked clips and is not the editable Storybook exporter.

Deliver the actual draft folder and explain how to replace screenshots (retain “复用原视频效果”) and edit native text. Keep a styled reference render when available. Disclose that the native horizontal fold approximates the original curved paper mesh; screenshot pixels are not editable text. Record exact app/version and distinguish draft opening, visual checks, screenshot replacement, text editing, save/reopen, and MP4 export results. Do not claim checks that were not completed. Add a uniquely named draft to the local library when requested for testing/opening; otherwise return a standalone folder. Never overwrite existing drafts.

## Stable implementation details

The following page-curl notes apply to storybook. For spotlight, preserve the paint barrier and screen-space labels. For launch, use normalized `region` crops only where supported by visible UI; never reuse a previous product's pixel coordinates.


- A turning right page has the old screenshot on its front and the next explanation on its back. Do not crossfade entire spreads or mirror the reverse text.
- All geometry follows frame numbers; never introduce wall-clock animation or unseeded randomness.
- The Canvas2D strip mesh avoids nested browser 3D compositing problems. Keep the flat-page fast path, small strip overlap, and continuous lighting overlay: per-strip antialiased shading creates visible lines across text.
- Camera distance 3000 keeps lifted page tips inside the 1080p frame. Recheck the full turn envelope after camera or page-size changes.
- The default renderer fits images without cropping. Landscape screenshots are supported; do not stretch them to a portrait aspect ratio.
- Render sequentially by default. Increasing concurrency requires another visual check of captured frames.

The package's original code is MIT licensed. Remotion and media have separate licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). This skill does not authorize publishing, uploading user assets, changing account settings, or installing itself globally.

## Extend the library

When asked to add another effect, follow [the extension contract](references/extending.md). Add a renderer, registry entry and example rather than replacing existing templates. Verify both the new effect and relevant existing templates.
