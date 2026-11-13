# Editing in Jianying or CapCut Desktop

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

Native draft formats, registration, paths and fonts can differ by OS and application version. “Latest version” is not a reproducible compatibility target. Record the exact app version, OS and successful import check before publishing compatibility claims. No installed Jianying/CapCut app was available during this implementation, so this package does not claim native import validation on either platform.

## Experimental native Jianying draft

A separate optional adapter creates a legacy plaintext draft with motion clips, editable title/description text tracks and separate audio tracks. It does not convert React, CSS transforms, or the page mesh to native animation keyframes.

The adapter uses `pyJianYingDraft==0.2.7` (Apache-2.0), installed into an isolated environment by the agent. Read the [upstream compatibility notes](https://github.com/GuanYixuan/pyJianYingDraft) before use. Do not assume Jianying and CapCut accept the same draft.

```sh
/path/to/isolated-python /path/to/skill/scripts/jianying.py --pack /path/to/editing-pack --out /path/to/new-standalone-draft
```

Generate on the destination machine: the draft contains absolute media paths, while the editing pack is portable. The adapter copies its media into the draft folder, never overwrites an existing folder, and does not install/register a draft in the application. If the folder moves, regenerate from the pack at the new location. Do not rename JSON files or overwrite encrypted app drafts as a compatibility workaround.

A successful JSON export or library readback is **not** proof that a current editor opens it. Keep this feature labeled experimental until the exact target build is tested in the GUI. If incompatible, deliver the portable editing pack rather than promise automatic draft import.
