from pathlib import Path

import pytest

from bee25.profiles import ProfileStore


def test_add_custom_style(tmp_path: Path) -> None:
    store = ProfileStore(tmp_path)
    item = store.add_style("my.clean", "My Clean", "clean", "A personal variation")
    assert item["id"] == "my.clean"
    assert store.list_profiles("styles")[0]["base"] == "clean"


def test_reject_duplicate_style(tmp_path: Path) -> None:
    store = ProfileStore(tmp_path)
    store.add_style("my.clean", "My Clean", "clean")
    with pytest.raises(FileExistsError):
        store.add_style("my.clean", "Duplicate", "clean")


def test_add_skybox_material_path(tmp_path: Path) -> None:
    store = ProfileStore(tmp_path)
    item = store.add_skybox("blue.sky", "Blue Sky", "skybox/blue")
    assert item["material"] == "materials/skybox/blue.vmt"


def test_reject_traversal_skybox_path(tmp_path: Path) -> None:
    store = ProfileStore(tmp_path)
    with pytest.raises(ValueError):
        store.add_skybox("unsafe.sky", "Unsafe", "../outside.vmt")
