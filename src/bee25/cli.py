"""Command-line interface for BEE2.5."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from bee25.packages.manager import PackageManager
from bee25.packages.manifest import ManifestError, load_manifest
from bee25.packages.vmf import VMFError, inspect_vmf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bee25", description="BEE2.5 package and map tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("gui", help="Launch the desktop interface")

    validate = subparsers.add_parser(
        "validate-package", help="Validate a package's bee25.json manifest"
    )
    validate.add_argument("package_dir", type=Path)

    inspect = subparsers.add_parser("inspect-vmf", help="Check a VMF file's basic structure")
    inspect.add_argument("vmf_file", type=Path)

    import_vmf = subparsers.add_parser("import-vmf", help="Create a package from a VMF file")
    import_vmf.add_argument("vmf_file", type=Path)
    import_vmf.add_argument("--id", required=True, dest="package_id")
    import_vmf.add_argument("--name", required=True)
    import_vmf.add_argument("--version", default="1.0.0")

    export = subparsers.add_parser("export-vmf", help="Compile a VMF into Portal 2")
    export.add_argument("vmf_file", type=Path)
    export.add_argument("portal2_directory", type=Path)
    export.add_argument("--map-name")
    export.add_argument("--style", default="clean")
    export.add_argument("--skybox", default="game_default")
    export.add_argument("--voice", default="glados")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "gui":
        try:
            from bee25.ui.app import run
            run()
        except ImportError as exc:
            print(f"Could not launch desktop UI: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.command == "validate-package":
        try:
            manifest = load_manifest(args.package_dir)
        except (ManifestError, OSError, json.JSONDecodeError) as exc:
            print(f"Invalid package: {exc}", file=sys.stderr)
            return 1
        print(f"Package OK: {manifest.package_id} ({manifest.version})")
        return 0

    if args.command == "inspect-vmf":
        try:
            info = inspect_vmf(args.vmf_file)
        except (VMFError, OSError) as exc:
            print(f"Invalid VMF: {exc}", file=sys.stderr)
            return 1
        print(
            f"VMF OK: {info.path.name} | {info.size_bytes} bytes | "
            f"{info.block_count} blocks | {info.entity_count} entities"
        )
        return 0

    if args.command == "import-vmf":
        try:
            package, info = PackageManager().create_vmf_package(
                args.vmf_file, args.package_id, args.name, args.version
            )
        except (ValueError, OSError, VMFError, ManifestError) as exc:
            print(f"Could not import VMF: {exc}", file=sys.stderr)
            return 1
        print(f"Created package: {package.path} ({info.entity_count} entities)")
        return 0

    if args.command == "export-vmf":
        from bee25.export.portal2 import ExportError, export_vmf_to_portal2
        try:
            result = export_vmf_to_portal2(
                args.vmf_file,
                args.portal2_directory,
                args.map_name,
                style_id=args.style,
                skybox_id=args.skybox,
                voice_id=args.voice,
                progress=print,
            )
        except (ExportError, OSError, ValueError) as exc:
            print(f"Export failed: {exc}", file=sys.stderr)
            return 1
        print(f"Exported BSP: {result.bsp_path}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
