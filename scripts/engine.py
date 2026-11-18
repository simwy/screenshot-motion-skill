#!/usr/bin/env python3
"""Deterministic template engine; no LLM or desktop editor required. Python 3.9+, Node, FFmpeg."""
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
    subprocess.run([str(a) for a in args], cwd=cwd, check=True, stdout=sys.stderr)

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
    # Legacy audio settings are ignored: all new jobs are visual-only.
    d.pop('audio', None)
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
    return out

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
    return job / output

def finalize(job):
    """Compatibility finalizer: always deliver video without audio."""
    job = job.resolve()
    video = job / 'out/video-silent.mp4'
    if not video.is_file():
        video = job / 'out/book-silent.mp4'
    if not video.is_file():
        raise ValueError('Render out/video-silent.mp4 before finalizing')
    ff = shutil.which('ffmpeg')
    if not ff:
        raise ValueError('FFmpeg is required on PATH')
    output = job / 'out/video.mp4'
    run([ff, '-y', '-v', 'error', '-i', video, '-map', '0:v:0',
         '-c:v', 'copy', '-an', '-movflags', '+faststart', output])
    return output
