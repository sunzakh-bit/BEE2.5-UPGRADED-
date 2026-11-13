import pytest

from bee25.packages.manifest import ManifestError, parse_manifest


def test_parse_valid_manifest() -> None:
    manifest = parse_manifest(
        {
            "id": "example.package",
            "name": "Example Package",
            "version": "1.2.3",
            "content": ["items", "instances"],
        }
    )
    assert manifest.package_id == "example.package"
    assert manifest.version == "1.2.3"
    assert manifest.content == ("items", "instances")


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"id": "Bad ID", "name": "Example", "version": "1.0.0"},
        {"id": "valid.id", "name": "", "version": "1.0.0"},
        {"id": "valid.id", "name": "Example", "version": "v1"},
        {"id": "valid.id", "name": "Example", "version": "1.0.0", "content": "items"},
    ],
)
def test_reject_invalid_manifest(payload: object) -> None:
    with pytest.raises(ManifestError):
        parse_manifest(payload)
