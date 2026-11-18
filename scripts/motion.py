#!/usr/bin/env python3
"""CLI adapter for the deterministic screenshot motion engine."""
import argparse
from pathlib import Path
import subprocess
from engine import registry, prepare, render, finalize

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
        elif a.command == 'prepare': print(prepare(a.config, a.out, a.template))
        elif a.command == 'render': print(render(a.job, a.browser, a.frame, a.clean))
        elif a.command == 'editor-pack':
            from editor_pack import export_pack
            export_pack(a.job, a.out)
        else: print(finalize(a.job))
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
