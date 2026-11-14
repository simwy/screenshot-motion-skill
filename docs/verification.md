# README capability audit — 2026-11-15

This audit compares the repository README with the skill routing, template registry, exporter implementations and local execution. It distinguishes file-generation checks from editor acceptance.

| README capability | Evidence | Limit |
| --- | --- | --- |
| Seven video effects | All seven example configurations prepared new jobs with corresponding renderer files; registered timing matches the README | This audit did not rerender all seven MP4s or replay their animations |
| Storybook supports 1–12 screenshots | Fresh 1-, 2- and 12-page jobs exported native Jianying drafts; durations matched the renderer calculation and all referenced images existed | These are structural checks, not visual acceptance of every page count |
| Native editable Jianying Storybook | `storybook_native.py` exports image/text segments and keyframes, without screenshot MP4 plates; prior local Jianying 11.8.0 session opened the draft and replaced a screenshot | macOS preview; text-edit/save/reopen and final export acceptance incomplete |
| Native editable CapCut Storybook | `capcut_native.py` packaged a freshly generated 2-page draft; prior local CapCut 9.7.1 session displayed cover, inner page, tracks and native text panel | Requires a local empty-project template; replacement, text-edit/save/reopen and final export acceptance incomplete |
| Portable editing pack | Implemented clean-render workflow, SRTs, audio stems, original images and timing manifest; eight existing timeline/export-safety tests passed | Motion inside clips is baked, not native geometry; this audit did not regenerate every full media pack |
| Optional supplied audio | Audio preparation and FFmpeg mixing are implemented | Current native audio path requires the ordinary silent video render before stem mixing; no new listening test in this audit |
| Editable source | Prepared jobs contain Remotion source, configuration and assets | This source is separate from a Jianying/CapCut draft |
| Installation examples | Repository includes the instructions and implementation resources | No new end-to-end installation/render test in all four named host apps; local tools and permissions remain required |

## Corrections made

- Marked native drafts as a macOS preview at the feature introduction, not only in the compatibility paragraph.
- Distinguished MP4, editable Remotion source, portable editing pack and native Storybook draft. An MP4-only prompt does not request a native draft.
- Added native-draft dependencies, destination-path restrictions and the CapCut empty-project prerequisite.
- Corrected the audio prerequisite and scoped the Chinese replacement-menu wording to Jianying.
- Found that the locally installed skill still had six templates despite the repository documenting seven. Backed up the installed copy and synchronized tracked resources, including Flipstack, then validated both skill copies.

The native fold approximates curved paper, perspective and dynamic shadows. Text inside screenshot pixels is not a native text layer. Windows, other app versions and complete editing/export round trips are not established by this audit.

## All-effects portable preview implementation — 2026-11-15

The earlier audit above describes the previous Storybook-only release. The new `motion_native.py` adds six 2D native recipes and delegates Storybook to its existing exporter. Fresh exports covered all seven effects:

| Effect | Duration in this fixture | Native segments |
| --- | --- | --- |
| Spotlight | 12 s | 29 |
| Launch | 20 s | 58 |
| Orbit | 18 s | 81 |
| Kinetic | 16 s | 77 |
| Prism | 18 s | 69 |
| Flipstack | 20 s | 47 |
| Storybook | 15.8 s (2 pages) | 56 |

All segment material IDs resolve; target time ranges fit the composition; image and text materials are separate. The fixtures repeat a supplied screenshot and use generic sample copy, so they test export coverage rather than a finished product campaign. The matching original-render MP4s accompany the acceptance bundle, not the public repository.

The installer is standard-library Python and reconstructs paths at the destination. Automated tests exercise Windows-style input paths, Unicode media, missing/traversing/symlink media rejection, fresh legacy IDs, matching modern root/timeline payloads, empty-template guards and output non-overwrite. These tests run on this Mac; they are not Windows application tests.

Both local editors listed the new all-effects draft cards. Further native opening/visual checks were blocked by the computer-control service repeatedly returning `windowNotFoundAtPosition`; CapCut also temporarily returned a launch timeout. Changing window size and dismissing startup dialogs did not resolve the coordinate error. No new per-effect GUI acceptance is claimed. The earlier Storybook screenshots and results remain scoped to their earlier exporter, versions and checks.

The user has no Windows test machine and requested a Windows acceptance pack first. The bundle includes seven portable drafts, seven original-effect MP4 references, an installer, checksums and a 28-row effect × OS × editor acceptance sheet. Every row begins pending for this exact bundle. The native 2D approximation is visibly different in principle from the original renderer, especially Flipstack; native full-fidelity and complete editing/export round trips remain unverified.

Final local checks for this implementation: 12 unit tests passed; all seven portable sources installed into fresh temporary libraries for each of the two editor schemas (14 installs), with every referenced media file present. All seven reference MP4s probe as 1920×1080 at 30 fps with the expected frame counts; one representative rendered frame per effect was inspected. Orbit's generic sample headline approaches/overlaps a foreground card, so the fixture is not a polished copy-layout acceptance result. SHA-256 verification passed for all 89 bundled files. These results do not include native GUI playback or Windows execution.
