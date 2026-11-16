# BEE2.5 — upgraded BEE2.4-inspired project

BEE2.5 is an independent community project aiming to modernize the workflow around Portal 2's Puzzle Maker, building on ideas and lessons from [BEE2.4](https://github.com/BEEmod/BEE2.4).

> **Development status: early development.** BEE2.5 is not yet a complete or compatible replacement for BEE2.4. The current build has a desktop UI, package tooling, a basic VMF importer, preset selectors, and a VMF-to-BSP export path.

## Current features

- Tkinter desktop application with Packages, Presets, and Export tabs.
- Install BEE2.5 package folders and ZIP archives containing `bee25.json`.
- Create a personal package from a VMF file.
- Basic VMF text validation and map summary.
- Selectable style presets: Clean, Original Clean, BTS, Wheatley Style, Overgrown Style, Underground Style, Destroyed Style, and Vactube Style.
- User-defined style entries based on a built-in style.
- Game-default and user-defined skybox material profiles.
- Voice preset selectors: GLaDOS, Announcer (Apocalypse), Wheatley (Core), Wheatley (GLaDOS Wheatley), and Announcer (BTS).
- Compile a VMF using Portal 2's VBSP, VVIS, and VRAD tools and copy the BSP into `portal2/maps`.

## Not implemented yet

- Applying BEE2.5 styles, skyboxes, or voice packs to Puzzle Maker exports.
- Full BEE2.4 `.bee_pack` compatibility.
- Loading legacy BEE2.4 package definitions and assets.
- Custom voice asset/choreography integration.
- Full Puzzle Maker item, instance, and resource compiler.

The selected preset IDs are currently recorded in a sidecar `.bee25.json` file beside the exported BSP. They do not yet change the compiled map.

## Requirements

- Python 3.11 or newer.
- Tkinter (included with most standard Python installations; some Linux distributions package it separately).
- Portal 2 installation with the Source compile tools `vbsp`, `vvis`, and `vrad` for map export.

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

## Launch the desktop application

```bash
bee25 gui
```

Or:

```bash
python -m bee25.ui.app
```

## Command line

```bash
bee25 validate-package path/to/package
bee25 inspect-vmf path/to/map.vmf
bee25 import-vmf path/to/map.vmf --id author.map --name "My Map"
bee25 export-vmf path/to/map.vmf "C:/Games/Portal 2"
```

## Package layout

A package directory or ZIP archive has a `bee25.json` manifest at its root:

```text
my_package/
  bee25.json
  maps/
    my_map.vmf
  materials/
    ...
  models/
    ...
  sounds/
    ...
```

See [Package format](docs/PACKAGE_FORMAT.md), [Architecture](docs/ARCHITECTURE.md), [Export notes](docs/EXPORT.md), and [Roadmap](docs/ROADMAP.md).

## Legal note

Portal 2 is a product of Valve. This project is not affiliated with or endorsed by Valve. Do not include proprietary game assets or content you do not have permission to redistribute.
