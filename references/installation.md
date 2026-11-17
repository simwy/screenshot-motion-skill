# Installation and host compatibility

Repository: https://github.com/simwy/screenshot-motion-skill

Install the entire repository, including `assets/`, `scripts/`, `references/`, and `templates.json`. Copying only `SKILL.md` will not provide the renderers. The published repository must have `SKILL.md` at its root, not inside a second `screenshot-motion-skill/` folder.

## skills CLI

From your project terminal, run:

```sh
npx skills add simwy/screenshot-motion-skill
```

Follow the prompts to select your agent and installation scope. To inspect the publicly available skill without installing it:

```sh
npx skills add simwy/screenshot-motion-skill --list
```

The CLI must copy the supporting files as well as `SKILL.md`; use the verification checklist below. Rendering dependencies are installed separately.

[CLI documentation](https://skills.sh/docs/cli). The skills.sh leaderboard uses CLI installation telemetry; a working installation command does not guarantee a listing or ranking.

## Codex

Paste the README's `$skill-installer` instruction into Codex chat. Codex's installer can download a skill from another GitHub repository. For this root-level repository, its helper uses the repository root as the skill path and `screenshot-motion-skill` as the installed directory name. Let the installed helper choose its configured user skill location.

For a project-local terminal installation, clone into `.agents/skills/screenshot-motion-skill` from the project root. Current official documentation identifies `.agents/skills/` as a project discovery location. Select `$screenshot-motion-skill` or name the skill in your request. If discovery has not refreshed, start a new task or restart Codex.

Source: [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Claude Code

Paste the README's installation request into Claude Code chat. The agent installs the full repository into `.claude/skills/screenshot-motion-skill` in the current project. Claude Code supports directory-based skills with a `SKILL.md` entry point and supporting files. Start a new task in the same project after installation.

Use the plain-language request in the README, or invoke `/screenshot-motion-skill` followed by your request. This guidance is for Claude Code with access to local files and commands; it does not claim that the same rendering workflow has been verified in ordinary Claude web chat or Cowork.

Source: [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

## WorkBuddy

The README's chat instruction asks the agent to perform a **filesystem installation for the current project**. It is not a marketplace installer command. WorkBuddy documents `.codebuddy/skills/` as its project-level skill location for local code-development workspaces. Use a project with local file/terminal access; installing here does not enable the skill in every other WorkBuddy project.

If that workflow is unavailable, use the documented skill upload interface: Experts · Skills · Connectors → Skills → Add Skill → Upload Skill. Download the repository, keep the complete skill folder together, and import a skill archive accepted by your version. WorkBuddy's documented conversational marketplace installation only covers marketplace entries; this repository is not claimed to be listed there.

Sources: [WorkBuddy project configuration](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project), [WorkBuddy skill installation and upload](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market).

## DeepSeek Harness

Use the README's chat instruction or clone into `.dsh/skills/screenshot-motion-skill` at the active project root. The shipped filesystem skill provider discovers `<name>/SKILL.md` directory bundles there. Name `screenshot-motion-skill` in your request; do not assume Codex's dollar-prefix syntax is a portable slash command.

The provider uses the nearest Git repository root, or the working directory when no Git root exists. Open your task at the same root where you installed the skill. Custom DSH profiles must include the filesystem skill provider and skill consumer; a profile without them cannot discover local skills merely because files exist.

Source: [DeepSeek Harness skill subsystem](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md).

## Optional terminal installation

With Git installed, run the command for your app from the active project's root folder. These are project-local installations; Git refuses to clone over an existing nonempty directory.

| App | Terminal command |
| --- | --- |
| Codex | `git clone --depth 1 https://github.com/simwy/screenshot-motion-skill.git .agents/skills/screenshot-motion-skill` |
| Claude Code | `git clone --depth 1 https://github.com/simwy/screenshot-motion-skill.git .claude/skills/screenshot-motion-skill` |
| WorkBuddy | `git clone --depth 1 https://github.com/simwy/screenshot-motion-skill.git .codebuddy/skills/screenshot-motion-skill` |
| DeepSeek Harness | `git clone --depth 1 https://github.com/simwy/screenshot-motion-skill.git .dsh/skills/screenshot-motion-skill` |

These Git commands use syntax accepted by macOS/Linux shells and Windows PowerShell. Start a new task in the same project after installation.

## Verify installation

The agent should verify that:

- `<installed-folder>/SKILL.md` exists and declares `name: screenshot-motion-skill`.
- `templates.json`, `scripts/motion.py` and `assets/video-template/` exist beside it.
- The host discovers the skill in a task using the intended project.

If an installation already exists, do not delete or overwrite it just to rerun the clone command. For a Git checkout, review local changes before updating. Dependencies are installed later in the generated video job, not into the skill folder.

These instructions are based on official host documentation checked on 2026-11-13. They do not imply an end-to-end rendering test inside all four apps. The skill needs local file access and command execution; installing it alone does not supply Python, Node.js, Chrome, or FFmpeg. See the [runtime guide](development.md).

## Publishing this repository

Publish the **contents** of the local `screenshot-motion-skill` folder at the repository root. A repository containing only a license cannot yet be installed as this skill. After publishing, verify the public root `SKILL.md` and use a fresh temporary directory for a download check before announcing installation support. Publishing is a separate maintainer action; the README does not upload anything automatically.
