# Adding another template

The registry (`templates.json`) is the selection contract. The prepare command copies the runtime and creates a composition entry point for the selected renderer. It snapshots registry metadata into the generated job so later registry edits do not change an existing job's duration or sound cues.

1. Add a self-contained React component under `assets/video-template/src/`. Read the job's `project.json`; keep user screenshots under `public/screenshots`. Reuse the shared schema and `Region` component where appropriate. Do not reference the skill installation by absolute path.
2. Add a unique registry key with `composition`, `component`, `module`, `description`, `minPages`, `maxPages`, and timing metadata. For a fixed-length effect use `timing: "fixed"`, integer `frames`, and `cues` containing effect peak frames. For a new variable timing model, implement its duration/cue calculation in the CLI as well as its renderer; do not mark it as book timing by accident.
3. Add `examples/<template>.json`, document screenshot roles in templates.md, and update the README's catalog and SKILL.md routing. Add configuration validation for any new fields before job creation.
4. Add shot and caption mappings in `scripts/editor_pack.py` so clean video, SRT and edit-pack boundaries agree. Use `Content.ts` or explicit clean-copy guards to remove promotional lettering without changing screenshots. Keep timeline/cue assumptions visible. The CLI uses registry timing when generating the composition and mixing audio; the renderer's shot boundaries must agree. Adding a registry entry alone does not generate motion code.
5. Validate preparation, typecheck, representative stills and a complete short render. Inspect output frame count, text fit, screenshots, motion continuity and mixed audio. If shared code changed, rerun affected existing templates. Keep all test output and source media outside the skill package.

No existing template should be silently replaced by a newly added one. Maintain stable template IDs and preserve old configuration fields or document an explicit migration. Bump dependency versions only with validation. Renderer code is shipped; finished videos and input screenshots are not.

## Fixed App demo inputs

Use the English SYTASK assets and manifest in `assets/demo-app/` for App effect development and website regression previews. Follow `AGENTS.md`. Inspect both screenshots and captions; generate GIF and MP4 from the same render. The demo set has five images; this does not authorize claiming arbitrary screenshot counts. Declare min/max in templates.json and test renderer layout/timing for each supported count. Current non-Storybook templates require exactly five; supporting three or six requires layout, timing, indexing and export review, not just relaxed validation.

## Per-effect input contract

Each renderer owns its supported screenshot range, published once through templates.json. Web, Skill, CLI and Worker must consume this declaration rather than invent independent limits. Out-of-range input requires user correction before rendering; never pad or truncate automatically. Validate boundary and intermediate counts before expanding the declared range.
