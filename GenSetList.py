#!/usr/bin/env python3
"""Generate a combined ChordPro set list from numbered files in the current folder."""

from __future__ import annotations

import argparse
import random
import re
from datetime import datetime
from pathlib import Path


DEFAULT_OUTPUT = "Set List.chopro"
DEFAULT_LIST = Path("notes") / "set_list" / "setlist.txt"
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


def find_files_from_list(list_path: Path, set_list_folder: Path) -> list[Path]:
    """Return ordered .chopro files based on titles listed in list_path."""
    files: list[Path] = []
    for line in list_path.read_text(encoding="utf-8", errors="replace").splitlines():
        title = line.strip()
        if not title:
            continue
        chopro = set_list_folder / f"{title}.chopro"
        if chopro.is_file():
            files.append(chopro)
    return files


def find_random_files(folders: list[Path], count: int) -> list[Path]:
    candidates: list[Path] = []
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if not path.is_file():
                continue
            if path.name.startswith("00"):
                continue
            if path.suffix.lower() == ".chopro":
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
    list_path = output_path.with_suffix(".html")
    titles = [path.stem for path in files]
    title = output_path.stem
    items = "\n".join(f"    <li>{name}</li>" for name in titles)
    html = (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "  <head>\n"
        "    <meta charset=\"utf-8\">\n"
        f"    <title>{title}</title>\n"
        "  </head>\n"
        "  <body>\n"
        f"    <h1>{title}</h1>\n"
        "    <ul>\n"
        f"{items}\n"
        "    </ul>\n"
        "  </body>\n"
        "</html>\n"
    )
    list_path.write_text(html, encoding="utf-8")


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
        help="Select 7 random songs: 2 from Christmas, 5 from notes/set_list",
    )
    parser.add_argument(
        "--list",
        default=None,
        metavar="FILE",
        help=(
            f"Text file with song titles (one per line) in desired order "
            f"(default when present: {DEFAULT_LIST})"
        ),
    )
    args = parser.parse_args()

    folder = Path.cwd()
    set_list_folder = folder / "notes" / "set_list"

    # Determine list file path
    if args.list:
        list_path: Path | None = Path(args.list)
    elif (folder / DEFAULT_LIST).is_file():
        list_path = folder / DEFAULT_LIST
    else:
        list_path = None

    if list_path and not args.random:
        files = find_files_from_list(list_path, set_list_folder)
        if not files:
            print(f"No matching .chopro files found for titles in {list_path}.")
            return 1
    elif args.random:
        christmas_files = find_random_files([folder / "Christmas"], 2)
        set_list_files = find_random_files([folder / "notes" / "set_list"], 5)
        if not christmas_files or not set_list_files:
            print("Not enough .chopro files found for random selection.")
            return 1
        files = christmas_files + set_list_files
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
