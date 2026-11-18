#!/usr/bin/env python3
"""Install a portable native draft at its final destination on macOS or Windows.

Standard library only. A local empty project supplies the target editor schema.
Never overwrites projects or updates the application's library index.
"""
import argparse
import copy
import json
import shutil
import uuid
from pathlib import Path


def media_relative(raw, source):
    parts = str(raw).replace('\\', '/').split('/')
    if 'media' not in parts:
        raise ValueError('Media is outside portable draft folder')
    tail = parts[len(parts)-parts[::-1].index('media'):]
    if not tail or any(p in ('', '.', '..') or ':' in p for p in tail):
        raise ValueError('Unsafe media path')
    rel = Path(*tail)
    root = (Path(source)/'media').resolve()
    path = root/rel
    try:
        path.resolve().relative_to(root)
    except ValueError:
        raise ValueError('Unsafe media symlink: '+str(rel))
    if not path.is_file():
        raise ValueError('Missing media: '+str(rel))
    return rel


def install(source, template, out, editor):
    source,out=(Path(p).resolve() for p in (source,out))
    template=Path(template).resolve() if template else None
    if out.exists(): raise FileExistsError('Destination already exists: '+str(out))
    src=json.loads((source/'draft_content.json').read_text(encoding='utf-8'))
    if template is None:
        if editor != 'jianying': raise ValueError('CapCut requires an empty local template')
        filename='draft_content.json';base=copy.deepcopy(src)
        base['tracks']=[];base['duration']=0;base['materials']={k:[] for k in src['materials']}
        meta=json.loads((source/'draft_meta_info.json').read_text(encoding='utf-8'));modern=False;project=None
    else:
        filename='draft_info.json' if (template/'draft_info.json').exists() else 'draft_content.json'
        try:base=json.loads((template/filename).read_text(encoding='utf-8'))
        except (UnicodeDecodeError,json.JSONDecodeError) as exc:
            raise ValueError('Template is not readable JSON. Do not overwrite or rename encrypted drafts. Jianying can be tested with a separate legacy draft by omitting --template; compatibility remains unverified until opened.') from exc
        meta=json.loads((template/'draft_meta_info.json').read_text(encoding='utf-8'))
        modern=(template/'Timelines/project.json').is_file()
        project=json.loads((template/'Timelines/project.json').read_text(encoding='utf-8')) if modern else None
    if base.get('tracks') or base.get('duration') or any(base.get('materials',{}).values()):
        raise ValueError('Use a new empty local project as template; existing projects are never modified')
    if modern and len(project.get('timelines',[]))!=1:raise ValueError('Template requires one empty timeline')
    # Paths are reconstructed from bundled media names, never from the source
    # computer's drive letters or home directory. Reject ambiguous/traversing paths.
    media_map={}
    for kind in ('videos','audios'):
        for item in src['materials'].get(kind,[]):
            rel=media_relative(item['path'], source)
            media_map[item['path']]=str(out/'media'/rel)
    dst=copy.deepcopy(base)
    for key in ('tracks','duration','fps','canvas_config','keyframes'):
        if key in src:dst[key]=copy.deepcopy(src[key])
    dst['materials'].update(copy.deepcopy(src['materials']))
    tid=str(uuid.uuid4()).upper();dst['id']=tid
    for kind in ('videos','audios'):
        for item in dst['materials'].get(kind,[]):item['path']=media_map[item['path']]
    # The template is empty, but omit its account/cloud metadata nevertheless.
    meta={k:v for k,v in meta.items() if 'cloud' not in k and 'enterprise' not in k and 'purchase' not in k}
    meta.update(draft_id=str(uuid.uuid4()).upper() if modern else tid,draft_name=out.name,draft_fold_path=str(out),draft_root_path=str(out.parent),tm_duration=src['duration'])
    cover = source/'draft_cover.jpg'
    meta['draft_cover'] = str(out/'draft_cover.jpg') if cover.is_file() else ''
    out.mkdir(parents=True)
    try:
        shutil.copytree(source/'media',out/'media')
        if cover.is_file(): shutil.copy2(cover,out/'draft_cover.jpg')
        (out/filename).write_text(json.dumps(dst,ensure_ascii=False),encoding='utf-8')
        (out/'draft_meta_info.json').write_text(json.dumps(meta,ensure_ascii=False),encoding='utf-8')
        if modern:
            project['id']=str(uuid.uuid4()).upper();project['main_timeline_id']=tid;project['timelines'][0]['id']=tid
            (out/'Timelines'/tid).mkdir(parents=True)
            (out/'Timelines/project.json').write_text(json.dumps(project),encoding='utf-8')
            (out/'Timelines'/tid/filename).write_text(json.dumps(dst,ensure_ascii=False),encoding='utf-8')
        if (source/'EDITING.md').exists():shutil.copy2(source/'EDITING.md',out/'EDITING.md')
    except Exception:
        shutil.rmtree(out);raise
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('source','out'):p.add_argument('--'+flag,type=Path,required=True)
    p.add_argument('--template',type=Path)
    p.add_argument('--editor',choices=['jianying','capcut'],required=True)
    a=p.parse_args();print(install(a.source,a.template,a.out,a.editor))
    print('安装完成。若剪映已打开，请保存当前工作后退出并重新启动；外部安装不会自动刷新草稿列表。')
