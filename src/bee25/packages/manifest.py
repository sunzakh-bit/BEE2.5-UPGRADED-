"""Load and validate BEE2.5 package manifests."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_MANIFEST_NAME = "bee25.json"
_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{1,63}$")
_VERSION_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ManifestError(ValueError):
    """Raised when a package manifest is missing or invalid."""


@dataclass(frozen=True, slots=True)
class PackageManifest:
    package_id: str
    name: str
    version: str
    content: tuple[str, ...]


def parse_manifest(data: Any) -> PackageManifest:
    if not isinstance(data, dict):
        raise ManifestError("manifest root must be a JSON object")

    package_id = data.get("id")
    name = data.get("name")
    version = data.get("version")
    content = data.get("content", [])

    if not isinstance(package_id, str) or not _ID_PATTERN.fullmatch(package_id):
        raise ManifestError("id must be 2-64 lowercase letters, digits, '.', '_' or '-'")
    if not isinstance(name, str) or not name.strip():
        raise ManifestError("name must be a non-empty string")
    if not isinstance(version, str) or not _VERSION_PATTERN.fullmatch(version):
        raise ManifestError("version must use MAJOR.MINOR.PATCH format")
    if not isinstance(content, list) or not all(
        isinstance(item, str) and item.strip() for item in content
    ):
        raise ManifestError("content must be a list of non-empty strings")

    return PackageManifest(
        package_id=package_id,
        name=name.strip(),
        version=version,
        content=tuple(content),
    )


def load_manifest(package_dir: Path) -> PackageManifest:
    manifest_path = package_dir / _MANIFEST_NAME
    if not manifest_path.is_file():
        raise ManifestError(f"missing {_MANIFEST_NAME} in {package_dir}")

    with manifest_path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    return parse_manifest(data)
