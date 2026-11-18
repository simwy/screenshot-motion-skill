#!/usr/bin/env python3
"""Agent-free worker entry point. Stdout is one JSON result; logs go to stderr."""
import argparse
import contextlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from engine import prepare, render, finalize, run, ROOT


def generate(config, out, template=None, browser=None, draft=False):
    """Run in an isolated worker with trusted, locally staged assets.

    Does not call an LLM, install an editor, or upload anything. Failures propagate
    to the caller; a completed MP4 is retained if optional draft export fails.
    """
    out = Path(out).resolve()
    config = Path(config).resolve()
    if out.exists():
        raise ValueError(f'Refusing to overwrite output: {out}')
    if draft:
        selected = template or json.loads(config.read_text()).get('template', 'storybook')
        if selected == 'entrance':
            raise ValueError('Entrance has no native draft recipe; request MP4 only')
        # Fail before expensive rendering if optional dependencies are missing.
        import motion_native
    job = prepare(config, out / 'job', template)
    run(['npm', 'ci'], job)
    render(job, browser, None)
    video = finalize(job)
    result = {'video': str(video), 'project': str(job / 'project.json')}
    if draft:
        from install_editor_draft import media_relative
        source = out / 'native'
        motion_native.export(job, source)
        run(['ffmpeg', '-v', 'error', '-ss', '1', '-i', video,
             '-frames:v', '1', '-vf', 'scale=640:-2', source / 'draft_cover.jpg'])
        # Use relative media references in the portable download. The installer
        # resolves them to destination-machine paths without needing Codex.
        with tempfile.TemporaryDirectory(dir=out) as folder:
            stage = Path(folder)
            target = stage / 'draft'
            shutil.copytree(source, target)
            content = target / 'draft_content.json'
            payload = json.loads(content.read_text())
            for kind in ('videos', 'audios'):
                for material in payload['materials'].get(kind, []):
                    material['path'] = 'media/' + media_relative(material['path'], source).as_posix()
            content.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
            meta_path = target / 'draft_meta_info.json'
            meta = json.loads(meta_path.read_text())
            meta.update(draft_fold_path='', draft_root_path='', draft_cover='draft_cover.jpg')
            meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding='utf-8')
            shutil.copy2(ROOT / 'scripts/install_editor_draft.py', stage)
            (stage / 'README.txt').write_text(
                'This is an installer ZIP, not a .jypack. Unzip first. Python 3 is required.\n'
                'Run: python3 install_editor_draft.py --source draft --editor jianying --out /path/to/NEW-draft-folder\n'
                'Install draft/ into a NEW directory in your Jianying draft library.\n'
                'Never overwrite an existing project. Save work and restart Jianying after installation to refresh its draft list.\n', encoding='utf-8')
            archive = shutil.make_archive(str(out / 'jianying-draft'), 'zip', stage)
        result['draftZip'] = archive
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--template')
    parser.add_argument('--browser')
    parser.add_argument('--draft', action='store_true')
    args = parser.parse_args()
    try:
        with contextlib.redirect_stdout(sys.stderr):
            result = generate(args.config, args.out, args.template, args.browser, args.draft)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, ImportError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
