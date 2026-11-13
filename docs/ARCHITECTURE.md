# Architecture

BEE2.5 is being developed as a modular Python application.

## Current modules

- `bee25.cli`: command-line entry point.
- `bee25.packages.manifest`: parsing and validation of package metadata.

## Planned boundaries

- Package discovery and indexing
- Asset validation and dependency analysis
- Portal 2 export/build pipeline
- User interface

Keep the core package logic independent from the UI so it can be tested without launching Portal 2 or the Puzzle Maker.
