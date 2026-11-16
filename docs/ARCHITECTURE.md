# Architecture

BEE2.5 is a modular Python application. Core package logic is kept separate from the desktop UI.

## Current modules

- `bee25.cli`: command-line entry point for GUI, validation, VMF inspection, importing, and compiling.
- `bee25.ui.app`: Tkinter desktop interface.
- `bee25.packages.manifest`: parsing and validation of package metadata.
- `bee25.packages.manager`: package installation, ZIP extraction, and VMF package creation.
- `bee25.packages.vmf`: basic VMF text validation and inspection.
- `bee25.content.catalog`: built-in style and voice selector entries.
- `bee25.profiles`: persistence for user-defined style and skybox profiles.
- `bee25.export.portal2`: standalone VMF compilation using Source compiler tools.

## User data

BEE2.5 stores packages and custom profiles outside the source checkout:
- Windows: `%APPDATA%/BEE2.5/`
- Linux: `$XDG_CONFIG_HOME/bee25/` or `~/.config/bee25/`
- macOS: `$XDG_CONFIG_HOME/bee25/` or `~/.config/bee25/`

## Export pipeline

The current exporter runs VBSP, VVIS, and VRAD without a shell, using the selected Portal 2 game directory. It then copies the compiled BSP to `portal2/maps/`. Style, skybox, and voice selections are recorded as sidecar metadata only.

## Planned boundaries

- Package object parser and package dependency graph
- Asset and material validation
- Puzzle Maker configuration and item database
- Style/skybox/fog/quote pack export adapters
- Full Puzzle Maker map generation and game export

Do not make the UI responsible for parsing VMF files or copying game assets directly. Put those operations in testable service modules.
