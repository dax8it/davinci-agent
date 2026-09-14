#!/usr/bin/env python3
"""Install the four reviewed workspace skills together; refuse differing existing installs."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('clean-davinci-dialogue', 'first-cut-davinci-dialogue',
         'smooth-davinci-audio-cuts', 'edit-davinci-video')


def manifest(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path,
                        default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills')
    args = parser.parse_args()
    for name in NAMES:
        source, target = ROOT / 'skills' / name, args.dest / name
        if not (source / 'SKILL.md').is_file():
            parser.error(f'Missing source skill: {source}')
        if target.exists() and (not target.is_dir() or manifest(source) != manifest(target)):
            parser.error(f'Existing skill differs; review and back it up before replacement: {target}')
    args.dest.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        source, target = ROOT / 'skills' / name, args.dest / name
        if not target.exists():
            shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        if manifest(source) != manifest(target):
            raise RuntimeError(f'Installed file verification failed: {target}')
        print(f'Installed and verified: {target}')


if __name__ == '__main__':
    main()
