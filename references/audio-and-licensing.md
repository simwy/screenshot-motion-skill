# Audio and licensing

Audio is optional and no music or sound recordings are bundled. Keep the unvoiced style unless the user requests narration. Do not assume a system TTS voice is cleared for commercial advertising.

Prefer user-owned recordings or individually verified CC0 assets. Other licenses may be usable if their attribution and distribution conditions are satisfied. “Royalty-free” is not equivalent to public domain. Website-wide marketing labels do not establish a particular file's license. For SaaS use, permission to synchronize audio into a finished video is different from permission to redistribute raw audio in a library.

For each track, record its title, author, source page, license/version, retrieval date, and any required credit. Save a copy of the relevant permission when appropriate. The preparer copies audio and records its SHA-256 in `audio-manifest.json`. Do not label MP3 previews as original lossless files. Do not promise immunity from mistaken Content ID claims.

Useful discovery sources: [Freesound](https://freesound.org/) for individually licensed effects and [OpenGameArt](https://opengameart.org/) for individually licensed music. These are discovery links, not blanket permission to use everything on those sites.

Mix after the picture timing is stable. Check gain in context; low-level recordings may need amplification, while loud ones need attenuation. The helper bounds SFX length, estimates peak delay, fades music, limits peaks, and copies the existing video stream. These operations do not replace listening or measuring the final AAC output.

If delivering both music and SFX-only variants, save the full mix first, temporarily remove `music` from the job manifest, mix again and save the SFX-only version, then restore the manifest. Do not overwrite the only copy of a requested variant. No external service or paid generation is required for local rendering.

Use `audio.pageTurn` for storybook, and `audio.transition` for spotlight/launch/orbit/kinetic/prism. Both have the same fields as the documented audio example. Unsupported audio keys are rejected so a requested track is not silently omitted. Choose material-appropriate effects; paper foley does not belong on every card zoom.
