# screenshot-motion-skill

[English](README.md) | **简体中文**

**用你的截图，制作下一次产品发布的宣传视频。**

这个 AI 技能可以将截图制作成动画，撰写字幕文案，并交付 MP4 视频。Storybook 还可导出剪映原生可编辑草稿，让你继续替换截图、修改书页文字；其他模板可导出桌面编辑素材包。

## 动画效果

| Spotlight · 卡片聚焦 | Launch · 暗色发布片 |
| :---: | :---: |
| ![Spotlight](docs/previews/spotlight.gif) | ![Launch](docs/previews/launch.gif) |
| **Storybook · 翻页故事书** | **Orbit · 环绕画廊** |
| ![Storybook](docs/previews/storybook.gif) | ![Orbit](docs/previews/orbit.gif) |
| **Kinetic · 动态图形** | **Prism · 棱镜折叠** |
| ![Kinetic](docs/previews/kinetic.gif) | ![Prism](docs/previews/prism.gif) |

<sub>以上为缩小、加速的静音预览。最终视频：1080p · 30 fps。</sub>

## 在剪映中继续创作：换截图、改书页文字

**Storybook 可导出剪映原生可编辑草稿。** 生成视频后，还可以在剪映里替换产品截图、调整书页文案，并继续剪辑。

![Mac 剪映中的 Storybook 原生草稿：书页预览与独立文字轨道](docs/previews/jianying-storybook-editable.jpg)

<sub>Mac 剪映 11.8.0 实机截图。上方是书页效果，下方是独立文字轨道；图片、纸张和背景也分别位于各自的图层中。</sub>

- **替换截图**：截图作为独立图片片段导入；使用“替换片段”并勾选“复用原视频效果”，保留位置和关键帧。
- **修改书页文字**：封面标题、正文、章节、页码都是原生文字片段，可在剪映文本面板中调整。
- **保留书本布局**：封面、左右页、配色和装饰按模板布局导出，页面切换使用同步关键帧。

直接对 AI 说：

```text
用 Storybook 制作视频，并导出剪映原生可编辑草稿。
我需要在剪映里替换截图、修改封面和书页文字，尽量保留原版布局与效果。
```

**当前范围：** 原生可编辑模式仅支持 Storybook。已在 Mac 剪映 11.8.0 验证草稿打开、版式显示和截图替换；文字修改后的保存重开与成片导出尚未完整验收。翻页以原生水平折页近似，纸张弯曲、透视和动态阴影不与渲染版完全一致。Windows 和 CapCut 未验证。[编辑与兼容性说明 →](references/editor-export.md)

## 使用方法

**1. 安装技能。** 在你使用的工具中打开一个本地项目，将对应指令粘贴到它的**聊天输入框**中：

| 工具 | 复制这段指令进行安装 |
| --- | --- |
| **Codex** | $skill-installer 将 https://github.com/simwy/screenshot-motion-skill 安装为 screenshot-motion-skill。 |
| **Claude Code** | 将 https://github.com/simwy/screenshot-motion-skill 安装到当前项目的 .claude/skills/screenshot-motion-skill 目录。 |
| **WorkBuddy** | 将 https://github.com/simwy/screenshot-motion-skill 安装到当前项目的 .codebuddy/skills/screenshot-motion-skill 目录。 |
| **DeepSeek Harness** | 将 https://github.com/simwy/screenshot-motion-skill 安装到当前项目的 .dsh/skills/screenshot-motion-skill 目录。 |

AI 确认安装完成后，在同一项目中新建任务。以上说明适用于能够访问本地文件和执行命令的 AI 工具；这里的“Claude”指 **Claude Code**。[安装帮助（英文）→](references/installation.md)

**2. 添加截图附件。** 在聊天输入框中上传 **5 张截图**。Storybook 支持 1–12 张截图。**截图和下一步的文字可以放在同一条消息里一起发送。**

**3. 填写应用信息并选择效果。** 将下面的示例粘贴到附有截图的消息中，替换应用名称和一句话介绍后发送。应用名称就是普通文字中的一行，无需单独填写表单或使用特殊命令。

```text
使用 screenshot-motion-skill，把附件中的截图制作成宣传视频。

App 名称：诗柚古文
一句话介绍：一款帮助学生轻松学习古诗词和文言文的 App。
效果：orbit
文案语言：英文，请自动撰写简短文案。
输出：导出 MP4。
截图顺序：请按附件上传顺序展示。
```

将 `orbit` 替换为你喜欢的效果：**`spotlight` · `launch` · `storybook` · `orbit` · `kinetic` · `prism`**。

指令可以用中文；如果希望视频使用中文文案，将“文案语言”改成“中文”即可。

AI 会撰写文案、制作动画、检查结果并交付视频。随后你可以继续说：“修改主标题”，或“再导出一份用于剪映或 CapCut 的编辑素材包”。

## 交付内容

- **制作完成的 MP4 视频**和可编辑的源项目。
- **可选的音乐与音效**，使用你提供的音频文件。
- **可选的编辑素材包**，包含不带字幕的动画片段、可编辑的 SRT 字幕、独立音轨以及原始截图。

- **可选的 Storybook 剪映原生草稿**，含可替换截图、独立文字图层和页面关键帧。具体兼容性与验证范围见上方展示区。

## 使用须知

- 默认输出为 **1080p、30 fps、横屏**。Spotlight：12 秒；Launch：20 秒；Orbit：18 秒；Kinetic：16 秒；Prism：18 秒；Storybook：5 页时为 32 秒，可调整停留时长。
- 请使用清晰的截图和简短文案。若要修改截图内部的文字，需要提供更新后的图片。
- 技能不附带音频；请提供你有权使用的文件。AI 会检查本地渲染所需工具。[环境配置说明（英文）→](references/development.md)
- 原创代码采用 MIT 许可证；Remotion 和媒体素材适用各自的条款。[许可证详情（英文）→](THIRD_PARTY_NOTICES.md)

## 扩展更多效果

模板库可以持续增加新效果，无需替换已有模板。[贡献新效果（英文）→](references/extending.md)

技能仅附带轻量 GIF 预览和剪映实机展示截图。完整演示视频、原始截图、运行依赖和生成的编辑素材包不包含在安装内容中。[预览说明（英文）→](docs/previews/README.md)
