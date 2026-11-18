# Deterministic engine contract

The eight React/Remotion templates remain the source of visual behavior. No model generates renderer code at runtime. AI is optional and produces only the configuration described in configuration.md; users may fill it themselves.

## Worker interface

```sh
python3 scripts/generate.py --config /staged/project.json --out /jobs/unique-id --browser /usr/bin/chromium
# Add --draft for an installer ZIP (not .jypack).
```

Success: exit 0 with JSON containing `video`, `project`, and optionally `draftZip` (absolute worker-local paths). Logs go to stderr. Failure: nonzero exit with an `error` JSON object for handled operational errors. Retain the job for diagnostics; a completed video is not deleted if the optional draft export fails. Output directories must be new. Native Entrance export is rejected before rendering.

`scripts/engine.py` exposes `registry`, `prepare`, `duration`, `render`, `finalize`, and `job_fingerprint`. `scripts/motion.py` is the developer CLI adapter; `mix` is retained as its old command spelling for silent finalization, not audio mixing. `scripts/generate.py` orchestrates these functions and optional native export. No editor or model dependency is imported for MP4-only requests.

The configuration uses local screenshot paths relative to its file. A web service must stage authorized uploads inside an isolated job directory before calling this trusted-worker API; do not forward arbitrary client filesystem paths. The engine is not an HTTP API or a tenant security boundary. Never execute user-supplied renderer source.

## Future Next.js / Vercel integration

1. Authenticate the user and upload images to private object storage.
2. Validate ownership, file size/type and quotas. Build configuration from form input or optional AI output.
3. Create a persistent task record and dispatch an isolated render worker (for example Vercel Sandbox).
4. Stage assets, run this command with Python, Node 22+, Chromium and FFmpeg installed, and capture its status.
5. Upload artifacts to object storage, update task state and provide authorized download URLs.
6. Apply timeout, retry/idempotency, concurrency and cleanup policies outside the engine.

This refactor does not provision Vercel, object storage, an API, job queue or authentication. npm dependencies use the checked-in lockfile; building a preinstalled worker image is a later deployment optimization. Fonts and browser versions should be pinned in that image for repeatable appearance across hosts.

## Draft delivery

`--draft` requires pyJianYingDraft 0.2.7 and Pillow. Original seven templates produce a ZIP with `draft/`, media, `install_editor_draft.py` and instructions. Paths in the downloaded draft are relative; the installer rebases them on the destination machine. The recipient needs Python 3 and a compatible Jianying desktop client. Template visual parity and client acceptance are separate from successful JSON generation.

`.jypack` remains a desktop-client backup format and is not implemented by this engine. Explicit requests can use the separate jianying-jypack.md workflow.

## Removed code

- `scripts/book.py`: obsolete alias; use `motion.py` or `generate.py`.
- `scripts/jianying.py`: old baked-clip adapter, superseded by native recipes. Portable clean clips/SRT remain available via `editor_pack.py`.
- Audio cue registry fields, audio-stem export branches and empty audio manifests: outputs are silent.

Native exporters, portable media export, destination installers and CapCut conversion remain because they serve distinct supported workflows.
