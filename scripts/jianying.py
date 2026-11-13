#!/usr/bin/env python3
"""Experimental standalone Jianying legacy draft. Never installs into an editor automatically."""
import argparse
import json
from pathlib import Path
import shutil
import sys


def export_draft(pack, out):
    try:
        import pyJianYingDraft as draft
    except ImportError as exc:
        raise ValueError('Optional adapter requires pyJianYingDraft==0.2.7 in an isolated environment') from exc
    pack,out=pack.resolve(),out.resolve()
    if out.exists():raise ValueError(f'Refusing to overwrite: {out}')
    d=json.loads((pack/'timeline.json').read_text())
    if d.get('schemaVersion') != 1:raise ValueError('Unsupported edit-pack schema')
    for relative in [c['file'] for c in d['clips']]+list(d['audio'].values()):
        source=(pack/relative).resolve()
        if not source.is_relative_to(pack) or not source.is_file():raise ValueError(f'Missing or unsafe material: {relative}')
    us=lambda frame:round(frame*1_000_000/d['fps'])
    out.parent.mkdir(parents=True,exist_ok=True)
    created=False
    try:
        script=draft.DraftFolder(str(out.parent)).create_draft(out.name,d['width'],d['height'],fps=d['fps'],maintrack_adsorb=False)
        created=True
        shutil.copytree(pack/'clips',out/'media/clips')
        shutil.copytree(pack/'audio',out/'media/audio')
        script.add_track(draft.TrackType.video,'Motion plates')
        for c in d['clips']:
            start,end=us(c['startFrame']),us(c['endFrame'])
            script.add_segment(draft.VideoSegment(str(out/'media'/c['file']),draft.trange(start,end-start),volume=0),'Motion plates')
        for role in ['title','body']:
            script.add_track(draft.TrackType.text,role)
            for c in d['captions']:
                start,end=us(c['startFrame']),us(c['endFrame'])
                script.add_segment(draft.TextSegment(c[role],draft.trange(start,end-start),
                    style=draft.TextStyle(size=9 if role=='title' else 6,bold=role=='title',align=1,auto_wrapping=True,max_line_width=.82),
                    border=draft.TextBorder(color=(0,0,0),width=20),
                    clip_settings=draft.ClipSettings(transform_y=-.65 if role=='title' else -.82)),role)
        for name,relative in d['audio'].items():
            script.add_track(draft.TrackType.audio,name)
            script.add_segment(draft.AudioSegment(str(out/'media'/relative),draft.trange(0,us(d['durationFrames']))),name)
        script.save()
        meta_path=out/'draft_meta_info.json';meta=json.loads(meta_path.read_text())
        meta.update(draft_name=out.name,draft_fold_path=str(out),draft_root_path=str(out.parent),draft_id=json.loads((out/'draft_content.json').read_text())['id'])
        meta_path.write_text(json.dumps(meta,ensure_ascii=False))
        shutil.copy2(pack/'audio-licenses.json',out/'audio-licenses.json')
        (out/'COMPATIBILITY.md').write_text('''# Experimental legacy Jianying draft

Generated with pyJianYingDraft 0.2.7. This is a plaintext legacy-format draft, not a verified latest-version project. No Jianying or CapCut GUI import has been verified by this adapter. It does not provide encryption, registration, or automatic installation.

The project contains consecutive baked motion clips, separate title/body text tracks, and independent music/effects tracks when supplied. Text uses a simple caption layout rather than reproducing the rendered typography. Original screenshots inside the motion clips and 3D/page-turn geometry are not separately editable.

Media paths are absolute for this destination. When moving to another OS or folder, regenerate the draft there from the portable editing pack. Do not overwrite existing application drafts. Test in a separate copy on a compatible build; if it rejects this format, use the portable pack and local subtitle import instead. Do not rename or overwrite encrypted draft files.
''')
    except Exception:
        if created and out.exists():shutil.rmtree(out)
        raise
    print(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args()
    try:export_draft(a.pack,a.out)
    except (ValueError,OSError,KeyError,ImportError) as exc:parser.exit(1,f'Error: {exc}\n')

if __name__=='__main__':main()
