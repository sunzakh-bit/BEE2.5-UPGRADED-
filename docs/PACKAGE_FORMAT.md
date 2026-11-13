# Package format (draft)

Each BEE2.5 package starts with a UTF-8 JSON file named `bee25.json`.

Example:

```json
{
  "id": "author.package-name",
  "name": "Package display name",
  "version": "1.0.0",
  "content": ["items", "instances", "resources"]
}
```

## Fields

- `id`: stable identifier, 2–64 lowercase letters, digits, dots, underscores or hyphens.
- `name`: non-empty display name.
- `version`: semantic-style `MAJOR.MINOR.PATCH` version.
- `content`: optional list describing the kinds of content included.

This is an initial BEE2.5 format, not a claim of BEE2.4 package compatibility. The format may change before a stable release.
