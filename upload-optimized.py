#!/usr/bin/env python3
"""Prepare reusable CDN images; pass --push to publish them to the image host."""
import argparse
import hashlib
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
CDN = 'https://cdn.jsdelivr.net/gh/madneal/blog-image@main/'

def run(*args):
    subprocess.run(args, check=True)

def prepare(source, cover=False):
    source = pathlib.Path(source).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        output = pathlib.Path(tmp) / 'image.webp'
        if source.suffix.lower() == '.webp':
            output.write_bytes(source.read_bytes())
        elif source.suffix.lower() == '.gif':
            run('gif2webp', '-q', '75', '-m', '6', str(source), '-o', str(output))
        else:
            run('cwebp', '-quiet', '-q', '78', '-m', '6', str(source), '-o', str(output))
        digest = hashlib.sha256(output.read_bytes()).hexdigest()[:20]
        folder = ROOT / 'images' / 'optimized' / ('covers' if cover else 'content')
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / (digest + '.webp')
        target.write_bytes(output.read_bytes())
        if cover:
            for width in (320, 720):
                run('cwebp', '-quiet', '-q', '72', '-m', '6', '-resize', str(width), '0',
                    str(source), '-o', str(folder / f'{digest}-{width}.webp'))
        return CDN + target.relative_to(ROOT).as_posix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--cover', action='store_true', help='also create 320/720px variants')
    parser.add_argument('--push', action='store_true', help='commit optimized images and push main')
    args = parser.parse_args()
    if args.push:
        branch = subprocess.check_output(['git', '-C', str(ROOT), 'branch', '--show-current'], text=True).strip()
        if branch != 'main':
            parser.error('--push requires the image host main branch')
        if subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).strip():
            parser.error('--push requires a clean worktree before preparing images')
        run('git', '-C', str(ROOT), 'pull', '--ff-only', 'origin', 'main')
    urls = [prepare(f, args.cover) for f in args.files]
    if args.push:
        run('git', '-C', str(ROOT), 'add', 'images/optimized')
        changed = subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--quiet']).returncode
        if changed:
            run('git', '-C', str(ROOT), 'commit', '-m', 'Upload optimized images')
        run('git', '-C', str(ROOT), 'push', 'origin', 'main')
    for url in urls:
        print(url)
