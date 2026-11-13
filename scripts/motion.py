#!/usr/bin/env python3
"""Prepare, render and mix videos from the template registry. Python 3.9+, Node, FFmpeg."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(args, cwd=None):
    subprocess.run([str(a) for a in args], cwd=cwd, check=True)

def string(value, name, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'{name} must be a nonempty string of at most {limit} characters')
    return value

def lines(value, name, limit):
    if not isinstance(value, list) or not 1 <= len(value) <= 3:
        raise ValueError(f'{name} needs 1–3 lines')
    return [string(x, name, limit) for x in value]

def number(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{name} must be between {low} and {high}')
    return value

def local_file(value, base):
    p = (base / string(value, 'file', 4096)).resolve()
    if not p.is_file():
        raise ValueError(f'File not found: {p}')
    return p

def registry():
    return json.loads((ROOT / "templates.json").read_text())

def prepare(config, out, template=None):
    config = config.resolve()
    d = json.loads(config.read_text(encoding='utf-8'))
    if not isinstance(d, dict):
        raise ValueError('Configuration must be a JSON object')
    selected = template or d.get('template', 'storybook')
    if selected not in registry():
        raise ValueError(f'Unknown template: {selected}. Run the templates command.')
    d['template'] = selected
    spec = registry()[selected]
    d['templateSpec'] = spec
    out = out.resolve()
    if out.exists():
        raise ValueError(f'Refusing to overwrite existing job: {out}')
    for key, limit in [('brand', 20), ('tagline', 44), ('cta', 28)]:
        string(d.get(key), key, limit)
    import re
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', d.get('accent', '')):
        raise ValueError('accent must be a six-digit hex color')
    for key in ['coverTitle', 'closingTitle']:
        lines(d.get(key), key, 20)
    d['holdFrames'] = round(number(d.pop('holdSeconds', 4), 'holdSeconds', 3, 12) * 30)
    if not isinstance(d.get('pages'), list) or not spec['minPages'] <= len(d['pages']) <= spec['maxPages']:
        raise ValueError(f'{selected} requires {spec["minPages"]}–{spec["maxPages"]} pages')
    files = []
    for i, p in enumerate(d['pages']):
        if not isinstance(p, dict):
            raise ValueError('Every page must be an object')
        if 'region' in p:
            v = p['region']
            if not isinstance(v, list) or len(v) != 4:
                raise ValueError('region must be [x, y, width, height]')
            for n in v: number(n, 'region coordinate', 0, 1)
            if v[2] <= 0 or v[3] <= 0 or v[0]+v[2] > 1 or v[1]+v[3] > 1:
                raise ValueError('region must fit within the source image')
        lines(p.get('title'), 'page title', 22)
        lines(p.get('body'), 'page body', 44)
        for key, limit in [('tag', 32), ('detail', 40), ('key', 36)]:
            string(p.get(key), key, limit)
        source = local_file(p.pop('image', None), config.parent)
        if source.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.webp']:
            raise ValueError('Screenshots must be PNG, JPEG or WebP')
        p['file'] = f'page-{i+1:02d}{source.suffix.lower()}'
        files.append((source, Path('public/screenshots') / p['file']))
    audio = d.pop('audio', {})
    manifest = {}
    if not isinstance(audio, dict):
        raise ValueError('audio must be an object')
    effect = 'pageTurn' if selected == 'storybook' else 'transition'
    if set(audio) - {'music', effect}:
        raise ValueError(f'{selected} accepts music and {effect} audio')
    for kind in ['music', effect]:
        if kind not in audio:
            continue
        a = audio[kind]
        if not isinstance(a, dict):
            raise ValueError('Each audio entry must be an object')
        source = local_file(a.get('file'), config.parent)
        string(a.get('license'), 'audio license', 200)
        string(a.get('source'), 'audio source / ownership record', 2048)
        a['gain'] = number(a.get('gain', .3 if kind == 'music' else 1), 'gain', 0, 10)
        a['startSeconds'] = number(a.get('startSeconds', 0), 'startSeconds', 0, 86400)
        a['file'] = f'{kind}{source.suffix.lower()}'
        a['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        files.append((source, Path('public/audio') / a['file']))
        manifest[kind] = a
    # Validate all inputs before creating anything. Input paths are not retained.
    shutil.copytree(ROOT / 'assets/video-template', out)
    entry = ("import React from 'react';\nimport {Composition,registerRoot} from 'remotion';\n"
             f"import {{{spec['component']}}} from './{spec['module']}';\n"
             f"registerRoot(()=> <Composition id=\"{spec['composition']}\" component={{{spec['component']}}} width={{1920}} height={{1080}} fps={{30}} durationInFrames={{{duration(d)[1]}}}/>);\n")
    (out / 'src/index.tsx').write_text(entry, encoding='utf-8')
    for source, relative in files:
        dest = out / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    (out / 'project.json').write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding='utf-8')
    (out / 'audio-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'Prepared {out} ({len(d["pages"])} pages). Install dependencies in this job, then render.')

def duration(d):
    spec = d.get('templateSpec') or registry()[d.get('template', 'storybook')]
    if spec['timing'] == 'fixed':
        return 0, spec['frames']
    close = 90 + len(d['pages']) * d['holdFrames'] + (len(d['pages']) - 1) * 42
    return close, close + 102

def browser_path(explicit):
    candidates = [explicit, os.environ.get('CHROME_PATH'), shutil.which('google-chrome'), shutil.which('chromium'), shutil.which('chromium-browser'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise ValueError('Chrome/Chromium not found. Supply --browser /path/to/executable.')

def job_fingerprint(job):
    h = hashlib.sha256()
    paths = [job / 'project.json', job / 'remotion.config.ts'] + sorted((job / 'src').glob('*')) + sorted((job / 'public/screenshots').glob('*'))
    for path in paths:
        if path.is_file():
            h.update(str(path.relative_to(job)).encode()); h.update(path.read_bytes())
    return h.hexdigest()

def render(job, browser, frame, clean=False):
    job = job.resolve()
    if clean and not (job / 'src/Content.ts').is_file():
        raise ValueError('This old job does not support clean rendering. Prepare a new job with the current skill.')
    cli = job / 'node_modules/@remotion/cli/remotion-cli.js'
    if not cli.is_file():
        raise ValueError(f'Install dependencies first: npm install (working directory: {job})')
    node = shutil.which('node')
    if not node:
        raise ValueError('Node.js is required')
    d = json.loads((job / 'project.json').read_text())
    _, total = duration(d)
    if frame is not None and not 0 <= frame < total:
        raise ValueError(f'frame must be in 0..{total-1}')
    (job / 'out').mkdir(exist_ok=True)
    mode = 'still' if frame is not None else 'render'
    output = f'out/{"clean-" if clean else ""}frame-{frame:04d}.png' if frame is not None else ('out/visuals-clean.mp4' if clean else 'out/video-silent.mp4')
    args = [node, cli, mode, 'src/index.tsx', (d.get('templateSpec') or registry()[d.get('template', 'storybook')])['composition'], output, '--browser-executable='+browser_path(browser)]
    args += [f'--frame={frame}'] if frame is not None else ['--concurrency=1']
    if clean:
        args += ['--props={"editorClean":true}']
    run(args, job)
    if clean and frame is None:
        (job / 'out/clean-render.json').write_text(json.dumps({'fingerprint': job_fingerprint(job)}))
    print(job / output)

def audio_cues(d):
    spec = d.get('templateSpec') or registry()[d.get('template', 'storybook')]
    if spec['timing'] == 'fixed':
        return spec['cues']
    close, _ = duration(d)
    return [67] + [90+d['holdFrames']+i*(42+d['holdFrames'])+21 for i in range(len(d['pages'])-1)] + [close+21]

def mix(job, stem=None):
    job = job.resolve()
    ff = shutil.which('ffmpeg')
    if not ff:
        raise ValueError('FFmpeg is required on PATH')
    d = json.loads((job / 'project.json').read_text())
    manifest = json.loads((job / 'audio-manifest.json').read_text())
    if stem:
        manifest = {k:v for k,v in manifest.items() if (k == 'music') == (stem == 'music')}
        if not manifest:
            return None
    video = job / 'out/video-silent.mp4'
    if not video.is_file() and (job / 'out/book-silent.mp4').is_file():
        video = job / 'out/book-silent.mp4'
    if not video.is_file():
        raise ValueError('Render out/video-silent.mp4 before mixing')
    if not manifest:
        shutil.copy2(video, job / 'out/video.mp4')
        print('No audio supplied; out/video.mp4 is silent.')
        return
    _, frames = duration(d)
    sec = frames / 30
    cues = audio_cues(d)
    args = [ff, '-y', '-v', 'error', '-i', video]
    filters, stems, index = [], [], 1
    for kind in ['music', 'pageTurn', 'transition']:
        if kind not in manifest:
            continue
        a = manifest[kind]
        args += ['-i', job / 'public/audio' / a['file']]
        if kind == 'music':
            filters.append(f'[{index}:a]atrim=start={a["startSeconds"]}:duration={sec},asetpts=PTS-STARTPTS,aresample=48000,volume={a["gain"]},afade=t=in:d=1,afade=t=out:st={sec-2}:d=2,apad=whole_dur={sec},atrim=end_sample={frames*1600},asetpts=N/SR/TB[music]')
            stems.append('[music]')
        else:
            # Use a bounded clip and measure its energy peak, not its file start.
            raw = subprocess.check_output([ff, '-v', 'error', '-ss', str(a['startSeconds']), '-i', str(job/'public/audio'/a['file']), '-t', '1.4', '-ar', '48000', '-ac', '1', '-f', 'f32le', '-'])
            import array
            values = array.array('f', raw)
            if len(values) < 480:
                raise ValueError('Effect audio is empty or too short at the requested offset')
            peak = max(range(len(values)//480), key=lambda k: sum(v*v for v in values[k*480:(k+1)*480])) * .01
            filters.append(f'[{index}:a]atrim=start={a["startSeconds"]}:duration=1.4,asetpts=PTS-STARTPTS,aresample=48000,volume={a["gain"]},afade=t=in:d=0.006,asplit={len(cues)}'+''.join(f'[p{i}]' for i in range(len(cues))))
            for i, f in enumerate(cues):
                filters.append(f'[p{i}]adelay={max(0,round((f/30-peak)*1000))}:all=1[s{i}]')
                stems.append(f'[s{i}]')
        index += 1
    filters.append(''.join(stems)+f'amix=inputs={len(stems)}:normalize=0,apad=whole_dur={sec},atrim=end_sample={frames*1600},asetpts=N/SR/TB,alimiter=limit=0.85:level=false:latency=true[a]')
    output = job / ('out/' + stem + '.wav' if stem else 'out/video.mp4')
    args += ['-filter_complex', ';'.join(filters)]
    args += ['-map', '[a]', '-c:a', 'pcm_s16le'] if stem else ['-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart']
    args += ['-ar', '48000', '-ac', '2', '-t', str(sec), output]
    run(args)
    print(output)
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('templates')
    p = sub.add_parser('prepare');p.add_argument('--template', choices=list(registry()));p.add_argument('--config', type=Path, required=True);p.add_argument('--out', type=Path, required=True)
    p = sub.add_parser('render');p.add_argument('--job', type=Path, required=True);p.add_argument('--browser');p.add_argument('--frame', type=int);p.add_argument('--clean', action='store_true')
    p = sub.add_parser('mix');p.add_argument('--job', type=Path, required=True)
    p = sub.add_parser('editor-pack');p.add_argument('--job', type=Path, required=True);p.add_argument('--out', type=Path, required=True)
    a = parser.parse_args()
    try:
        if a.command == 'templates':
            for name, spec in registry().items():
                print(f'{name}: {spec["description"]} ({spec["minPages"]}–{spec["maxPages"]} images)')
        elif a.command == 'prepare': prepare(a.config, a.out, a.template)
        elif a.command == 'render': render(a.job, a.browser, a.frame, a.clean)
        elif a.command == 'editor-pack':
            from editor_pack import export_pack
            export_pack(a.job, a.out)
        else: mix(a.job)
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
