#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""Organize files by extension, with a dry run by default."""
import argparse
import os
from pathlib import Path

EXTENSIONS = {
    "jpeg": "Images", "png": "Images", "jpg": "Images", "tiff": "Images", "gif": "Images",
    "mp4": "Videos", "mkv": "Videos", "mov": "Videos", "webm": "Videos", "flv": "Videos",
    "mp3": "Music", "ogg": "Music", "wav": "Music", "flac": "Music",
    "py": "Program Files", "js": "Program Files", "cpp": "Program Files",
    "html": "Program Files", "css": "Program Files", "c": "Program Files", "sh": "Program Files",
    "pdf": "Documents", "doc": "Documents", "docx": "Documents", "txt": "Documents",
    "ppt": "Documents", "ods": "Documents", "csv": "Documents",
}

def plan(directory: Path) -> list[tuple[Path, Path]]:
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Directory must exist and must not be a symlink")
    operations = []
    for source in sorted(directory.iterdir(), key=lambda p: p.name.casefold()):
        if source.name.startswith(".") or source.is_symlink() or not source.is_file():
            continue
        category = EXTENSIONS.get(source.suffix.lower().lstrip("."), "Miscellaneous")
        operations.append((source, directory / category / source.name))
    return operations

def organize(directory: Path, *, apply: bool = False) -> tuple[int, int]:
    completed = skipped = 0
    for source, destination in plan(directory):
        if destination.exists() or destination.is_symlink():
            print(f"SKIP existing destination: {destination}")
            skipped += 1
            continue
        if not apply:
            print(f"DRY-RUN {source.name} -> {destination.parent.name}/")
            continue
        destination.parent.mkdir(exist_ok=True)
        try:
            # Reserve destination without overwriting it, on the same filesystem.
            os.link(source, destination, follow_symlinks=False)
        except FileExistsError:
            print(f"SKIP collision: {destination}")
            skipped += 1
            continue
        except OSError as exc:
            print(f"SKIP cannot safely move {source.name}: {exc}")
            skipped += 1
            continue
        source.unlink()
        print(f"MOVED {source.name} -> {destination.parent.name}/")
        completed += 1
    return completed, skipped

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--apply", action="store_true", help="Move files; default is preview")
    args = parser.parse_args()
    try:
        moved, skipped = organize(args.directory, apply=args.apply)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"Moved: {moved}; skipped: {skipped}")

if __name__ == "__main__":
    main()
