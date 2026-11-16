"""User-defined style and skybox presets."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bee25.content.catalog import BUILTIN_STYLES
from bee25.packages.manager import user_data_dir

_PROFILE_ID = re.compile(r"^[a-z0-9][a-z0-9_.-]{1,63}$")
_ALLOWED_KINDS = {"styles", "skyboxes"}


class ProfileStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or user_data_dir() / "profiles").expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def list_profiles(self, kind: str) -> list[dict[str, str]]:
        self._check_kind(kind)
        path = self.root / f"{kind}.json"
        if not path.is_file():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return [
            {str(key): str(value) for key, value in item.items()}
            for item in data
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]

    def add_style(
        self, profile_id: str, name: str, base_id: str, description: str = ""
    ) -> dict[str, str]:
        if base_id not in {item["id"] for item in BUILTIN_STYLES}:
            raise ValueError("custom styles must declare a supported built-in base style")
        return self._add(
            "styles",
            {"id": profile_id, "name": name, "base": base_id, "description": description},
        )

    def add_skybox(self, profile_id: str, name: str, material: str) -> dict[str, str]:
        material = material.strip().replace("\\", "/")
        if not material or material.startswith("/") or ".." in Path(material).parts:
            raise ValueError("skybox material must be a relative game material path")
        if not material.lower().startswith("materials/"):
            material = "materials/" + material
        if not material.lower().endswith(".vmt"):
            material += ".vmt"
        return self._add(
            "skyboxes",
            {"id": profile_id, "name": name, "material": material},
        )

    def _add(self, kind: str, profile: dict[str, str]) -> dict[str, str]:
        self._check_kind(kind)
        profile_id = profile["id"].strip()
        name = profile["name"].strip()
        if not _PROFILE_ID.fullmatch(profile_id):
            raise ValueError("ID must be 2-64 lowercase letters, digits, '.', '_' or '-'")
        if not name:
            raise ValueError("name cannot be empty")
        existing = self.list_profiles(kind)
        if profile_id in {item["id"] for item in existing}:
            raise FileExistsError(f"{kind[:-1]} '{profile_id}' already exists")
        existing.append({**profile, "id": profile_id, "name": name})
        path = self.root / f"{kind}.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
        return profile

    @staticmethod
    def _check_kind(kind: str) -> None:
        if kind not in _ALLOWED_KINDS:
            raise ValueError(f"unsupported profile kind: {kind}")
