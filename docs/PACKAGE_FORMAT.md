# BEE2.5 package format (draft)

A BEE2.5 package is a directory or ZIP archive with a UTF-8 JSON file named `bee25.json` at its root.

Example:

```json
{
  "id": "author.package-name",
  "name": "Package display name",
  "version": "1.0.0",
  "content": ["maps", "items", "styles", "skyboxes", "resources"]
}
```

## Fields

- `id`: stable identifier, 2–64 lowercase letters, digits, dots, underscores or hyphens.
- `name`: non-empty display name.
- `version`: semantic-style `MAJOR.MINOR.PATCH` version.
- `content`: optional list describing the kinds of content included.
- `kind`: optional descriptive field, for example `vmf_map`.

## Example layout

```text
example_package/
  bee25.json
  maps/
    example.vmf
  styles/
    my_style.json
  skyboxes/
    my_skybox.json
  materials/
    skybox/
      my_skybox.vmt
      ...
  models/
  sounds/
```

## Importing

- Folder import copies a package directory into the user's BEE2.5 package directory.
- ZIP import accepts archives containing `bee25.json` at the root or inside one top-level directory.
- VMF import creates a small package with a `maps/` folder and a generated manifest.

ZIP imports reject path traversal, symbolic links, and archives larger than 512 MiB after unpacking.

## Compatibility

This is an initial BEE2.5 format. The current importer does not yet parse legacy BEE2.4 `.bee_pack` archives or VPK files. It also does not yet interpret the example style/skybox JSON definitions; those are reserved package locations for the upcoming object schema.
