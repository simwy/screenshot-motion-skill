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
