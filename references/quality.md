# Quality checks for all templates

For spotlight, inspect the initial stack, full fan, center hero and final lineup; look for disappearing image layers and unstable small labels. For kinetic, inspect text entrances, both split-screen orientations and all graphic edits. For prism, inspect accordion hinges, layered panel occlusion and light-sweep transitions. For orbit, inspect each settled hero, intermediate rotations, occlusion and final lineup. For launch, inspect all six shots, any configured regions, headline fit, and CTA. For storybook, apply the page-specific checks below. For all effects, compare video and audio duration with the selected registry specification.


Inspect the rendered cover, each held spread, front/back turn samples, near-vertical midpoint, and closing frame. Ensure explanations match screenshots, page backs are not mirrored, page tips stay inside the frame, screenshot aspect ratios are preserved, and page numbers match the chapter count. Small screenshot text is not a substitute for readable explanatory copy.

If text shimmers during a hold, compare consecutive decoded frames. Check that rendering waits for texture loading and canvas painting; preserve the direct-draw flat-page path. If vertical seams occur during turns, preserve strip overlap and the single continuous lighting overlay. Do not conceal such defects by blurring the entire image.

Use FFprobe to verify dimensions, fps, frame count, duration and audio streams. Decode the full file with FFmpeg to detect corrupt output. Check final mixed loudness and true peak, and listen when a playback capability is available. Never report waveform inspection as listening. A full motion review is stronger than still review; disclose the actual checks performed.

```sh
ffprobe -v error -show_streams -show_format /path/to/job/out/video.mp4
ffmpeg -v error -i /path/to/job/out/video.mp4 -f null -
ffmpeg -i /path/to/job/out/video.mp4 -vn -af ebur128=peak=true -f null -
```

A still-only smoke test verifies loading/layout, not all-frame correctness. After changes to geometry or timing, perform at least one full small-project render. Maintain a safe copy of a user's previous final before replacing it. Keep QA images and temporary renders in the job, not in the skill's distributable package.

For editor exports, inspect clean plates for leftover promotional copy, verify each clip frame count and contiguous timeline coverage, parse the SRT files, and check independent audio duration. Test native draft references and text/audio tracks, but distinguish JSON readback from actual GUI import.

For flipstack, inspect frames 15/24 (shared-spine riffle), 59/60 (first reveal), 150/164/178 (front, edge and reverse), 200 (settled chapter), 509/510 (closing edit), and 550 (closing hold). Check that all leaf origins share the same spine and paper backs stay blank, screenshot letters have no mesh seams, and clean rendering removes all promotional copy.

For flipstack direction revisions, verify left-to-right leaf motion about the right spine without mirroring UI text. Compare consecutive settled-page frames: the white floor grid must recede toward the horizon while the book has only a stable readable pose after the main sweeping move.

For whole-book movement, compare frames 0/10/20/30/44: the shared spine translates along a leftward arc and returns to the final front-facing composition. Check all page corners during the large-scale intermediate turns.

Check chapter boundaries 149/150 and 239/240 for pose continuity. Camera motion must not shrink or jump back to its opening pose, and intermediate approach points must not ease to a stop.

For Entrance, inspect frames 35/65 for gentle upward fan entry and readable side introductions, 90–105 for the side-copy exit and fan transition, and 170 for the lifted center card and closing text. Check clean mode removes side text, headings and numbering without altering screenshot pixels.
