# Roadmap

BEE2.5 is in early development. The roadmap is a direction, not a promise of completed features.

## Phase 1 — Foundation

- [x] Establish Python package structure
- [x] Add a first package manifest format and validator
- [x] Add VMF structural inspection
- [x] Add a Tkinter desktop application
- [x] Import package folders and ZIP packages
- [x] Create a package from a VMF file
- [x] Add initial test suite and GitHub Actions checks

## Phase 2 — Package infrastructure

- [ ] Define package object schemas for items, styles, skyboxes, and quote packs
- [ ] Discover and index objects provided by installed packages
- [ ] Validate asset paths and package dependencies
- [ ] Report conflicts between packages
- [ ] Add legacy BEE2.4 .bee_pack compatibility

## Phase 3 — Puzzle Maker integration

- [ ] Implement style selection in the export configuration
- [ ] Implement skybox and fog configuration
- [ ] Implement quote-pack selection with correct choreography/localization handling
- [ ] Implement item metadata and configuration handling
- [ ] Build a real Puzzle Maker compile/export pipeline

## Phase 4 — User experience

- [x] Add selectors for requested style and voice presets
- [x] Add user-defined style and skybox profile storage
- [ ] Add visual package and content previews
- [ ] Add custom voice package tooling
- [ ] Improve diagnostics and logs
- [ ] Document migration from BEE2.4

## Current export scope

The current Portal 2 exporter compiles standalone VMF maps using VBSP, VVIS, and VRAD. It does not yet generate Puzzle Maker maps or apply the selected BEE2.5 presets to a BSP.

## Non-goals

- Redistributing Portal 2 game assets
- Claiming compatibility before it has been tested
