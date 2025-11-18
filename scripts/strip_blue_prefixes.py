"""Clean up legacy &blue prefixed lines in .chopro files.

Usage examples:
    python scripts/strip_blue_prefixes.py                   # scan repo root
    python scripts/strip_blue_prefixes.py Christmas/*.chopro # specific files
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
import re
from typing import Iterable, List, Sequence, Tuple

PREFIX_RE = re.compile(r"^\s*(?:/?&blue/?)(?:\s*:)?\s*", re.IGNORECASE)
MARKER_OPEN = "{textcolour: blue}"
MARKER_CLOSE = "{textcolour}"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Strip legacy &blue prefixes and wrap affected sections in textcolour tags.",
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


def detect_line_ending(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    if "\n" in text:
        return "\n"
    if "\r" in text:
        return "\r"
    return "\n"


def strip_prefix(line: str) -> Tuple[str, bool]:
    newline = ""
    if line.endswith("\r\n"):
        core, newline = line[:-2], "\r\n"
    elif line.endswith("\n"):
        core, newline = line[:-1], "\n"
    elif line.endswith("\r"):
        core, newline = line[:-1], "\r"
    else:
        core = line

    match = PREFIX_RE.match(core)
    if not match:
        return line, False

    stripped = core[match.end():] + newline
    return stripped, True


def transform_lines(lines: Sequence[str], line_ending: str) -> Tuple[List[str], bool]:
    result: List[str] = []
    in_blue_block = False
    changed = False

    for line in lines:
        stripped_line, had_prefix = strip_prefix(line)
        if had_prefix:
            if not in_blue_block:
                result.append(f"{MARKER_OPEN}{line_ending}")
                in_blue_block = True
                changed = True
            result.append(stripped_line)
            if stripped_line != line:
                changed = True
        else:
            if in_blue_block:
                result.append(f"{MARKER_CLOSE}{line_ending}")
                in_blue_block = False
                changed = True
            result.append(line)

    if in_blue_block:
        result.append(f"{MARKER_CLOSE}{line_ending}")
        changed = True

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

    line_ending = detect_line_ending(text)
    lines = text.splitlines(keepends=True)
    if text and not lines:
        lines = [text]

    updated_lines, changed = transform_lines(lines, line_ending)
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
