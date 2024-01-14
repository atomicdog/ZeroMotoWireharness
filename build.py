#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path
from typing import List

from wireviz import wireviz
from wireviz.wv_helper import open_file_read, open_file_append

INPUT_EXTENSIONS = ['.yml']
EXTENSIONS_NOT_CONTAINING_GRAPHVIZ_OUTPUT = ['.gv', '.bom.tsv']
EXTENSIONS_CONTAINING_GRAPHVIZ_OUTPUT = ['.png', '.svg', '.html']
GENERATED_EXTENSIONS = EXTENSIONS_NOT_CONTAINING_GRAPHVIZ_OUTPUT + EXTENSIONS_CONTAINING_GRAPHVIZ_OUTPUT


def collect_filenames(description: str, path: Path, ext_list: list) -> List[Path]:
    patterns = [f"*{ext}" for ext in ext_list]
    print(f'{description} in "{path}"')
    return sorted([filename for pattern in patterns for filename in path.glob(pattern)])


def build_generated(path, output_filename=None, include_output=False, include_source=True):
    # preparation
    # collect and iterate input YAML files
    for yaml_file in collect_filenames('Building', path, INPUT_EXTENSIONS):
        print(f'  "{yaml_file}"')
        wireviz.parse_file(str(yaml_file))

        if output_filename:
            i = ''.join(filter(str.isdigit, yaml_file.stem))

            with open_file_append(path / output_filename) as out:
                if include_output:
                    with open_file_read(yaml_file.with_suffix('.md')) as info:
                        for line in info:
                            out.write(line.replace('## ', f'## {i} - '))
                        out.write('\n\n')
                else:
                    out.write(f'\n## {yaml_file.stem}\n')

                if include_source:
                    with open_file_read(yaml_file) as src:
                        out.write('```yaml\n')
                        for line in src:
                            out.write(line)
                        out.write('```\n')
                    out.write('\n')

                out.write(f'![]({yaml_file.stem}.png)\n\n')
                out.write(f'[Source]({yaml_file.name}) - [Bill of Materials]({yaml_file.stem}.bom.tsv)\n\n\n')


def clean_generated(path: Path):
    # collect and remove files
    for filename in collect_filenames('Cleaning', path, GENERATED_EXTENSIONS):
        if filename.is_file():
            print(f'  rm "{filename}"')
            os.remove(filename)


def compare_generated(path: Path, branch='', include_graphviz_output=False):
    if branch:
        branch = f' {branch.strip()}'
    compare_extensions = GENERATED_EXTENSIONS if include_graphviz_output else EXTENSIONS_NOT_CONTAINING_GRAPHVIZ_OUTPUT
    # collect and compare files
    for filename in collect_filenames('Comparing', path, compare_extensions):
        cmd = f'git --no-pager diff{branch} -- "{filename}"'
        print(f'  {cmd}')
        os.system(cmd)


def restore_generated(path: Path, branch='', output_filename=None):
    if branch:
        branch = f' {branch.strip()}'
    # collect input YAML files
    filename_list = collect_filenames('Restoring', path, INPUT_EXTENSIONS)
    # collect files to restore
    filename_list = [fn.with_suffix(ext) for fn in filename_list for ext in GENERATED_EXTENSIONS]
    if output_filename:
        filename_list.append(path / output_filename)
    # restore files
    for filename in filename_list:
        cmd = f'git checkout{branch} -- "{filename}"'
        print(f'  {cmd}')
        os.system(cmd)


def parse_args():
    parser = argparse.ArgumentParser(description=f'Build script', )
    parser.add_argument('action', nargs='?', action='store',
                        choices=['build', 'clean', 'compare', 'diff', 'restore'], default='build',
                        help='what to do with the generated files (default: build)')
    parser.add_argument('-b', '--branch', action='store', default='',
                        help='branch or commit to compare with or restore from')
    parser.add_argument('-c', '--compare-graphviz-output', action='store_true',
                        help='the Graphviz output is also compared (default: False)')
    parser.add_argument('--path', default=os.getcwd(),
                        help='the directory to process')
    parser.add_argument('-o', '--output', default='output.md',
                        help='the name of the output markdown file')
    return parser.parse_args()


def main():
    args = parse_args()
    path = Path(args.path)
    output_filename = args.output
    if args.action == 'build':
        build_generated(path, output_filename=output_filename)
    elif args.action == 'clean':
        clean_generated(path)
    elif args.action == 'compare' or args.action == 'diff':
        compare_generated(path, branch=args.branch, include_graphviz_output=args.compare_graphviz_output)
    elif args.action == 'restore':
        restore_generated(path, branch=args.branch, output_filename=output_filename)


if __name__ == '__main__':
    main()
