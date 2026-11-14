# Choosing and populating templates

## Spotlight — 12 seconds

The first demo's motion: an overlapping stack deals into five cards, the center card becomes the hero, and all cards return. Best for a compact product overview.

Provide exactly five screenshots in final left-to-right order. Page 3 is the hero. `coverTitle` becomes the opening heading, page 3 `title` and `body` explain the hero, `closingTitle` closes the clip, and `cta` supplies the final supporting line. Page keys label the lineup, and the first three tags become feature chips. Keep keys/tags short (ideally 2–3 words) and inspect wrapping. Screenshots fit portrait display frames without stretching; portrait UI works best.

Example: `examples/spotlight.json`.

## Launch — 20 seconds

The second demo's dark promotional style: screenshot collage, typographic entrances, alternating feature compositions, directional wipes and closing CTA. Best for a product launch or feature pitch.

Exactly five screenshots have these roles:

1. Main product view: first feature, collage and final hero.
2. Feature/action view: second feature scene.
3. Team/detail view: third feature scene; `key` and `detail` supply the supporting card.
4. Overview/result view: fourth feature scene, often a wide crop.
5. Supporting product view: collage and closing companion.

These are visual roles, not required app features. Replace all copy to match the actual product. Optional normalized `region` rectangles focus the feature panels; the original SYTASK pixel crops and AI-specific claims are not universal defaults. Supply a suitable region for a wide panel, or accept a full-image fit with surrounding whitespace. Do not invent metrics or crop away necessary context.

Example: `examples/launch.json`.

## Storybook — variable duration

The third demo's hardcover book: left-page explanations, right-page screenshots, curved page turns and a closing cover. Provide 1–12 screenshots in reading order. Each page uses its own title, body and detail; cover copy is independent. At four-second holds, five pages last 32 seconds.

Example: `examples/storybook.json`. `examples/project.json` remains a backward-compatible storybook example.

## Orbit — 18 seconds

A neon orbital gallery: screenshots rotate through depth around a lit stage, three features settle in front of the camera, and five screens form a final lineup. Exactly five screenshots are needed. The second, third and fourth pages supply the three feature headlines and explanations; the first and fifth support the gallery. `coverTitle`, `closingTitle`, `tagline` and `cta` drive the opening and closing copy. Default accent is lime, but the brand color is configurable.

Use concise headings and portrait screens for the strongest result. The orbital motion is deterministic CSS geometry; no generated imagery, cloud video model, or external 3D assets are required. Example: `examples/orbit.json`.

## Kinetic — 16 seconds

High-contrast poster typography with cream/coral panels, alternating left/right screenshot layouts and directional graphic edits. Five screenshots: the first four supply the four feature scenes; the fifth supports the opening and closing lineups. `coverTitle` and `closingTitle` drive the opening and final CTA. The default accent is coral. Keep the opening title to two short lines for the strongest composition. Example: `examples/kinetic.json`.

## Prism — 18 seconds

Five screenshots unfold like an accordion, then layered glass panels reveal three features under prismatic light sweeps. The second, third and fourth screenshots supply the feature scenes; all five appear in the opening and closing layouts. The default accent is lavender. Portrait images work best. Example: `examples/prism.json`.

Both effects support clean rendering and the same desktop editing pack as the other templates. Their animation remains baked into video clips; imported captions are separate editor text.

## Flipstack — 20 seconds

Multiple curved leaves riffle around one shared right spine. Leaves turn from left to right without mirroring the screenshot pixels. White floor grid lines recede toward the horizon throughout the video. The whole book follows one continuous cubic approach curve while growing and rotating. Later chapter turns use a smooth excursion from and back to the same front-facing pose, avoiding camera resets. Both white grid planes extend inward and move faster toward the horizon. Five 90-frame feature chapters follow a 60-frame opening; the final 90 frames hold the closing message. Each new chapter starts with the same overlapping multi-leaf motion, not independent card rotation. Portrait screenshots sit alongside their explanatory copy on a landscape paper sheet. Copy remains removable in clean mode. Use exactly five images and `audio.transition` for paper foley. Example: `examples/flipstack.json`.

## Media previews

The README embeds small, silent GIF previews under `docs/previews/`; they are not renderer dependencies. Keep full-resolution videos outside the installable skill folder. When published showcase URLs exist, link them from the README. Do not invent public URLs for local-only videos. See [preview maintenance](../docs/previews/README.md).
