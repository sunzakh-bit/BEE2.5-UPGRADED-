"""Built-in names for BEE2.5 style and voice selectors.

These identifiers are selectable metadata presets. They do not bundle or redistribute
Portal 2 assets; applying them to Puzzle Maker requires the future compiler pipeline.
"""

BUILTIN_STYLES: tuple[dict[str, str], ...] = (
    {"id": "clean", "name": "Clean"},
    {"id": "original_clean", "name": "Original Clean"},
    {"id": "bts", "name": "BTS"},
    {"id": "wheatley_style", "name": "Wheatley Style"},
    {"id": "overgrown", "name": "Overgrown Style"},
    {"id": "underground", "name": "Underground Style"},
    {"id": "destroyed", "name": "Destroyed Style"},
    {"id": "vactube", "name": "Vactube Style"},
)

BUILTIN_VOICES: tuple[dict[str, str], ...] = (
    {"id": "glados", "name": "GLaDOS"},
    {"id": "announcer_apocalypse", "name": "Announcer (Apocalypse)"},
    {"id": "wheatley_core", "name": "Wheatley (Core)"},
    {"id": "wheatley_glados_wheatley", "name": "Wheatley (GLaDOS Wheatley)"},
    {"id": "announcer_bts", "name": "Announcer (BTS)"},
)

DEFAULT_SKYBOX = {"id": "sky_black", "name": "Black (Portal 2 default)"}
