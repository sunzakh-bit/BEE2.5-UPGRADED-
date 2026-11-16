"""Install and create local BEE2.5 packages."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from bee25.packages.manifest import ManifestError, PackageManifest, load_manifest
from bee25.packages.vmf import VMFInfo, inspect_vmf

_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{1,63}$")


def user_data_dir() -> Path:
    if os.name == "nt":
        base = os.environ.get("APPDATA")
        return Path(base) / "BEE2.5" if base else Path.home() / "AppData/Roaming/BEE2.5"
    base = os.environ.get("XDG_CONFIG_HOME")
    return Path(base) / "bee25" if base else Path.home() / ".config/bee25"


@dataclass(frozen=True, slots=True)
class InstalledPackage:
    manifest: PackageManifest
    path: Path


class PackageManager:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or user_data_dir() / "packages").expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def list_packages(self) -> list[InstalledPackage]:
        packages: list[InstalledPackage] = []
        for child in sorted(self.root.iterdir()):
            if not child.is_dir() or child.is_symlink():
                continue
            try:
                packages.append(InstalledPackage(load_manifest(child), child))
            except (ManifestError, OSError, json.JSONDecodeError):
                continue
        return packages

    def install_package(self, source: Path) -> InstalledPackage:
        source = source.expanduser().resolve()
        if not source.is_dir():
            raise ValueError(f"package directory does not exist: {source}")
        if any(item.is_symlink() for item in source.rglob("*")):
            raise ValueError("package contains symbolic links; remove them before importing")

        manifest = load_manifest(source)
        destination = self.root / manifest.package_id
        if destination.exists():
            raise FileExistsError(f"package '{manifest.package_id}' is already installed")

        temporary = Path(tempfile.mkdtemp(prefix=".bee25-install-", dir=self.root))
        staged = temporary / manifest.package_id
        try:
            shutil.copytree(source, staged)
            shutil.move(str(staged), destination)
        finally:
            shutil.rmtree(temporary, ignore_errors=True)
        return InstalledPackage(manifest, destination)

    def create_vmf_package(
        self,
        vmf_path: Path,
        package_id: str,
        name: str,
        version: str = "1.0.0",
    ) -> tuple[InstalledPackage, VMFInfo]:
        if not _ID_PATTERN.fullmatch(package_id):
            raise ValueError("package ID must be 2-64 lowercase letters, digits, '.', '_' or '-'")
        if not name.strip():
            raise ValueError("package name cannot be empty")
        info = inspect_vmf(vmf_path)
        destination = self.root / package_id
        if destination.exists():
            raise FileExistsError(f"package '{package_id}' is already installed")

        temporary = Path(tempfile.mkdtemp(prefix=".bee25-vmf-", dir=self.root))
        staged = temporary / package_id
        try:
            (staged / "maps").mkdir(parents=True)
            shutil.copy2(info.path, staged / "maps" / info.path.name)
            manifest_data = {
                "id": package_id,
                "name": name.strip(),
                "version": version,
                "content": ["maps"],
                "kind": "vmf_map",
            }
            (staged / "bee25.json").write_text(
                json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8"
            )
            shutil.move(str(staged), destination)
        finally:
            shutil.rmtree(temporary, ignore_errors=True)

        installed = InstalledPackage(load_manifest(destination), destination)
        return installed, info
