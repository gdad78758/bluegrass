#!/usr/bin/env python3
"""Generate a combined ChordPro set list from numbered files in the current folder."""

from __future__ import annotations

import argparse
import random
import re
from datetime import datetime
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


def find_random_files(folders: list[Path], count: int) -> list[Path]:
    candidates: list[Path] = []
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.is_file() and path.suffix.lower() == ".chopro":
                candidates.append(path)
    if len(candidates) < count:
        return []
    return random.sample(candidates, count)


def log_random_selection(log_path: Path, files: list[Path]) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d")
    titles = [path.stem for path in files]
    lines = [f"{stamp}"] + [f"- {title}" for title in titles]
    with log_path.open("a", encoding="utf-8", errors="replace") as handle:
        handle.write("\n".join(lines) + "\n")


def write_song_list(output_path: Path, files: list[Path]) -> None:
    list_path = output_path.with_suffix(".txt")
    titles = [path.stem for path in files]
    list_path.write_text("\n".join(titles) + "\n", encoding="utf-8")


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
    parser.add_argument(
        "--random",
        action="store_true",
        help="Select 7 random songs from notes/set_list and Christmas",
    )
    args = parser.parse_args()

    folder = Path.cwd()
    if args.random:
        random_folders = [folder / "notes" / "set_list", folder / "Christmas"]
        files = find_random_files(random_folders, 7)
        if not files:
            print("Not enough .chopro files found for random selection.")
            return 1
        log_random_selection(folder / "random.log", files)
    else:
        files = find_input_files(folder, args.output)
    if not files:
        print("No matching .chopro files found.")
        return 1

    output_path = folder / args.output
    content = build_set_list(files)
    output_path.write_text(content, encoding="utf-8")
    write_song_list(output_path, files)
    print(f"Wrote {output_path.name} with {len(files)} songs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
