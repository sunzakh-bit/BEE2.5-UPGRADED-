"""Small, dependency-free VMF structural validator.

This checks text encoding, quoted strings, and brace balance. It does not replace
Hammer/Source map validation or guarantee that a VMF can be compiled.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class VMFError(ValueError):
    """Raised when a VMF file is structurally invalid."""


@dataclass(frozen=True, slots=True)
class VMFInfo:
    path: Path
    size_bytes: int
    block_count: int
    world_count: int
    entity_count: int


def validate_vmf_text(text: str) -> tuple[int, int, int]:
    depth = 0
    blocks = 0
    quoted = False
    escaped = False
    line_comment = False
    index = 0

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue

        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
            continue

        if char == "/" and next_char == "/":
            line_comment = True
            index += 2
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            depth += 1
            blocks += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                raise VMFError("unexpected closing brace")
        index += 1

    if quoted:
        raise VMFError("unterminated quoted string")
    if depth != 0:
        raise VMFError(f"unbalanced braces: {depth} block(s) were not closed")
    if blocks == 0:
        raise VMFError("file contains no VMF blocks")

    world_count = len(re.findall(r"(?mi)^\s*world\s*$", text))
    entity_count = len(re.findall(r"(?mi)^\s*entity\s*$", text))
    if world_count == 0:
        raise VMFError("VMF has no world block")
    return blocks, world_count, entity_count


def inspect_vmf(path: Path) -> VMFInfo:
    path = path.expanduser()
    if not path.is_file():
        raise VMFError(f"VMF file does not exist: {path}")
    if path.suffix.lower() != ".vmf":
        raise VMFError("expected a .vmf file")

    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise VMFError("VMF must be readable as UTF-8 text") from exc

    blocks, worlds, entities = validate_vmf_text(text)
    return VMFInfo(
        path=path.resolve(),
        size_bytes=path.stat().st_size,
        block_count=blocks,
        world_count=worlds,
        entity_count=entities,
    )
