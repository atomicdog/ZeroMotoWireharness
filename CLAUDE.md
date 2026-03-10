# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WireViz project documenting the wire harness of a Zero SR/S electric motorcycle (Gen3 FST platform). Each `.yml` file in `harness/` describes a sub-harness or circuit. WireViz generates wiring diagrams (SVG, PNG, HTML) and bills of materials (BOM TSV) from them. The generated site is deployed to GitHub Pages via the `gh-pages` branch.

## Setup and Build

Builds run directly on the host using `uv`. `graphviz` must be installed on the host (`dot` in PATH).

```bash
make setup        # uv sync
make build        # build all harness diagrams → docs/
make clean        # remove generated output

# Build a single file
uv run wireviz harness/<name>.yml
```

`build.py` processes all `harness/*.yml` files, moves generated files to `docs/`, and produces `docs/index.html`. In VS Code, Ctrl+Shift+B offers "build current file" or "build all" tasks (both run via toolbox).

## Repository Structure

```
harness/          # WireViz YAML source files (one per sub-harness)
docs/             # Generated output — gitignored, deployed to gh-pages branch
.github/
  workflows/
    build.yml     # CI: builds diagrams and deploys to gh-pages on push to master
build.py          # Build script: harness/ → docs/, generates index.html
pyproject.toml    # UV dependencies (wireviz==0.3.2)
Makefile          # setup / build / clean targets
```

## YAML Schema

Each harness file has three sections:

- **`connectors`** — Named connectors with `pinlabels`, `pincount`, `type`, `subtype`, manufacturer/mpn, optional `hide_disconnected_pins`
- **`cables`** — Wire bundles with `wirecount` and `colors` arrays (two-letter codes: `BK`=black, `WH`=white, `RD`=red, `BU`=blue, `BN`=brown, `GY`=grey, `YE`=yellow, `GN`=green, `OG`=orange)
- **`connections`** — Maps `[connector: pins, wire: wires, connector: pins]`

## Key Conventions

- `MBB1` (48-pin) and `MBB2` (36-pin) are the Main Battery Box connectors and appear across multiple files — pin numbers must stay consistent with `harness/MBB.yml` as the reference
- `#~~~` marks intentional breaks/separators in connection blocks
- `fixme` notes flag pins or connectors with uncertain assignments
- Color codes follow standard automotive two-letter abbreviations
