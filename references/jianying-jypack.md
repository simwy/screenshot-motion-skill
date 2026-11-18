# Jianying native import delivery

Deliver `<project>.mp4` and `<project>.jypack`. Use this workflow for the original seven templates; Entrance has no native recipe. CapCut is a separate explicit workflow.

1. Generate the selected template with `scripts/motion_native.py --job <job> --out <new-source>`. Use the isolated Python environment documented in editor-export.md. Keep source, temporary media and QA outside the installed skill and final delivery folder.
2. Discover the installed Jianying application, version and configured local draft directory. Use `scripts/install_editor_draft.py` to stage a uniquely named draft at its final library path, rebasing media references. Never overwrite an existing draft. macOS and Windows use different library paths; discover them instead of hardcoding another machine’s home or drive.
3. Open the staged draft in Jianying and check its timeline, text, images and media availability. Save the generated project. Do not interrupt or close unrelated user edits.
4. On the home screen, open this draft’s menu → **备份至本地 → 备份草稿及素材**. Use the available computer-use tool. Do not select “仅备份草稿”, which omits media. This client step creates the native interchange package; Python JSON generation alone does not.
5. In the save dialog, navigate to the delivery directory using the location control / Go to Folder, then enter only the filename. On macOS, putting a full path into the filename field can save a colon-containing filename in the wrong directory. Wait for the backup task to finish and verify the actual `.jypack` exists and is nonempty.
6. Import the resulting file through **导入剪映草稿** into a separate copy where possible. Check image availability, text and timeline. Never overwrite the source for a verification run. Record the OS, app version, template and checks internally; distinguish agent-observed results from user feedback.
7. Return links to the MP4 and `.jypack`, with this short instruction: “剪映首页 → 导入剪映草稿 → 选择 .jypack 文件，无需解压。” Do not ship installer scripts, render source, acceptance CSVs or internal reports as extra deliverables.

If native backup is unavailable or automation fails, preserve the completed video and staging draft, report the exact blocker, and request only the manual client step needed. Do not label an installer ZIP as an importable draft or silently change the deliverable. A client without this feature needs an explicitly chosen legacy installation workflow. Do not promise all historical versions support native import.

## Internal evidence

On 2026-11-18, macOS Jianying 11.8.0 exported a Storybook draft through “备份草稿及素材”. The user subsequently reported the delivered draft/effect was usable. This is user feedback on that sample, not a complete test of every edit/save/export operation, template, Windows build or historical version.

The application declares `.jypack` as `application/vnd.bytedance.jypack`. The observed package has JY archive signatures and non-plaintext draft payloads. Renaming an ordinary ZIP, rewriting signatures or inventing encryption is not the supported generation route. Use the client’s own exporter.
