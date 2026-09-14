#!/usr/bin/env python3
"""Package a skill folder into a distributable .skill file.

Usage:
    python package_skill.py /path/to/skill [--output-dir ./dist]
"""

import fnmatch
import sys
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
ROOT_EXCLUDE_DIRS = {"evals"}


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Validate that a skill folder has the required structure."""
    if not skill_path.exists():
        return False, f"Skill folder not found: {skill_path}"
    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"
    if not (skill_path / "SKILL.md").exists():
        return False, "SKILL.md not found in skill folder"
    return True, "Valid skill"


def should_exclude(rel_path: Path) -> bool:
    """Check if a path should be excluded from packaging."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_skill(skill_path: Path, output_dir: Path | None = None) -> Path | None:
    """Package a skill folder into a .skill file."""
    valid, msg = validate_skill(skill_path)
    if not valid:
        print(f"Error: {msg}")
        return None

    skill_name = skill_path.name
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    skill_filename = output_dir / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob("*"):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname):
                    print(f"  Skipped: {arcname}")
                    continue
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

        print(f"Packaged: {skill_filename}")
        return skill_filename
    except Exception as e:
        print(f"Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <path/to/skill> [output-directory]")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None

    print(f"Packaging skill: {skill_path}")
    if output_dir:
        print(f"  Output: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
