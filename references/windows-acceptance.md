# All-effects desktop editor acceptance pack / 全特效桌面编辑器验收包

This pack targets Jianying and CapCut on macOS and Windows. **Windows client acceptance is pending.** A successful install only verifies file generation. Record the exact OS and app build in `acceptance.csv`; all 28 combinations start pending for this bundle.

本包面向 macOS / Windows 的剪映和 CapCut，包含全部已生成效果。**Windows 尚无实机验收结果**，安装成功不代表客户端兼容。请逐项填写 `acceptance.csv`，记录系统和客户端完整版本。

## Contents / 内容

- `drafts/<effect>`: separate native screenshot and text segments, with 2D keyframes. Storybook retains its native book layout; the other effects use experimental 2D reconstructions. These are not pixel-identical replicas. Perspective, mesh bending, lighting, shadows, blur, crop regions and typography can differ. Flipstack's reconstruction is particularly simplified.
- `references/<effect>.mp4`: full original renderer output for comparison, also importable as an ordinary video for faithful playback. These reference videos have baked pixels; replacing a screenshot inside them requires rerendering.
- `install_editor_bundle.py`: installs every effect with destination-native absolute media paths. Python 3.9+ standard library only; no Node, FFmpeg, Pillow or pyJianYingDraft needed to install the pack.
- `manifest.json`: SHA-256 checksums and exact effect list.

原生草稿可以改字、换图，但属于二维近似；完整三维/翻页效果以参考视频为准。Orbit 为保持遮挡顺序，将同一截图拆成多个片段，换图时须替换所有对应片段，或让 skill 重新生成。截图里的 UI 文字仍是图片像素。

## Install on Windows / Windows 安装

1. Extract the whole ZIP to a permanent local folder. Install Python 3.9+ if needed.
2. Create and close a **new empty project** in the target editor. Read its draft storage location from that editor's settings. Save your existing work and exit the editor before installation.
3. Open PowerShell in this extracted folder. Set the actual library path; the examples below are placeholders, not assumed default paths.

```powershell
$draftRoot = 'D:\Actual\DraftLibrary'
py -3 .\install_editor_bundle.py --editor jianying --root "$draftRoot" --prefix 'Motion QA'
```

For CapCut, also supply the path of the empty project created by **that exact installed build**:

```powershell
$emptyProject = 'D:\Actual\DraftLibrary\Empty QA Project'
py -3 .\install_editor_bundle.py --editor capcut --root "$draftRoot" --template "$emptyProject" --prefix 'Motion QA'
```

剪映默认生成独立旧格式草稿。若客户端不识别，可以另建空项目并使用 `--template` 适配其可读 JSON 格式。CapCut 必须提供本机空项目。**遇到加密或不支持的格式，安装器会停止；不能通过重命名、覆盖加密文件来解决。** 不要用已有作品当模板。脚本拒绝覆盖目标目录；再次测试请更换 `--prefix`。

4. Restart the editor. Look for `Motion QA <effect>` in local projects. A card appearing on the home screen is not sufficient: actually open it and scrub its timeline. If a project is missing, recheck the library path. If it appears but cannot open, record that failure and exact version; do not mark compatible.
5. If native loading fails, import the matching MP4 from `references` to compare the original effect. This is a reference-only fallback, not completion of native editing acceptance.

## Install on macOS / macOS 安装

Use the same scripts with `python3`, POSIX paths and the library actually configured by the app:

```sh
python3 install_editor_bundle.py --editor jianying --root '/actual/draft/library' --prefix 'Motion QA'
python3 install_editor_bundle.py --editor capcut --root '/actual/draft/library' --template '/actual/empty/project' --prefix 'Motion QA'
```

Do not move installed folders afterward: media paths are absolute. Reinstall the original portable pack into a new final destination instead. Templates and source drafts are read-only; installation creates new folders and does not change the library index.

## Acceptance / 验收步骤

Run separately for each effect and each app/OS combination. Use a test copy for edits.

1. **Open**: no crash, missing media or unsupported-project warning; correct duration and 1920×1080 canvas.
2. **Preview**: scrub opening, feature holds, transitions and closing; compare with the matching reference. Record visual differences, clipping and layer order. A black initial frame can be an entrance fade; check a hold as well.
3. **Replace image**: replace one native screenshot with a clearly different image, preserve effects/keyframes, verify position and transitions. In Jianying retain “复用原视频效果”; verify CapCut's local replacement controls. Orbit requires replacing all split occurrences.
4. **Edit text**: edit a native text segment in its text panel. Check readability, line breaks and no clipping. Screenshot UI text is not independently editable.
5. **Save/reopen**: save, return home, reopen; verify image and text edits survived, and media still resolves.
6. **Export MP4**: export full duration locally and play the actual output, checking beginning/middle/end and audio when present. Record file name, resolution and duration.

填写 `pass` / `fail`，保留未执行项的 `pending`，在 notes 中记录差异和截图证据。不要把参考视频导入成功计为原生草稿验收通过。不要把 macOS、剪映或某个效果的结果复制给 Windows、CapCut 或其他效果。
