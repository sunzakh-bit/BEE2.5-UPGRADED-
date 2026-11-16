# Roadmap

BEE2.5 is experimental. Checkboxes describe repository work, not compatibility guarantees.

## Phase 1 — Foundation
- [x] Python package structure and CLI
- [x] Draft BEE2.5 package manifest and validation
- [x] Automated tests and GitHub Actions checks

## Phase 2 — Packages and maps
- [x] Discover installed BEE2.5 packages
- [x] Install packages from folders
- [x] Install BEE2.5 ZIP package archives with path checks
- [x] Import a VMF into a local map package
- [x] Basic VMF structural inspection
- [ ] Full VMF/Hammer validation and asset dependency scanning
- [ ] Package conflict detection, dependency resolution, enable/disable and uninstall
- [ ] Legacy BEE2.4 .bee_pack compatibility importer

## Phase 3 — Desktop UI and presets
- [x] Tkinter desktop UI with Packages, Presets, and Export tabs
- [x] Built-in style selector: Clean, Original Clean, BTS, Wheatley, Overgrown, Underground, Destroyed, Vactube
- [x] User-defined style presets based on a built-in style
- [x] User-defined skybox entries
- [x] Voice preset selector
- [ ] Full custom style editor with item/instance/material overrides
- [ ] Skybox asset import, validation, and preview
- [ ] Custom voice package assets and safe audio replacement
- [ ] UI preview thumbnails and package metadata editor

## Phase 4 — Portal 2 integration
- [x] Basic VMF-to-BSP wrapper for VBSP, VVIS, and VRAD
- [ ] Verify compiler invocation across supported Portal 2 installations
- [ ] Apply selected style and skybox resources during export
- [ ] Integrate with Puzzle Maker item definitions and instances
- [ ] Add voice line/resource installation and restore support
- [ ] End-to-end tests using redistributable test maps/assets

## Non-goals
- Bundling proprietary Portal 2 assets in this repository
- Claiming BEE2.4 package compatibility before it is implemented and tested
