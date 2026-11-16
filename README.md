# BEE2.5 — upgraded BEE2.4-inspired project

BEE2.5 is an independent community project aiming to modernize the workflow around Portal 2's Puzzle Maker, building on ideas and lessons from [BEE2.4](https://github.com/BEEmod/BEE2.4).

> **Development status: experimental.** The desktop shell, package handling, VMF inspection/import, preset metadata, and a basic VMF-to-BSP compiler wrapper exist. This is not yet a complete BEE2.4 replacement and does not yet inject BEE2 items or apply styles/voices inside Puzzle Maker.

## Current features

- Desktop UI launched with `bee25 gui`.
- Install a BEE2.5 package from a folder or ZIP archive.
- Create a local map package from a VMF file.
- Basic VMF structure inspection (not a full Hammer validation).
- Select built-in style labels: Clean, Original Clean, BTS, Wheatley Style, Overgrown, Underground, Destroyed, and Vactube.
- Add custom style presets based on one of the built-in styles.
- Add custom skybox presets by specifying a material path.
- Select voice preset labels: GLaDOS, Announcer (Apocalypse), Wheatley (Core), Wheatley (GLaDOS Wheatley), and Announcer (BTS).
- Compile a VMF using Portal 2 VBSP/VVIS/VRAD tools and copy the resulting BSP into `portal2/maps`, when those tools are installed and configured.

## Important limitations

- Style, skybox, and voice selections are currently saved as BEE2.5 metadata. They are **not yet applied** to the compiled BSP or Puzzle Maker.
- A custom style currently inherits a built-in style ID; a full style resource editor is still planned.
- A custom skybox entry stores a material path. It does not create the VMT/VTF assets.
- Voice choices are selectable labels only. Custom sound import and in-game voice replacement are not implemented.
- VMF validation is deliberately basic; use Hammer/Source tools to validate map geometry and entities.
- Legacy BEE2.4 `.bee_pack` files are not yet supported. BEE2.5 currently uses its own `bee25.json` package format.

## Requirements

- Python 3.11 or newer.
- Tkinter for the desktop interface (usually included with standard Windows Python).
- Portal 2 and its VBSP/VVIS/VRAD tools for map compilation.

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

## Launch the UI

```bash
bee25 gui
```

## Useful commands

```bash
bee25 validate-package examples/sample_package
bee25 install-package path/to/package-folder
bee25 install-package path/to/package.zip
bee25 inspect-vmf path/to/map.vmf
bee25 import-vmf path/to/map.vmf --id my.map --name "My Map"
bee25 export-vmf path/to/map.vmf "C:/Program Files (x86)/Steam/steamapps/common/Portal 2"
```

## Documentation

- [Roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Package format](docs/PACKAGE_FORMAT.md)
- [Contributing](CONTRIBUTING.md)

Portal 2 is a product of Valve. BEE2.5 is an independent community project and is not affiliated with or endorsed by Valve. Do not redistribute proprietary game assets or content without permission.
