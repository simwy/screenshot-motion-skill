固定模板 + 可选 AI 文案 → 确定性生成引擎 → 静音 MP4 与可选普通草稿 ZIP。生成端无需 Codex 或剪映；`.jypack` 仅为显式请求时使用的客户端流程。见[程序入口与云端集成](references/engine.md)。

# screenshot-motion-skill — 截图转产品宣传视频

[English](README.md) | **简体中文**

**给 AI 编程助手几张截图，生成下一次产品发布的宣传视频。**

`screenshot-motion-skill` 是面向 Codex、Claude Code 等本地 AI 编程助手的开源技能：将 App、网站或 SaaS 产品截图制作成动画，撰写文案，并通过 Remotion 在本地渲染 1080p MP4 产品演示视频。

- **8 种动画风格**：卡片聚焦、暗色发布片、翻页故事书、环绕画廊、动态图形、棱镜折叠、卡片翻叠与轻扇形入场。
- **用自然语言修改**：调整标题、文案和效果，再生成视频。
- **可继续编辑**：交付 MP4 与剪映草稿，可继续替换截图和修改宣传文案。

[快速开始](#使用方法) · [交付内容](#交付内容) · [运行条件](#运行条件) · [常见问题](#常见问题)

## 动画效果

| Spotlight · 卡片聚焦 | Launch · 暗色发布片 |
| :---: | :---: |
| ![Spotlight](docs/previews/spotlight.gif) | ![Launch](docs/previews/launch.gif) |
| **Storybook · 翻页故事书** | **Orbit · 环绕画廊** |
| ![Storybook](docs/previews/storybook.gif) | ![Orbit](docs/previews/orbit.gif) |
| **Kinetic · 动态图形** | **Prism · 棱镜折叠** |
| ![Kinetic](docs/previews/kinetic.gif) | ![Prism](docs/previews/prism.gif) |
| **Flipstack · 卡片翻叠** | |
| ![Flipstack](docs/previews/flipstack.gif) | ![Entrance](docs/previews/entrance.gif) |

<sub>Flipstack：正常速度 · 20 fps · 完整 20 秒，保留翻叠过程。</sub>


<sub>以上为缩小、加速的静音预览。最终视频：1080p · 30 fps。</sub>


### 第 8 个模板：Entrance 轻扇形入场

选择 `entrance`，使用 5 张截图生成 8 秒视频：截图从下方沿轻微扇形逐张入场，左侧展示产品介绍，右侧功能说明依次点亮，再展开为大扇形，中央截图抬起并出现结尾标题。左右文案、卡片标签、品牌色和收尾文字均可配置。交付 1080p MP4；此模板暂不提供原生剪映/CapCut 草稿。[配置示例](examples/entrance.json) · [文案映射](references/templates.md#entrance--8-seconds)

## 使用方法

**1. 安装技能。** 在项目终端运行以下命令，按提示选择使用的 AI 助手：

```sh
npx skills add simwy/screenshot-motion-skill
```

安装完成后，在同一项目中新建任务。需要使用能够访问本地文件和执行命令的 AI 编程助手；渲染环境仍需满足下方的[运行条件](#运行条件)。

**2. 添加截图附件。** 在聊天输入框中上传 **5 张截图**。Storybook 支持 1–12 张截图。**截图和下一步的文字可以放在同一条消息里一起发送。**

**3. 填写应用信息并选择效果。** 将下面的示例粘贴到附有截图的消息中，替换应用名称和一句话介绍后发送。应用名称就是普通文字中的一行，无需单独填写表单或使用特殊命令。

```text
Use screenshot-motion-skill to make a promotional video from the attached screenshots.

App name: FocusFlow
Description: A task planner that helps people organize their day and stay focused.
Effect: orbit
```

将 `orbit` 替换为你喜欢的效果：**`spotlight` · `launch` · `storybook` · `orbit` · `kinetic` · `prism` · `flipstack` · `entrance`**。

`Description` 就是一句话描述应用做什么，也可以用中文填写。截图默认按附件上传顺序展示，AI 自动撰写简短文案。文案语言根据应用名称判断：中文或中英混合名称使用中文，英文名称使用英文，其他语言使用对应语言；描述所用语言不影响这一判断。如有需要，仍可明确指定其他顺序或文案语言。

使用上述指令，AI 会撰写文案、制作动画、检查结果，并交付 MP4、剪映草稿包和导入说明。随后你可以继续说：“修改主标题”，或“替换第三张截图”。

## 交付内容

- **MP4 视频**：可直接播放和分享，仅保留画面，不添加背景音乐或音效。
- **可选剪映草稿 ZIP**：包含截图素材、独立文案和安装脚本；解压后安装到草稿目录，不是 `.jypack`。

渲染项目和源文件由 skill 内部保留，用于后续修改，不作为默认交付内容。

## 运行条件

需要能访问本地文件、执行命令的 AI 编程助手，以及 **Python 3.9+、Node.js 22+、npm、Chrome / Chromium 和 FFmpeg**。由助手检查环境并执行渲染；首次运行需要安装依赖。详见[环境配置](references/development.md)。

普通草稿生成另需 pyJianYingDraft 0.2.7 和 Pillow，不需要剪映客户端；可选的 `.jypack` 由客户端“备份草稿及素材”生成。接收端需具备“导入剪映草稿”功能。

## 在剪映中继续创作：换截图、改书页文字

**原有 7 种效果可生成剪映原生可编辑草稿。** 下图为此前在 macOS 实测的 Storybook 草稿。 生成视频后，还可以在剪映里替换产品截图、调整书页文案，并继续剪辑。

![Mac 剪映中的 Storybook 原生草稿：书页预览与独立文字轨道](docs/previews/jianying-storybook-editable.jpg)

<sub>Mac 剪映 11.8.0 实机截图。上方是书页效果，下方是独立文字轨道；图片、纸张和背景也分别位于各自的图层中。</sub>

- **替换截图**：截图作为独立图片片段导入；使用“替换片段”并勾选“复用原视频效果”，保留位置和关键帧。
- **修改书页文字**：封面标题、正文、章节、页码都是原生文字片段，可在剪映文本面板中调整。
- **保留书本布局**：封面、左右页、配色和装饰按模板布局导出，页面切换使用同步关键帧。

### 可选：通过客户端导出及导入 .jypack

1. 下载生成的 `.jypack` 文件，**无需解压**。
2. 打开剪映桌面版，在首页选择 **导入剪映草稿**。
3. 选择该文件，完成导入后打开草稿继续编辑。

草稿包由剪映客户端通过“备份至本地 → 备份草稿及素材”生成，素材随包携带。仅在明确要求此格式时交付 **MP4 + `.jypack`**。默认交付 MP4，也可选用无需客户端生成的普通草稿 ZIP。原有七种模板提供草稿导出；Entrance 当前交付 MP4。

直接对 AI 说：

```text
用选定的特效制作视频，交付 MP4 和包含素材的剪映 .jypack 草稿。
我需要通过剪映首页的“导入剪映草稿”打开，并继续替换截图、修改文案。
```

生成草稿包需要本机剪映及客户端操作能力。Mac 和 Windows 接收端均需提供对应导入功能；请使用具备此功能的版本。仅需视频时可说“仅导出 MP4”；CapCut 请单独指定。[开发者导出说明 →](references/jianying-jypack.md)

## 使用须知

- 默认输出为 **1080p、30 fps、横屏**。Spotlight：12 秒；Launch：20 秒；Orbit：18 秒；Kinetic：16 秒；Prism：18 秒；Flipstack：20 秒；Storybook：5 页时为 32 秒，可调整停留时长。
- 请使用清晰的截图和简短文案。若要修改截图内部的文字，需要提供更新后的图片。
- 技能不附带音频；请提供你有权使用的文件。AI 会检查本地渲染所需工具。[环境配置说明（英文）→](references/development.md)
- 原创代码采用 MIT 许可证；Remotion 和媒体素材适用各自的条款。[许可证详情（英文）→](THIRD_PARTY_NOTICES.md)

## 常见问题

### 这是网页应用吗？

这是安装在本地 AI 编程助手中的 Skill。上传截图并在聊天中提出需求，由助手运行本地脚本生成视频；它不是托管的在线视频编辑器。

### 需要额外的视频生成 API Key 吗？

模板视频通过本地 Remotion 渲染，不需要视频生成服务的 API Key。你使用的 AI 助手仍需要自己的账号或模型配置，相关服务可能收费。

### 可以免费使用或用于商业项目吗？

本仓库原创代码采用 MIT 许可证。Remotion、AI 助手以及你使用的图片、字体、音频适用各自条款；商业用途请查看[第三方许可说明](THIRD_PARTY_NOTICES.md)。

### 可以修改截图里面的文字吗？

视频上的独立标题和文案可以修改；截图中的文字属于图片像素，需要提供更新后的截图。原生草稿的截图替换、文字编辑及保存导出支持情况见[兼容性说明](references/editor-export.md)。

### 可以添加背景音乐吗？

目前仅生成画面，不添加背景音乐或音效。

## 扩展更多效果

模板库可以持续增加新效果，无需替换已有模板。[贡献新效果（英文）→](references/extending.md)

技能仅附带轻量 GIF 预览及中英文版对应的剪映、CapCut 实机展示截图。完整演示视频、原始截图、运行依赖和生成的编辑素材包不包含在安装内容中。[预览说明（英文）→](docs/previews/README.md)

如果这个技能对你有帮助，欢迎点一个 **Star**，方便下次产品发布时找到它。遇到问题请[提交 Issue](https://github.com/simwy/screenshot-motion-skill/issues)，并附上所用工具、系统、模板名称和报错信息。请勿附带密钥或私人素材。
