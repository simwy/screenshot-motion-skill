# SYTASK App demo assets

## 固定 App 演示素材

- 本项目官网、README、效果开发与回归检查中的 App 演示必须使用 `screenshots/` 的 SYTASK 英文截图，顺序以 `manifest.json` 为准。不得从旧 job、prototype、临时目录或中文截图中自行选图。
- 固定素材为 5 张：Home、Progress、Members、Profile、Create task。演示素材数量不等于引擎的通用输入限制；根据各模板声明的数量范围使用，不得用复制图片冒充额外截图。
- 演示标题、标签和说明统一英文。GIF 与 MP4 必须由同一个配置和同一套截图生成；替换截图后必须重新渲染，不能只修改页面标签或转码旧视频。
- 每次交付前核对截图清单和哈希，检查视频中的界面语言、说明文字与动效中间帧。网站 MP4 按当前要求最多 8 秒、720p、30 fps、无音轨，截取不加速。
- 这些素材仅作为本项目公开演示的固定样本，不替代客户任务明确提供的截图，不将 SYTASK 品牌素材作为通用可再授权素材。

素材来源：AI-Sytask2-Mobile/store-screenshots/english/android-1080x1920。根据项目所有者要求作为本项目演示素材收录。SYTASK 品牌与截图不随代码 MIT 许可重新授权。

## 截图数量检查（2026-11-18）

已实际调用 prepare 检查 3 张与 6 张：Storybook 均通过（声明范围 1–12）；Entrance、Spotlight、Launch、Orbit、Kinetic、Prism、Flipstack 均拒绝（当前范围 5–5）。渲染代码还包含固定中心索引、五等分角度、固定场景时间和页面索引。支持可变数量必须同时适配这些逻辑及编辑草稿导出，不能只修改 registry。
