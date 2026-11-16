import json
from pathlib import Path
from zipfile import ZipFile

import pytest

from bee25.packages.manager import PackageManager


def test_install_zip_package(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "bee25.json").write_text(
        json.dumps({
            "id": "archive.demo",
            "name": "Archive Demo",
            "version": "1.0.0",
            "content": ["items"],
        }),
        encoding="utf-8",
    )
    (source / "readme.txt").write_text("hello", encoding="utf-8")
    archive = tmp_path / "demo.zip"
    with ZipFile(archive, "w") as zip_file:
        zip_file.write(source / "bee25.json", "demo/bee25.json")
        zip_file.write(source / "readme.txt", "demo/readme.txt")

    installed = PackageManager(tmp_path / "packages").install_package_archive(archive)
    assert installed.manifest.package_id == "archive.demo"
    assert (installed.path / "readme.txt").read_text(encoding="utf-8") == "hello"


def test_reject_zip_path_traversal(tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.zip"
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr("../outside.txt", "should not be extracted")

    with pytest.raises(ValueError, match="unsafe archive path"):
        PackageManager(tmp_path / "packages").install_package_archive(archive)
    assert not (tmp_path / "outside.txt").exists()
