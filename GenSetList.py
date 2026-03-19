#!/usr/bin/env python3
"""Generate a combined ChordPro set list from numbered files in the current folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_OUTPUT = "00 - Set List.chopro"
NUMBER_PREFIX = re.compile(r"^(\d{2})(?!\d)")


def find_input_files(folder: Path, output_name: str) -> list[Path]:
    output_path = (folder / output_name).resolve()
    default_output_path = (folder / DEFAULT_OUTPUT).resolve()
    candidates: list[tuple[int, str, Path]] = []

    for path in folder.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() != ".chopro":
            continue
        match = NUMBER_PREFIX.match(path.name)
        if not match:
            continue
        resolved = path.resolve()
        if resolved in {output_path, default_output_path}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if text.count("{new_song}") > 1:
            continue
        number = int(match.group(1))
        candidates.append((number, path.name.lower(), path))

    candidates.sort(key=lambda item: (item[0], item[1]))
    return [item[2] for item in candidates]


def build_set_list(files: list[Path]) -> str:
    chunks: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if text and not text.endswith("\n"):
            text += "\n"
        stripped = text.lstrip("\ufeff \t\r\n")
        if stripped.startswith("{new_song}"):
            chunks.append(text)
        else:
            chunks.append("{new_song}\n" + text)
    return "".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Concatenate numbered .chopro files in the current folder into a set list."
        )
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output file name (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    folder = Path.cwd()
    files = find_input_files(folder, args.output)
    if not files:
        print("No matching .chopro files found.")
        return 1

    output_path = folder / args.output
    content = build_set_list(files)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path.name} with {len(files)} songs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
