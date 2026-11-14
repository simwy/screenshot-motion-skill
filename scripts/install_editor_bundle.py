#!/usr/bin/env python3
"""Install all bundled effects into a chosen local draft library. Python 3.9+."""
import argparse
from pathlib import Path
from install_editor_draft import install


def install_bundle(bundle, root, editor, template=None, prefix='Screenshot Motion'):
    bundle, root = Path(bundle).resolve(), Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Choose the existing draft library shown by your editor settings')
    if not prefix or any(c in prefix for c in '/\\:') or prefix in ('.','..'):
        raise ValueError('Prefix must be a simple project-name prefix')
    sources = sorted(p for p in (bundle/'drafts').iterdir() if (p/'draft_content.json').is_file())
    if not sources:
        raise ValueError('Bundle has no drafts')
    targets = [root/(prefix+' '+p.name) for p in sources]
    for target in targets:
        if target.exists():
            raise FileExistsError('No projects changed; choose another --prefix: '+str(target))
    created = []
    try:
        for source, target in zip(sources, targets):
            install(source, template, target, editor)
            created.append(target)
    except Exception:
        # Keep successfully installed drafts, so no project that an editor could
        # have opened concurrently is removed. Report partial completion clearly.
        print('Installed before failure:', ', '.join(str(p) for p in created) or 'none')
        raise
    return created


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--editor', choices=['jianying','capcut'], required=True)
    p.add_argument('--template', type=Path)
    p.add_argument('--prefix', default='Screenshot Motion')
    a = p.parse_args()
    for path in install_bundle(a.bundle,a.root,a.editor,a.template,a.prefix):
        print(path)
    print('Installation finished. Restart the editor and complete acceptance.csv; generation is not client verification.')
