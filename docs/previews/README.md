# Showcase preview maintenance

All eight GIFs were regenerated on 2026-11-18 from the canonical English SYTASK screenshots in `assets/demo-app/`. Each GIF shows the same first eight seconds at original speed as the corresponding website MP4, at 400 pixels wide and 8 fps. GIF and MP4 are derived from one render/configuration; do not substitute older Chinese demo videos. The complete Entrance template lasts eight seconds; other previews are excerpts, not sped-up full animations.

Follow `AGENTS.md` and the canonical manifest for new App effects. Website MP4s are 1280×720, 30 fps, silent H.264; no sound should be added. These screenshots are authorized project demo media, not stock media licensed for reuse in other products. Validation and source paths for this refresh are in `output/canonical-previews/validation.json` at workspace root.

## Publishing full videos

Commit the skill source and these small previews. Create a GitHub release, attach the full MP4s as separate release assets, and then add their verified URLs to the README if desired. Do not commit those MP4s to the source tree. See [GitHub's release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository). No assets are uploaded by this skill automatically.

## Jianying editable Storybook capture

`jianying-storybook-editable.jpg` is an unaltered application screenshot captured on 2026-11-14 in Jianying macOS 11.8.0, using the native editable Storybook delivery draft. It shows an inner-page hold and separate native text tracks. This is a UI capture, not an AI-generated mockup or proof of frame-identical page-turn animation. The project owner requested its inclusion in the README.

## CapCut editable Storybook capture

`capcut-storybook-editable.jpg` is an unaltered application screenshot captured on 2026-11-15 in CapCut macOS 9.7.1. It shows the native Storybook inner-page layout, separate image/text tracks, keyframes and the Text > Basic panel. The English README uses this capture; the Chinese README uses the Jianying capture above. It is not a mockup or proof of complete replacement/edit/export acceptance. The product screenshot inside the book is the original Chinese-language demo image; the editor and book copy are English.
