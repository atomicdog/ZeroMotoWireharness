#!/usr/bin/env python3

import argparse
import shutil
import subprocess
from pathlib import Path

from wireviz import wireviz

HARNESS_DIR = Path('harness')
DOCS_DIR = Path('docs')
GENERATED_DIR = DOCS_DIR / 'harness'  # wireviz output + generated pages (gitignored)
SITE_DIR = Path('site')
GENERATED_EXTENSIONS = ['.gv', '.bom.tsv', '.png', '.svg', '.html']


def build(harness_dir: Path = HARNESS_DIR, out_dir: Path = GENERATED_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    yml_files = sorted(harness_dir.glob('*.yml'), key=lambda f: f.stem.lower())

    for yml_file in yml_files:
        print(f'  Building {yml_file}')
        wireviz.parse_file(str(yml_file))
        for ext in GENERATED_EXTENSIONS:
            src = yml_file.with_suffix(ext)
            if src.exists():
                shutil.move(str(src), out_dir / src.name)
        generate_page(yml_file.stem, out_dir)

    generate_index(yml_files, out_dir)

    print('  Running zensical build')
    subprocess.run(['zensical', 'build', '--clean'], check=True)
    print('Done.')


def bom_to_markdown(tsv_file: Path) -> str:
    rows = [line.split('\t') for line in tsv_file.read_text().splitlines() if line.strip()]
    if not rows:
        return '_No BOM entries._'

    def fmt(cells):
        return '| ' + ' | '.join(c.replace('|', '\\|') for c in cells) + ' |'

    header, *body = rows
    lines = [fmt(header), '| ' + ' | '.join('---' for _ in header) + ' |']
    lines += [fmt(r + [''] * (len(header) - len(r))) for r in body]
    return '\n'.join(lines)


def generate_page(name: str, out_dir: Path):
    bom_file = out_dir / f'{name}.bom.tsv'
    bom = bom_to_markdown(bom_file) if bom_file.exists() else '_No BOM generated._'

    md = f"""\
# {name}

[Interactive HTML]({name}.html) &middot; [SVG]({name}.svg) &middot; [PNG]({name}.png) &middot; [BOM (TSV)]({name}.bom.tsv) &middot; [Source](https://github.com/atomicdog/ZeroMotoWireharness/blob/master/harness/{name}.yml)

[![{name} wiring diagram]({name}.svg)]({name}.svg)

## Bill of materials

{bom}
"""
    (out_dir / f'{name}.md').write_text(md)


def generate_index(yml_files, out_dir: Path):
    rows = '\n'.join(f'- [{f.stem}]({f.stem}.md)' for f in yml_files)
    md = f"""\
# Harnesses

{rows}
"""
    (out_dir / 'index.md').write_text(md)
    print(f'  Generated {out_dir}/index.md')


def clean(harness_dir: Path = HARNESS_DIR, out_dir: Path = GENERATED_DIR):
    # Remove any leftover generated files from harness dir
    for yml_file in harness_dir.glob('*.yml'):
        for ext in GENERATED_EXTENSIONS:
            f = yml_file.with_suffix(ext)
            if f.exists():
                print(f'  rm {f}')
                f.unlink()
    for d in (out_dir, SITE_DIR):
        if d.exists():
            print(f'  rm -r {d}')
            shutil.rmtree(d)
    print('Done.')


def main():
    parser = argparse.ArgumentParser(description='Build wire harness diagrams')
    parser.add_argument('action', nargs='?', choices=['build', 'clean'], default='build')
    args = parser.parse_args()

    if args.action == 'build':
        build()
    elif args.action == 'clean':
        clean()


if __name__ == '__main__':
    main()
