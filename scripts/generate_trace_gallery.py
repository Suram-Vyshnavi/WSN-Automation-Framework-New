#!/usr/bin/env python3
"""
Generate a simple HTML gallery from a Playwright trace zip by extracting image files.
Usage:
    python3 scripts/generate_trace_gallery.py <trace.zip> [--output <outdir>]

Creates an output folder (default: <trace-name>_gallery) under the same folder as the zip,
extracts screenshots (png/jpg/jpeg/gif) and writes `index.html` referencing them.
"""
import sys
import os
import zipfile
from pathlib import Path
import argparse

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.gif')


def main():
    p = argparse.ArgumentParser(description='Generate HTML gallery from Playwright trace zip')
    p.add_argument('trace', help='path to the trace zip file')
    p.add_argument('--output', '-o', help='output directory (optional)')
    args = p.parse_args()

    trace_path = Path(args.trace)
    if not trace_path.exists():
        print('Trace zip not found:', trace_path)
        sys.exit(2)

    default_out = trace_path.with_suffix('')
    default_out = default_out.parent / (trace_path.stem + '_gallery')
    out_dir = Path(args.output) if args.output else default_out
    out_dir.mkdir(parents=True, exist_ok=True)

    images = []
    with zipfile.ZipFile(trace_path, 'r') as z:
        namelist = z.namelist()
        # find image files in the zip
        for i, name in enumerate(namelist):
            low = name.lower()
            if low.endswith(IMG_EXTS):
                # choose a safe filename to write (avoid collisions)
                base = Path(name).name
                safe_name = f"{i:04d}_{base}"
                dest = out_dir / safe_name
                with z.open(name) as src, open(dest, 'wb') as dst:
                    dst.write(src.read())
                images.append({'file': safe_name, 'path_in_zip': name})

    if not images:
        print('No images found inside trace zip. Gallery not created.')
        sys.exit(0)

    # write index.html
    html_lines = [
        '<!doctype html>',
        '<html><head><meta charset="utf-8"><title>Trace Gallery</title>',
        '<style>body{font-family:Arial,Helvetica,sans-serif;margin:18px} .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px} .card{border:1px solid #ddd;padding:8px} img{max-width:100%;height:auto;display:block;margin:6px 0}</style>',
        '</head><body>',
        f'<h1>Trace Gallery — {trace_path.name}</h1>',
        f'<p>Total images: {len(images)}</p>',
        '<div class="grid">'
    ]

    for img in images:
        html_lines.append('<div class="card">')
        html_lines.append(f'<strong>{img["file"]}</strong>')
        html_lines.append(f'<div><a href="{img["file"]}" target="_blank"><img src="{img["file"]}" alt="{img["file"]}"></a></div>')
        html_lines.append(f'<div style="font-size:smaller;color:#666">{img["path_in_zip"]}</div>')
        html_lines.append('</div>')

    html_lines.append('</div>')
    html_lines.append('</body></html>')

    index_path = out_dir / 'index.html'
    index_path.write_text('\n'.join(html_lines), encoding='utf-8')

    print('Gallery created at:', index_path)
    print('Open it with your browser, e.g.:')
    print(f'  open "{index_path}"')


if __name__ == '__main__':
    main()
