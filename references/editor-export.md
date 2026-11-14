# Editing in Jianying or CapCut Desktop

## Native editable Storybook (macOS preview)

For Storybook requests that require replacing screenshots and editing page text, prefer `scripts/storybook_native.py --job /path/to/storybook-job --out /path/to/new-draft` with the isolated Python environment containing pyJianYingDraft 0.2.7 and Pillow. It uses the normalized project and original screenshots directly; a clean MP4 is not needed. macOS Arial fonts are required.

This path preserves the book layout using separate native image and text segments, with synchronized horizontal-fold keyframes. Screenshot replacement must keep **复用原视频效果** checked. Each text line is independently editable; long replacements may need font resizing. It does not reproduce the original curved mesh, perspective or dynamic shadow exactly. Do not market it as pixel-identical. The portable/baked workflow below remains available for other templates.

Local validation on 2026-11-14: Jianying macOS 11.8.0 opened the native project, displayed the cover and inner-page layout, and successfully replaced a screenshot through “替换片段” with the effect-retention option checked. The replacement retained placement and keyframes. Text-edit/save/reopen and final MP4 export still require verification; Windows/CapCut are unverified.

### Export and verify

1. Prepare a normalized Storybook job using `motion.py prepare`; reuse a compatible existing job when available. The exporter reads `project.json`, `public/screenshots/`, and optional audio configuration.
2. Run the native exporter with an isolated Python containing `pyJianYingDraft==0.2.7` and Pillow. Audio stems additionally use the existing FFmpeg workflow. This exporter currently locates Arial under `/System/Library/Fonts/Supplemental`.
   ```sh
   /path/to/isolated-python /path/to/skill/scripts/storybook_native.py --job /path/to/storybook-job --out /path/to/new-draft
   ```
3. On the destination machine, open the uniquely named draft in Jianying. The draft includes its media and `EDITING.md`; it does not depend on temporary rendered clips. If the library list does not refresh, save the current work before restarting the app. Discover the actual application path rather than relying on its display name.
4. Check the cover, each page hold, page-turn midpoints and closing. Compare text position/size, screenshot fit, occlusion and timing against the source layout. A successful JSON export is not visual acceptance.
5. In a test copy, select a screenshot segment → **替换片段** → choose an image → keep **复用原视频效果** checked. Verify placement and keyframes, including through the turn. Select a text segment and edit its native text field; verify focus before typing so shortcuts do not modify the timeline. Check save/reopen and final export before claiming the full workflow passed.
6. Deliver a clean draft without test edits, with a concise account of completed checks and remaining differences. Longer replacement text and changed image aspect ratios may need layout adjustment.

Never overwrite an existing draft. Adding a uniquely named draft to the local library is appropriate when the user requests opening/testing it there; otherwise deliver the standalone folder. Regenerate at the final path because media paths are absolute.

## Deliverables and boundaries

The normal delivery is an MP4 and an editable source project. When the user requests desktop editing, also export a portable editing pack. Do not present a single flattened MP4 as an editable project.

| Item | Editable in the desktop editor |
| --- | --- |
| Clean animation clips | Trim, reorder, speed, grade, and layer |
| Imported SRT captions | Text, timing, font, position and styling |
| Separate music and effects stems | Volume, trim, placement and replacement |
| Original screenshot files | New image overlays or manual replacements |
| Page curl / orbital geometry inside a clip | Baked; rerender through the skill to change |
| Text already inside an app screenshot | Baked; supply an updated screenshot |

Clean mode removes promotional copy, including canvas-painted book text. It preserves screenshot pixels and decorative shapes. Captions are exported independently as a simple title/description timeline; they do not reproduce the original text entrances, typography, label layout, or text printed on turning pages. Storybook captions only cover static holds. Additional original copy is retained in `copy.json`.

Music and effects are separate full-length stems with cue timing and fades already applied. Individual sound cues are not separate clips in the current editing pack. The source project remains available for cue-level revisions.

## Agent workflow

1. Prepare and render the requested final video using the normal workflow. Use the current runtime, which includes `Content.ts` and clean rendering support; old generated jobs must be prepared again rather than having their finished videos misidentified as clean plates.
2. Render the clean mode, then export into a new folder:

   ```sh
   python3 /path/to/skill/scripts/motion.py render --job /path/to/job --clean
   python3 /path/to/skill/scripts/motion.py editor-pack --job /path/to/job --out /path/to/new-editing-pack
   ```

3. Check the clean render visually. Verify that promotional copy is absent, screenshot text remains, and motion is preserved. The exporter checks a source fingerprint and rejects stale or missing clean renders.
4. Inspect the shot boundaries, SRT timecodes, and audio durations. Return the folder and `START-HERE.md`. Do not claim actual editor import was tested unless it was.

The pack includes `visuals-clean.mp4`, numbered `clips/`, `titles.srt`, optional `descriptions.srt`, `audio/`, `screenshots/`, `copy.json`, `timeline.json`, and `audio-licenses.json`. All timeline paths are relative. Use either the full clean video or consecutive shot clips, not both. SRT captions and audio must be moved along with shots if the user changes the edit.

## Platform compatibility

CapCut Desktop officially documents importing SRT files as editable text clips: [CapCut subtitle import](https://www.capcut.com/help/how-to-import-subtitles). This is a media/subtitle workflow, not native project interchange. Jianying is a separate application: verify local subtitle import in the user's exact installed build. If unavailable, provide the copy and shot timings for manual text creation.

Native draft formats, registration, paths and fonts can differ by OS and application version. “Latest version” is not a reproducible compatibility target. Record the exact app version, OS and successful import check before publishing compatibility claims. The native Storybook macOS validation is recorded above. It does not establish compatibility for other platforms, apps, versions, or the separate baked-clip adapter.

## Legacy baked-clip Jianying adapter

A separate optional adapter creates a legacy plaintext draft with motion clips, editable title/description text tracks and separate audio tracks. It does not convert React, CSS transforms, or the page mesh to native animation keyframes.

The adapter uses `pyJianYingDraft==0.2.7` (Apache-2.0), installed into an isolated environment by the agent. Read the [upstream compatibility notes](https://github.com/GuanYixuan/pyJianYingDraft) before use. Do not assume Jianying and CapCut accept the same draft.

```sh
/path/to/isolated-python /path/to/skill/scripts/jianying.py --pack /path/to/editing-pack --out /path/to/new-standalone-draft
```

Generate on the destination machine: the draft contains absolute media paths, while the editing pack is portable. The adapter copies its media into the draft folder, never overwrites an existing folder, and does not install/register a draft in the application. If the folder moves, regenerate from the pack at the new location. Do not rename JSON files or overwrite encrypted app drafts as a compatibility workaround.

A successful JSON export or library readback is **not** proof that a current editor opens it. Keep this feature labeled experimental until the exact target build is tested in the GUI. If incompatible, deliver the portable editing pack rather than promise automatic draft import.
