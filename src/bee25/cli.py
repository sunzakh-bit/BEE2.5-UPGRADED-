"""Command-line interface for BEE2.5."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from bee25.packages.manifest import ManifestError, load_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bee25", description="BEE2.5 development tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate-package", help="Validate a package's bee25.json manifest"
    )
    validate.add_argument("package_dir", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "validate-package":
        try:
            manifest = load_manifest(args.package_dir)
        except (ManifestError, OSError, json.JSONDecodeError) as exc:
            print(f"Invalid package: {exc}", file=sys.stderr)
            return 1

        print(f"Package OK: {manifest.package_id} ({manifest.version})")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
