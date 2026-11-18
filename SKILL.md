---
name: screenshot-motion-skill
description: Generate silent screenshot videos using eight fixed templates and optional portable Jianying drafts. AI only interprets screenshots and supplies copy/configuration; a deterministic engine handles validation, animation, rendering and packaging.
---

# Screenshot Motion

Use fixed template code. Never regenerate animation source for each request. The same engine runs from this skill or from a server worker without an agent. User-supplied copy needs no AI call.

| Template | Effect | Screenshots | Duration |
| --- | --- | --- | --- |
| `entrance` | Gentle upward fan, introductions on both sides, wide fan and lifted center card | Exactly 5 | 8 seconds |
| `spotlight` | Five cards unfold, the center screenshot becomes the hero, then the lineup returns | Exactly 5 | 12 seconds |
| `kinetic` | Bold type, split screens and graphic wipes | Exactly 5 | 16 seconds |
| `prism` | Accordion screens, layered glass reveals and light sweeps | Exactly 5 | 18 seconds |
| `orbit` | Neon orbital gallery, depth rotation and final lineup | Exactly 5 | 18 seconds |
| `launch` | Dark editorial promo with collage, feature close-ups, large headlines and CTA | Exactly 5 | 20 seconds |
| `flipstack` | Shared-spine multi-page riffle, camera push and front-facing page reveals | Exactly 5 | 20 seconds |
| `storybook` | Hardcover opens, illustrated spreads turn, cover closes | 1–12 | Configurable holds; 5 pages default to 32 seconds |


## Inputs

Read [configuration](references/configuration.md) and [template mapping](references/templates.md). Accept screenshots, product name, description and optional template. Preserve attachment order, explicit template and language. Infer copy language from the app name, falling back to request language. Inspect screenshots before writing short copy; do not invent product claims. Keep copy separate from screenshot pixels. Ask only for missing essential inputs.

AI's responsibility ends at a validated project JSON. Use the matching example in `examples/`. Layout, timing, keyframes, image copying, validation and rendering belong to code. Revisions update configuration and create a new job. Do not rewrite templates to satisfy routine copy changes.

## Generation

Default to silent MP4. When requested, also generate a portable native Jianying installer ZIP for the original seven templates. Entrance has no native draft recipe. No music, narration or audio downloads.

Run in an isolated output directory:

```sh
python3 scripts/generate.py --config /path/to/project.json --out /path/to/new-output --browser /path/to/chrome
```

Add `--draft` for a portable native draft ZIP. The worker prepares a job, installs pinned dependencies with `npm ci`, renders and finalizes MP4. It emits a JSON result on stdout and logs on stderr. It never invokes an LLM, opens an editor, installs itself globally or uploads assets. See [engine and deployment contract](references/engine.md).

Node.js 22+, Python 3.9+, Chromium and FFmpeg are runtime dependencies. Native draft export additionally requires pyJianYingDraft 0.2.7 and Pillow. Report missing dependencies concretely. For interactive QA, use the separate prepare/render commands in [development](references/development.md), render representative stills, and inspect clipping and copy before delivering. Follow [quality checks](references/quality.md). Never claim a render or visual check happened unless performed.

## Draft formats

The portable ZIP contains editable draft data, media and an installation script. It is generated without the Jianying client. The recipient needs Python to run the installer and Jianying to edit. It is NOT accepted by the app's “导入剪映草稿” command. Explain this distinction when delivering it. Never rename ZIP to `.jypack`.

Only when explicitly requested, follow [client-backed .jypack export](references/jianying-jypack.md). That optional route still requires the desktop app. Do not invoke it as part of the cloud engine. If unavailable, report the blocker without silently changing formats.

Native draft effects approximate Remotion motion; original seven templates have recipes, but compatibility must be verified per client version and OS. Preserve source projects and never overwrite existing drafts. See [editor compatibility](references/editor-export.md). Keep CapCut adapters for explicit CapCut requests only.

## Template maintenance

The registry is `templates.json`. Preserve deterministic frame-based animation, existing renderer code and screenshot aspect ratios. Storybook uses the Canvas2D mesh; retain the flat-page fast path and strip overlap. Do not introduce wall-clock animation or unseeded randomness. Follow [extension contract](references/extending.md) for new effects.

Original code is MIT licensed; Remotion and media have separate terms in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## App demo assets

For this library’s App showcases and new-effect regression previews, follow [the fixed demo asset rules](AGENTS.md) and use [the English SYTASK manifest](assets/demo-app/manifest.json). Reuse the same screenshot set for GIF and MP4; do not reuse Chinese legacy renders. Customer-provided screenshots still take precedence for customer projects.

## Screenshot count validation

Before preparing a customer job, read the selected template’s minPages/maxPages from templates.json and enforce the shared engine validation. If the supplied count is outside the supported range, stop and ask the user to add screenshots, explicitly choose which to remove, or select another effect. Never pad, truncate, silently substitute demo assets, or switch effects. Preserve existing assets and edits while waiting. See AGENTS.md for the full constraint contract.
