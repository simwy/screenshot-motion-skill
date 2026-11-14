#!/usr/bin/env python3
"""Bundle generated native drafts and matching MP4 references for destination QA.

No renderer or editor dependencies; Python 3.9+. Never overwrites an output.
"""
import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path
from install_editor_draft import media_relative


def bundle(drafts, jobs, out):
    drafts, jobs, out = (Path(p).resolve() for p in (drafts, jobs, out))
    if out.exists():
        raise FileExistsError(out)
    names = [p.name for p in sorted(drafts.iterdir()) if (p/'draft_content.json').is_file()]
    if not names:
        raise ValueError('No native drafts found')
    # Validate every input before creating an output folder.
    payloads = {}
    for name in names:
        source = drafts/name
        payload = json.loads((source/'draft_content.json').read_text(encoding='utf-8'))
        job = json.loads((jobs/name/'project.json').read_text(encoding='utf-8'))
        if job['template'] != name:
            raise ValueError('Draft directory must match the job template: '+name)
        reference = jobs/name/'out/video-silent.mp4'
        if not reference.is_file() or reference.stat().st_size == 0:
            raise ValueError('Render the matching reference first: '+str(reference))
        for kind in ('videos', 'audios'):
            for material in payload['materials'].get(kind, []):
                rel = media_relative(material['path'], source)
                material['path'] = 'media/'+rel.as_posix()
        payloads[name] = payload
    out.mkdir(parents=True)
    try:
        (out/'references').mkdir()
        for name, payload in payloads.items():
            target = out/'drafts'/name
            target.mkdir(parents=True)
            shutil.copytree(drafts/name/'media', target/'media')
            (target/'draft_content.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
            meta = json.loads((drafts/name/'draft_meta_info.json').read_text(encoding='utf-8'))
            meta.update(draft_fold_path='', draft_root_path='', draft_name=name)
            (target/'draft_meta_info.json').write_text(json.dumps(meta, ensure_ascii=False), encoding='utf-8')
            if (drafts/name/'EDITING.md').is_file():
                shutil.copy2(drafts/name/'EDITING.md', target/'EDITING.md')
            shutil.copy2(jobs/name/'out/video-silent.mp4', out/'references'/(name+'.mp4'))
        here = Path(__file__).parent
        for file in ('install_editor_draft.py', 'install_editor_bundle.py'):
            shutil.copy2(here/file, out/file)
        shutil.copy2(here.parent/'references/windows-acceptance.md', out/'START-HERE.md')
        with (out/'acceptance.csv').open('w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['effect','os','editor','version','open','preview','replace_image','edit_text','save_reopen','export_mp4','notes'])
            for name in names:
                for os in ('macOS','Windows'):
                    for editor in ('jianying','capcut'):
                        writer.writerow([name,os,editor,'']+['pending']*6+['This exact bundle has not passed client acceptance'])
        manifest = {'effects':names,'nativeMode':'editable 2D approximation','referenceMode':'original rendered effect; baked pixels','clientAcceptance':'pending','files':{}}
        for path in sorted(out.rglob('*')):
            if path.is_file():
                manifest['files'][path.relative_to(out).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        (out/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    except Exception:
        shutil.rmtree(out)
        raise
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('drafts','jobs','out'):
        parser.add_argument('--'+flag, type=Path, required=True)
    args = parser.parse_args()
    print(bundle(args.drafts, args.jobs, args.out))
