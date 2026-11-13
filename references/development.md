# Developer rendering commands

This reference is for contributors, debugging, and agents executing the skill. The user-facing workflow is to invoke the skill in conversation; users do not need to author JSON or run these commands themselves.

Requirements: Python 3.9+, Node.js 22+, npm, Chrome/Chromium, and FFmpeg for audio mixing and verification.

From the skill directory, list the templates and prepare an isolated job:

```sh
python3 scripts/motion.py templates
python3 scripts/motion.py prepare --template spotlight --config /path/to/project.json --out /path/to/new-job
```

Start from the matching JSON in `examples/`. Replace sample image paths and copy. Read [configuration](configuration.md) and [template roles](templates.md). Keep jobs outside the skill folder. Preparation refuses to overwrite an existing job.

Inside the generated job, install the pinned dependencies with `npm ci`. Use `npm run studio` for interactive developer preview.

From the skill directory, render a still, inspect it, then render the complete video and mix any configured audio:

```sh
python3 scripts/motion.py render --job /path/to/new-job --frame 190 --browser /path/to/chrome
python3 scripts/motion.py render --job /path/to/new-job --browser /path/to/chrome
python3 scripts/motion.py mix --job /path/to/new-job
```

Output: `out/video-silent.mp4` and `out/video.mp4`. Without audio, both are silent. `--browser` can be omitted if Chrome is found; `CHROME_PATH` is also supported. The helper does not automatically download a browser. `scripts/book.py` is a compatibility alias; prefer `motion.py`.

Follow the [quality checks](quality.md) before delivery. Caption edits can be made in the job's `project.json` before rerendering. For screenshot changes or storybook duration changes, prepare a new job from the input configuration so the composition metadata is regenerated consistently.

Python orchestrates preparation, validation, and audio mixing. The React/Remotion renderers define the motion. The skill supplies the agent's workflow for choosing a template, interpreting screenshots, writing copy, checking results, and carrying out revisions.

## Desktop editing output

For the clean render, portable editing pack, and optional experimental Jianying draft adapter, follow [editing export](editor-export.md). The native adapter uses an optional isolated Python dependency; normal rendering and portable export do not require it.

## Contributor checks

Run `python3 -m unittest discover -s tests -v` from the skill directory for timeline coverage, caption timing and output safety checks. Typecheck the generated job with `npm run typecheck`. A new renderer also requires visual checks and a complete rendered video; these tests do not prove motion quality or editor compatibility.
