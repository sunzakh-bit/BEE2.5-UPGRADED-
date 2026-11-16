"""Compile an imported VMF with Portal 2's Source compiler tools."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from bee25.packages.vmf import inspect_vmf

_MAP_NAME = re.compile(r"^[A-Za-z0-9_-]{1,48}$")
_PROGRESS = Callable[[str], None]


class ExportError(RuntimeError):
    """Raised when Portal 2 export cannot be completed."""


@dataclass(frozen=True, slots=True)
class ExportResult:
    bsp_path: Path
    game_directory: Path
    map_name: str


def locate_game_directory(install_path: Path) -> Path:
    root = install_path.expanduser().resolve()
    candidates = [root, root / "portal2"]
    for candidate in candidates:
        if (candidate / "gameinfo.txt").is_file():
            return candidate
    raise ExportError(
        "Portal 2 game directory was not found. Select either the Portal 2 install "
        "folder or its portal2 subfolder (the selected game folder must contain gameinfo.txt)."
    )


def _find_tool(game_dir: Path, tool_name: str) -> Path:
    names = [tool_name + ".exe", tool_name]
    roots = [game_dir / "bin", game_dir.parent / "bin"]
    for folder in roots:
        for name in names:
            candidate = folder / name
            if candidate.is_file():
                return candidate
    raise ExportError(
        f"Could not find {tool_name} in '{game_dir / 'bin'}' or '{game_dir.parent / 'bin'}'. "
        "Install/verify the Portal 2 tools or select the correct game folder."
    )


def _run_tool(command: list[str], cwd: Path, timeout: int, label: str) -> None:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ExportError(f"{label} timed out after {timeout} seconds") from exc
    except OSError as exc:
        raise ExportError(f"Could not start {label}: {exc}") from exc

    if result.returncode != 0:
        output = (result.stdout or "").strip()
        tail = "\n".join(output.splitlines()[-25:])
        raise ExportError(
            f"{label} failed with exit code {result.returncode}.\n{tail or 'No tool output.'}"
        )


def export_vmf_to_portal2(
    vmf_path: Path,
    install_path: Path,
    map_name: str | None = None,
    *,
    style_id: str = "clean",
    skybox_id: str = "game_default",
    voice_id: str = "glados",
    progress: _PROGRESS | None = None,
) -> ExportResult:
    """Compile a VMF and copy its BSP into Portal 2's portal2/maps directory.

    The selected BEE2.5 style/skybox/voice IDs are written to a sidecar metadata
    file for future Puzzle Maker integration. They are not yet applied to the BSP.
    """

    report = progress or (lambda _message: None)
    vmf_info = inspect_vmf(vmf_path)
    game_dir = locate_game_directory(install_path)
    tools = {name: _find_tool(game_dir, name) for name in ("vbsp", "vvis", "vrad")}

    selected_name = map_name or vmf_info.path.stem
    if not _MAP_NAME.fullmatch(selected_name):
        raise ExportError("Map name must contain 1-48 letters, digits, '_' or '-'.")

    with tempfile.TemporaryDirectory(prefix="bee25-compile-") as temp:
        work_dir = Path(temp)
        work_vmf = work_dir / f"{selected_name}.vmf"
        shutil.copy2(vmf_info.path, work_vmf)
        bsp_path = work_dir / f"{selected_name}.bsp"

        report("1/3 — Running VBSP…")
        _run_tool(
            [str(tools["vbsp"]), "-game", str(game_dir), str(work_vmf)],
            work_dir,
            300,
            "VBSP",
        )
        if not bsp_path.is_file():
            raise ExportError("VBSP finished without producing a BSP file.")

        report("2/3 — Running VVIS…")
        _run_tool([str(tools["vvis"]), str(bsp_path)], work_dir, 600, "VVIS")
        report("3/3 — Running VRAD…")
        _run_tool([str(tools["vrad"]), str(bsp_path)], work_dir, 900, "VRAD")

        if not bsp_path.is_file():
            raise ExportError("The compiled BSP disappeared during compilation.")

        maps_dir = game_dir / "maps"
        maps_dir.mkdir(parents=True, exist_ok=True)
        destination = maps_dir / f"{selected_name}.bsp"
        shutil.copy2(bsp_path, destination)

    metadata = {
        "format": "bee25-export-metadata-v1",
        "map": selected_name,
        "source_vmf": vmf_info.path.name,
        "selected_presets": {
            "style": style_id,
            "skybox": skybox_id,
            "voice": voice_id,
        },
        "note": (
            "Preset IDs are recorded for BEE2.5. They are not yet applied to the compiled BSP."
        ),
    }
    (game_dir / "maps" / f"{selected_name}.bee25.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    report(f"Export complete: {destination}")
    return ExportResult(destination, game_dir, selected_name)
