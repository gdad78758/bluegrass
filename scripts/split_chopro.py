#!/usr/bin/env python3
"""Split a multi-song .chopro file into individual song files.

Usage:
  python split_chopro.py path\\to\\setlist.chopro
  python split_chopro.py path\\to\\setlist.chopro --out-dir path\\to\\out
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

NEW_SONG = "{new_song}"
TITLE_PATTERNS = [
    re.compile(r"^\{\s*t\s*:\s*(.+?)\s*\}$", re.IGNORECASE),
    re.compile(r"^\{\s*title\s*:\s*(.+?)\s*\}$", re.IGNORECASE),
]
INVALID_FS_CHARS = re.compile(r"[<>:\"/\\|?*]")
MULTI_SPACE = re.compile(r"\s+")
TRAILING_DATE = re.compile(r"\s*-?\s*v\s*[-_]?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\s*$", re.IGNORECASE)


def sanitize_filename(name: str) -> str:
    name = name.strip()
    name = TRAILING_DATE.sub("", name)
    name = INVALID_FS_CHARS.sub("-", name)
    name = MULTI_SPACE.sub(" ", name).strip()
    name = name.strip(".")
    return name or "untitled"


def extract_title(lines: list[str]) -> str | None:
    for line in lines:
        text = line.strip()
        for pattern in TITLE_PATTERNS:
            match = pattern.match(text)
            if match:
                return match.group(1).strip()
    return None


def split_songs(text: str) -> list[list[str]]:
    lines = text.splitlines()
    songs: list[list[str]] = []
    current: list[str] = []
    in_song = False

    for line in lines:
        if line.strip() == NEW_SONG:
            if current:
                songs.append(current)
            current = []
            in_song = True
        else:
            if in_song:
                current.append(line)
            else:
                # Ignore anything before the first {new_song}
                continue

    if current:
        songs.append(current)

    return songs


def write_songs(songs: list[list[str]], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for idx, song_lines in enumerate(songs, start=1):
        title = extract_title(song_lines)
        if title:
            base = sanitize_filename(title)
        else:
            base = f"song-{idx:02d}"

        filename = f"{base}.chopro"
        path = out_dir / filename
        content = "\n".join(song_lines).rstrip() + "\n"
        path.write_text(content, encoding="utf-8")
        written.append(path)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a multi-song .chopro file into individual song files.")
    parser.add_argument("input_file", help="Path to the .chopro file to split")
    parser.add_argument(
        "--out-dir",
        help="Directory to write split files (default: input file directory)",
        default=None,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_file)
    if not input_path.is_file():
        raise SystemExit(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    songs = split_songs(text)
    if not songs:
        raise SystemExit("No songs found (missing {new_song} markers).")

    out_dir = Path(args.out_dir) if args.out_dir else input_path.parent

    written = write_songs(songs, out_dir)
    print(f"Wrote {len(written)} song files to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
