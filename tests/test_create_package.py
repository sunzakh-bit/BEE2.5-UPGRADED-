import json
from pathlib import Path

from bee25.packages.manager import PackageManager


def test_create_package_scaffold(tmp_path: Path) -> None:
    manager = PackageManager(tmp_path / "packages")
    package = manager.create_package("author.tools", "Author Tools")
    assert package.manifest.package_id == "author.tools"
    assert (package.path / "items").is_dir()
    assert (package.path / "styles").is_dir()
    assert (package.path / "skyboxes").is_dir()
    assert (package.path / "resources").is_dir()
    manifest = json.loads((package.path / "bee25.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.0.0"
