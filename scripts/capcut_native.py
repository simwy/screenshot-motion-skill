#!/usr/bin/env python3
"""Package a native Storybook draft using an empty local CapCut timeline schema.

Preview compatibility: CapCut macOS 9.7.1. Never modifies the source/template.
"""
import argparse
import copy
import json
import shutil
import uuid
from pathlib import Path


def package(source: Path, template: Path, out: Path):
    source, template, out = (p.resolve() for p in (source, template, out))
    src = json.loads((source / 'draft_content.json').read_text())
    dst = json.loads((template / 'draft_info.json').read_text())
    project = json.loads((template / 'Timelines/project.json').read_text())
    meta = json.loads((template / 'draft_meta_info.json').read_text())
    if dst.get('tracks') or dst.get('duration'):
        raise ValueError('Template must be a newly created empty CapCut project')
    if any(dst.get('materials', {}).values()):
        raise ValueError('Template must contain no materials')
    if len(project.get('timelines', [])) != 1:
        raise ValueError('Template must have exactly one empty timeline')
    if out.exists():
        raise FileExistsError(out)
    # Native exporter owns these files; reject references outside its media folder.
    for kind in ('videos', 'audios'):
        for item in src['materials'].get(kind, []):
            path = Path(item['path']).resolve()
            path.relative_to(source / 'media')
            if not path.is_file():
                raise FileNotFoundError(path)
    tid = str(uuid.uuid4()).upper()
    for key in ('tracks', 'duration', 'fps', 'canvas_config', 'keyframes'):
        if key in src:
            dst[key] = copy.deepcopy(src[key])
    dst['materials'].update(copy.deepcopy(src['materials']))
    dst['id'] = tid
    for kind in ('videos', 'audios'):
        for item in dst['materials'].get(kind, []):
            item['path'] = str(out / Path(item['path']).resolve().relative_to(source))
    project['id'] = str(uuid.uuid4()).upper()
    project['main_timeline_id'] = tid
    project['timelines'][0]['id'] = tid
    meta.update(draft_id=str(uuid.uuid4()).upper(), draft_name=out.name,
                draft_fold_path=str(out), draft_root_path=str(out.parent),
                tm_duration=src['duration'])
    out.mkdir(parents=True)
    shutil.copytree(source / 'media', out / 'media')
    (out / 'Timelines' / tid).mkdir(parents=True)
    for path, data in ((out / 'draft_info.json', dst),
                       (out / 'Timelines' / tid / 'draft_info.json', dst),
                       (out / 'Timelines/project.json', project),
                       (out / 'draft_meta_info.json', meta)):
        path.write_text(json.dumps(data, ensure_ascii=False))
    (out / 'EDITING.md').write_text('''# Editable Storybook for CapCut
Select a text segment to edit its copy in Text > Basic. Each line is separate.
Screenshots are native image segments. Preserve effects/keyframes when replacing
an image, then check its fit and the page turn. Longer copy may need resizing.
Horizontal folds approximate the rendered effect; curved paper, perspective and
dynamic shadows are not identical. Text inside screenshots requires a new image.
Media paths are absolute: regenerate at the final destination after moving.
Preview tested in CapCut macOS 9.7.1: opening, page layout and text panel.
Screenshot replacement, text-edit/save/reopen and final export need acceptance.
''')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('source', 'template', 'out'):
        parser.add_argument('--' + flag, type=Path, required=True)
    args = parser.parse_args()
    print(package(args.source, args.template, args.out))
