# BEE2.5 — upgraded BEE2.4-inspired project

BEE2.5 is an independent community project aiming to modernize the workflow around Portal 2's Puzzle Maker, building on ideas and lessons from [BEE2.4](https://github.com/BEEmod/BEE2.4).

> **Development status: early development.** This repository is a new foundation, not yet a complete or compatible replacement for BEE2.4.

## Goals

- A maintainable, modular Python codebase.
- Clear package metadata and validation.
- Better diagnostics and package conflict reporting.
- A modern, approachable user experience.
- Compatibility research and migration support for existing BEE2.4 packages.

## Current state

The initial codebase includes:
- A Python package and `bee25` command-line entry point.
- A draft `bee25.json` package manifest.
- A package manifest validator.
- A sample package and initial tests.
- Architecture, package-format, and roadmap documentation.

## Requirements

- Python 3.11 or newer.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
```

## Validate the sample package

```bash
bee25 validate-package examples/sample_package
```

## Project documentation

- [Roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Draft package format](docs/PACKAGE_FORMAT.md)
- [Contributing](CONTRIBUTING.md)

## Important

Portal 2 is a product of Valve. This project is not affiliated with or endorsed by Valve. Do not add proprietary game assets or content you do not have permission to redistribute.
