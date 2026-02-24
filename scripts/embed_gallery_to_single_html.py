#!/usr/bin/env python3
"""
Embed images from a gallery folder into a single self-contained HTML file.
Usage:
  python3 scripts/embed_gallery_to_single_html.py <gallery_dir> [--output <out.html>]

Example:
  python3 scripts/embed_gallery_to_single_html.py reports/traces/Valid_login_gallery \
      --output reports/traces/Valid_login_single.html
"""
import sys
import argparse
from pathlib import Path
import base64

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


def build_single_html(gallery_dir: Path, output: Path):
    imgs = [p for p in sorted(gallery_dir.iterdir()) if p.suffix.lower() in IMG_EXTS]
    if not imgs:
        print('No images found in', gallery_dir)
        return False

    parts = [
        '<!doctype html>',
        '<html><head><meta charset="utf-8">',
        f'<title>Trace Single-file Gallery — {gallery_dir.name}</title>',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<style>body{font-family:Arial,Helvetica,sans-serif;margin:18px} .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px} .card{border:1px solid #ddd;padding:8px} img{max-width:100%;height:auto;display:block;margin:6px 0}</style>',
        '</head><body>',
        f'<h1>Trace Single-file Gallery — {gallery_dir.name}</h1>',
        f'<p>Images: {len(imgs)}</p>',
        '<div class="grid">'
    ]

    for p in imgs:
        b = p.read_bytes()
        mime = 'image/jpeg'
        sfx = p.suffix.lower()
        if sfx == '.png':
            mime = 'image/png'
        elif sfx in ('.jpg', '.jpeg'):
            mime = 'image/jpeg'
        elif sfx == '.gif':
            mime = 'image/gif'
        elif sfx == '.webp':
            mime = 'image/webp'
        b64 = base64.b64encode(b).decode('ascii')
        data_uri = f"data:{mime};base64,{b64}"
        parts.append('<div class="card">')
        parts.append(f'<strong>{p.name}</strong>')
        parts.append(f'<div><a href="{data_uri}" target="_blank"><img src="{data_uri}" alt="{p.name}"/></a></div>')
        parts.append('</div>')

    parts.append('</div>')
    parts.append('</body></html>')

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('\n'.join(parts), encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gallery', help='path to gallery folder')
    parser.add_argument('--output', '-o', help='output html path', default=None)
    args = parser.parse_args()

    gallery = Path(args.gallery)
    if not gallery.exists() or not gallery.is_dir():
        print('Gallery directory not found:', gallery)
        sys.exit(2)

    out = Path(args.output) if args.output else gallery.parent / (gallery.name + '_single.html')
    ok = build_single_html(gallery, out)
    if not ok:
        print('No output generated')
        sys.exit(1)
    print('Single-file HTML created at:', out)


if __name__ == '__main__':
    main()
