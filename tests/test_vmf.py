import pytest
from pathlib import Path

from bee25.packages.vmf import VMFError, inspect_vmf, validate_vmf_text


VALID_VMF = """world
{
    "id" "1"
}
entity
{
    "id" "2"
    "classname" "info_player_start"
}
"""


def test_validate_minimal_vmf() -> None:
    blocks, worlds, entities = validate_vmf_text(VALID_VMF)
    assert blocks == 2
    assert worlds == 1
    assert entities == 1


def test_ignores_braces_inside_strings_and_comments() -> None:
    text = """world
{
    "message" "{ this is not a block }"
    // } comment brace
}
"""
    assert validate_vmf_text(text) == (1, 1, 0)


@pytest.mark.parametrize(
    "text",
    [
        "world {",
        "world }",
        '"unfinished',
        '"entity" "not a world block"',
        "",
    ],
)
def test_rejects_invalid_vmf(text: str) -> None:
    with pytest.raises(VMFError):
        validate_vmf_text(text)


def test_inspect_vmf_file(tmp_path: Path) -> None:
    vmf_file = tmp_path / "room.vmf"
    vmf_file.write_text(VALID_VMF, encoding="utf-8")
    info = inspect_vmf(vmf_file)
    assert info.path.name == "room.vmf"
    assert info.world_count == 1
    assert info.entity_count == 1


def test_rejects_non_vmf_extension(tmp_path: Path) -> None:
    file = tmp_path / "room.txt"
    file.write_text(VALID_VMF, encoding="utf-8")
    with pytest.raises(VMFError):
        inspect_vmf(file)
