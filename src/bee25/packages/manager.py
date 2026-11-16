"""Install and create local BEE2.5 packages."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from bee25.packages.manifest import ManifestError, PackageManifest, load_manifest, parse_manifest
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

    def create_package(
        self,
        package_id: str,
        name: str,
        version: str = "1.0.0",
    ) -> InstalledPackage:
        """Create a new editable package with standard content directories."""
        if not _ID_PATTERN.fullmatch(package_id):
            raise ValueError("package ID must be 2-64 lowercase letters, digits, '.', '_' or '-'")
        if not name.strip():
            raise ValueError("package name cannot be empty")
        manifest_data = {
            "id": package_id,
            "name": name.strip(),
            "version": version,
            "content": ["items", "styles", "skyboxes", "maps", "materials", "models", "sounds"],
        }
        parse_manifest(manifest_data)
        destination = self.root / package_id
        if destination.exists():
            raise FileExistsError(f"package '{package_id}' is already installed")

        temporary = Path(tempfile.mkdtemp(prefix=".bee25-new-", dir=self.root))
        staged = temporary / package_id
        try:
            staged.mkdir()
            for folder in (
                "items", "styles", "skyboxes", "maps",
                "materials", "models", "sounds", "resources",
            ):
                (staged / folder).mkdir()
            (staged / "bee25.json").write_text(
                json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8"
            )
            shutil.move(str(staged), destination)
        finally:
            shutil.rmtree(temporary, ignore_errors=True)
        return InstalledPackage(load_manifest(destination), destination)

    def install_package_archive(self, archive_path: Path) -> InstalledPackage:
        """Safely install a BEE2.5 package archive containing bee25.json.

        This currently supports ZIP archives using the BEE2.5 manifest format.
        Legacy BEE2.4 .bee_pack files need a separate compatibility importer.
        """
        archive_path = archive_path.expanduser().resolve()
        if not archive_path.is_file() or archive_path.suffix.lower() != ".zip":
            raise ValueError("select a .zip archive containing a BEE2.5 bee25.json manifest")

        temporary = Path(tempfile.mkdtemp(prefix=".bee25-archive-", dir=self.root))
        try:
            with zipfile.ZipFile(archive_path) as archive:
                total_size = 0
                for entry in archive.infolist():
                    raw_name = entry.filename
                    member = PurePosixPath(raw_name)
                    if (
                        not raw_name
                        or "\\" in raw_name
                        or member.is_absolute()
                        or ".." in member.parts
                        or (member.parts and ":" in member.parts[0])
                    ):
                        raise ValueError(f"unsafe archive path: {raw_name!r}")
                    mode = (entry.external_attr >> 16) & 0o170000
                    if mode == stat.S_IFLNK:
                        raise ValueError(f"symbolic links are not allowed: {raw_name}")
                    total_size += entry.file_size
                    if total_size > 512 * 1024 * 1024:
                        raise ValueError("package archive exceeds the 512 MiB unpacked size limit")
                archive.extractall(temporary)

            package_root = temporary
            if not (package_root / "bee25.json").is_file():
                folders = [item for item in temporary.iterdir() if item.is_dir()]
                if len(folders) == 1 and (folders[0] / "bee25.json").is_file():
                    package_root = folders[0]
            if not (package_root / "bee25.json").is_file():
                raise ValueError("archive does not contain bee25.json at its package root")
            return self.install_package(package_root)
        except zipfile.BadZipFile as exc:
            raise ValueError("the selected file is not a valid ZIP archive") from exc
        finally:
            shutil.rmtree(temporary, ignore_errors=True)

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
            # Validate generated metadata before moving it into the installed package store.
            parse_manifest(manifest_data)
            (staged / "bee25.json").write_text(
                json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8"
            )
            shutil.move(str(staged), destination)
        finally:
            shutil.rmtree(temporary, ignore_errors=True)

        installed = InstalledPackage(load_manifest(destination), destination)
        return installed, info
