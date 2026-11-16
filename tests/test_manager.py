from pathlib import Path
import json

import pytest

from bee25.packages.manager import PackageManager


VALID_VMF = """world
{
    "id" "1"
}
"""


def test_create_package_from_vmf(tmp_path: Path) -> None:
    vmf = tmp_path / "test_map.vmf"
    vmf.write_text(VALID_VMF, encoding="utf-8")
    manager = PackageManager(tmp_path / "packages")

    installed, info = manager.create_vmf_package(vmf, "test.map", "Test map")
    assert installed.manifest.package_id == "test.map"
    assert (installed.path / "maps" / "test_map.vmf").is_file()
    manifest = json.loads((installed.path / "bee25.json").read_text(encoding="utf-8"))
    assert manifest["kind"] == "vmf_map"
    assert info.world_count == 1
    assert len(manager.list_packages()) == 1


def test_reject_duplicate_package_id(tmp_path: Path) -> None:
    vmf = tmp_path / "test_map.vmf"
    vmf.write_text(VALID_VMF, encoding="utf-8")
    manager = PackageManager(tmp_path / "packages")
    manager.create_vmf_package(vmf, "test.map", "Test map")
    with pytest.raises(FileExistsError):
        manager.create_vmf_package(vmf, "test.map", "Another map")
