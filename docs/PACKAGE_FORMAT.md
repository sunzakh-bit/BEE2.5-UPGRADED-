# BEE2.5 package format (draft)

A package is a directory or ZIP archive containing `bee25.json` at its root.

```json
{
  "id": "author.package-name",
  "name": "Package display name",
  "version": "1.0.0",
  "content": ["items", "instances", "resources"]
}
```

## Manifest fields
- `id`: stable identifier, 2–64 lowercase letters, digits, dots, underscores or hyphens.
- `name`: non-empty display name.
- `version`: `MAJOR.MINOR.PATCH`.
- `content`: optional list describing included content.

## Importing a VMF

The UI can create a package from one VMF file. The current generated package layout is:

```
my-map/
  bee25.json
  maps/
    my_map.vmf
```

This is a map-source package, not a converted Puzzle Maker item package. VMF inspection checks basic text structure only; it does not prove that a map compiles.

## ZIP archives

ZIP archives may contain the manifest at the archive root or inside one top-level directory. Archive paths are checked for traversal and symbolic links, and the unpacked size is limited.

## Compatibility

This is a new BEE2.5 draft format. It is not the BEE2.4 `.bee_pack` format. Legacy package conversion requires explicit format mapping and resource compatibility work.
