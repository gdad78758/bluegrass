#!/usr/bin/env python3
"""Reverse the formatting performed by strip_blue_prefixes.py.

Usage examples:
    python scripts/restore_blue_prefixes.py                   # scan repo root
    python scripts/restore_blue_prefixes.py Christmas/*.chopro # specific files
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

MARKER_OPEN_RE = re.compile(r"^\s*\{textcolour:\s*blue\}\s*$", re.IGNORECASE)
MARKER_CLOSE_RE = re.compile(r"^\s*\{textcolour\}\s*$", re.IGNORECASE)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Restore legacy &blue prefixes by replacing blue textcolour blocks.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path.cwd()],
        help="Files or directories to process (defaults to current working directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would change without writing updates.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file status messages (still returns non-zero exit on failure).",
    )
    return parser.parse_args(argv)


def split_line_ending(line: str) -> Tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def transform_lines(lines: Sequence[str]) -> Tuple[List[str], bool]:
    result: List[str] = []
    in_blue_block = False
    changed = False

    for line in lines:
        core, newline = split_line_ending(line)

        if MARKER_OPEN_RE.match(core):
            if not in_blue_block:
                in_blue_block = True
                changed = True
                continue

        if MARKER_CLOSE_RE.match(core):
            if in_blue_block:
                in_blue_block = False
                changed = True
                continue

        if in_blue_block:
            result.append("/&blue:" + core + newline)
            changed = True
        else:
            result.append(line)

    return result, changed


def iter_chopro_targets(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".chopro":
            yield path
        elif path.is_dir():
            for candidate in sorted(path.rglob("*.chopro")):
                if candidate.is_file():
                    yield candidate


def process_file(path: Path, dry_run: bool, quiet: bool) -> bool:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"Failed to read {path}: {exc}", file=sys.stderr)
        return False

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print(f"Skipping {path} (not valid UTF-8)", file=sys.stderr)
        return False

    lines = text.splitlines(keepends=True)
    if text and not lines:
        lines = [text]

    updated_lines, changed = transform_lines(lines)
    if not changed:
        if not quiet:
            print(f"✓ {path} (no changes)")
        return True

    if dry_run:
        if not quiet:
            print(f"• {path} (would update)")
        return True

    try:
        path.write_text("".join(updated_lines), encoding="utf-8", newline="")
    except OSError as exc:
        print(f"Failed to write {path}: {exc}", file=sys.stderr)
        return False

    if not quiet:
        print(f"✎ {path} (updated)")
    return True


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    targets = list(iter_chopro_targets(args.paths))
    if not targets:
        print("No .chopro files found for the provided paths.", file=sys.stderr)
        return 1

    overall_ok = True
    for path in targets:
        if not process_file(path, dry_run=args.dry_run, quiet=args.quiet):
            overall_ok = False

    return 0 if overall_ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
