"""Export portable editing media. No editor installation or draft mutation required."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from engine import duration, job_fingerprint


def scenes(d):
    total = duration(d)[1]
    name = d.get('template', 'storybook')
    if name == 'entrance':
        return [(0, 94, 'Opening', None), (94, 133, 'Fan', None), (133, total, 'Closing', None)]
    if name == 'spotlight':
        return [(0, 145, 'Opening', None), (145, 280, 'Feature', 2), (280, total, 'Closing', None)]
    if name == 'launch':
        return [(0, 90, 'Opening', None), (90, 195, 'Feature', 0), (195, 300, 'Feature', 1),
                (300, 405, 'Feature', 2), (405, 480, 'Feature', 3), (480, total, 'Closing', None)]
    if name == 'flipstack':
        return [(0, 60, 'Opening', None)] + [(60+i*90, 150+i*90, 'Feature', i) for i in range(5)] + [(510, total, 'Closing', None)]
    if name == 'kinetic':
        return [(0, 60, 'Opening', None), (60, 135, 'Feature', 0), (135, 210, 'Feature', 1),
                (210, 285, 'Feature', 2), (285, 360, 'Feature', 3), (360, total, 'Closing', None)]
    if name == 'prism':
        return [(0, 100, 'Opening', None), (100, 190, 'Feature', 1), (190, 280, 'Feature', 2),
                (280, 370, 'Feature', 3), (370, total, 'Closing', None)]
    if name == 'orbit':
        return [(0, 90, 'Opening', None), (90, 200, 'Feature', 1), (200, 310, 'Feature', 2),
                (310, 420, 'Feature', 3), (420, total, 'Closing', None)]
    if name != 'storybook':
        raise ValueError(f'No editing timeline mapping for {name}; add one before exporting')
    result = [(0, 90, 'Opening', None)]
    for i in range(len(d['pages'])):
        start = 90 + i*(d['holdFrames']+42)
        end = start+d['holdFrames']+(42 if i < len(d['pages'])-1 else 0)
        result.append((start, end, 'Feature', i))
    result.append((duration(d)[0], total, 'Closing', None))
    return result


def captions(d):
    if d.get('template') == 'entrance':
        return [
            {'startFrame':4, 'endFrame':94, 'title':'\n'.join(d['coverTitle']),
             'body':' '.join(d['pages'][0]['body']) + '\n' + '\n'.join(p['key'] + ': ' + p['detail'] for p in d['pages'])},
            {'startFrame':133, 'endFrame':duration(d)[1], 'title':'\n'.join(d['closingTitle']), 'body':d['cta']}
        ]
    result = []
    for start, end, kind, i in scenes(d):
        if kind == 'Opening': title, body = d['coverTitle'], d['tagline']
        elif kind == 'Closing': title, body = d['closingTitle'], d['cta']
        else: title, body = d['pages'][i]['title'], ' '.join(d['pages'][i]['body'])
        # Book captions stay off turning surfaces. They are independent editor text.
        if d.get('template') == 'storybook':
            if kind == 'Opening': end = 45
            elif kind == 'Closing': start += 42
            else: end = start+d['holdFrames']
        if d.get('template') == 'flipstack' and kind == 'Feature':
            start += 24 if i else 0
        result.append({'startFrame':start, 'endFrame':end, 'title':'\n'.join(title), 'body':body})
    return result


def timestamp(frame):
    ms = round(frame*1000/30)
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def export_pack(job, out):
    job, out = job.resolve(), out.resolve()
    if out.exists(): raise ValueError(f'Refusing to overwrite: {out}')
    ff = shutil.which('ffmpeg'); probe = shutil.which('ffprobe')
    if not ff or not probe: raise ValueError('FFmpeg and FFprobe are required')
    clean, proof = job/'out/visuals-clean.mp4', job/'out/clean-render.json'
    if not clean.is_file() or not proof.is_file():
        raise ValueError('Render with --clean first. A finished video with baked captions is not a clean plate.')
    if json.loads(proof.read_text())['fingerprint'] != job_fingerprint(job):
        raise ValueError('Clean render is stale; rerender with --clean after changing the project or screenshots')
    d = json.loads((job/'project.json').read_text()); total=duration(d)[1]
    info=json.loads(subprocess.check_output([probe,'-v','error','-select_streams','v:0','-show_streams','-of','json',str(clean)]))['streams'][0]
    if (int(info.get('nb_frames',0)),info['width'],info['height']) != (total,1920,1080):
        raise ValueError('Clean plate frame count or resolution does not match this job')
    cuts=scenes(d); caps=captions(d)
    out.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.editing-',dir=out.parent))
    try:
        (stage/'clips').mkdir()
        shutil.copy2(clean,stage/'visuals-clean.mp4')
        shutil.copytree(job/'public/screenshots',stage/'screenshots')
        # Preserve all copy in a portable text reference, with no machine-local paths.
        (stage/'copy.json').write_text(json.dumps({k:d[k] for k in ['brand','tagline','cta','coverTitle','closingTitle','pages']},indent=2,ensure_ascii=False))
        timeline=[]
        for n,(start,end,kind,index) in enumerate(cuts,1):
            filename=f'clips/{n:02d}-{kind.lower()}.mp4'
            subprocess.run([ff,'-y','-v','error','-i',str(clean),'-vf',f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS',
                '-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(stage/filename)],check=True)
            timeline.append({'file':filename,'startFrame':start,'endFrame':end,'label':kind,'pageIndex':index})
        for field in ['title','body']:
            chunks=[f'{i}\n{timestamp(c["startFrame"])} --> {timestamp(c["endFrame"])}\n{c[field]}\n' for i,c in enumerate(caps,1)]
            (stage/('titles.srt' if field == 'title' else 'descriptions.srt')).write_text('\n'.join(chunks),encoding='utf-8')
        manifest={'schemaVersion':1,'template':d['template'],'brand':d['brand'],'fps':30,'width':1920,'height':1080,
            'durationFrames':total,'clips':timeline,'captions':caps,'audio':{},
            'editability':{'motion':'baked into clips','screenshotPixels':'baked; originals provided for replacement overlays',
                'captions':'editable after SRT import; typography and placement are set in the editor',
                'audio':'silent; no audio tracks'},
            'nativeDraftStatus':'separate native exporter for original seven templates; client acceptance varies'}
        (stage/'timeline.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
        (stage/'START-HERE.md').write_text('''# Continue editing in Jianying or CapCut Desktop

1. Create a 1920x1080, 30 fps project. Import `visuals-clean.mp4`, or place the numbered `clips/` files consecutively from time zero. Use one approach, not both.
2. Import `titles.srt` through the editor's local subtitle import. Edit the resulting text clips, font, size and position. `descriptions.srt` is an optional second text pass; import on a separate track if supported, or copy its text from `copy.json`. Native menu names and SRT support depend on the editor version.
3. The original `screenshots/` are available to add or replace ordinary image overlays. To replace a screenshot inside a curved page or orbital card, ask the skill to rerender that shot.
4. Trim/reorder the clips if needed. Captions will not automatically follow manual edits; move their timeline segments with the corresponding shots.

`timeline.json` records exact frame boundaries. `copy.json` contains the original promotional copy. This folder is portable media, not a native one-click draft. Motion stays baked in the clips; imported captions do not reproduce the original animated typography or curved page lettering. Add your own text style and layout in the editor. Text inside screenshots is unchanged.

CapCut Desktop documents SRT import at https://www.capcut.com/help/how-to-import-subtitles. Jianying is a separate product: verify local subtitle import in your installed build. If unavailable, use `copy.json` to create text clips manually.

Native editable drafts are generated separately with motion_native.py for the original seven templates.
''',encoding='utf-8')
        stage.rename(out)
    except Exception:
        shutil.rmtree(stage,ignore_errors=True);raise
    print(out)
