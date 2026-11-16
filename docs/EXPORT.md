# Portal 2 VMF export

The current exporter builds a **standalone VMF map**. It does not yet run the BEE2 Puzzle Maker compiler.

## Requirements

The selected Portal 2 game directory must contain `gameinfo.txt`. The exporter searches for the following programs in the game's `bin/` directory and the parent install directory's `bin/` directory:

- `vbsp.exe`
- `vvis.exe`
- `vrad.exe`

## What happens

1. BEE2.5 checks the VMF text structure.
2. VBSP compiles the VMF.
3. VVIS calculates visibility.
4. VRAD calculates lighting.
5. The resulting BSP is copied into `portal2/maps/<map_name>.bsp`.
6. Selected BEE2.5 style, skybox, and voice IDs are written to a `<map_name>.bee25.json` sidecar file.

The compiler processes run without a command shell and have timeouts. Compiler errors are displayed in the UI or terminal.

## Current limitations

The style, skybox, and voice selections are **metadata only**. They are not translated into BEE2.4-style VBSP configuration, game assets, Puzzle Maker item definitions, or quote-pack choreography. The BSP output is therefore only the compiled VMF map.

A future Puzzle Maker exporter will need to translate package objects into instances, editor item definitions, VBSP configuration, resources, and other game-specific data.
