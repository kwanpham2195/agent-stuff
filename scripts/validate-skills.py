#!/usr/bin/env python3
"""Validate local skill metadata and common cross-file references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIRS = (ROOT / "skills", ROOT / "pi" / "skills")
LONG_DESCRIPTION_LIMIT = 350
DEAD_SKILL_NAMES = ("github-pr-workflow",)


def load_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "missing frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "unterminated frontmatter"

    raw = text[4:end]
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            return None, "frontmatter is not a mapping"
        return data, None
    except ImportError:
        data: dict[str, str] = {}
        for line in raw.splitlines():
            match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if match:
                key, value = match.groups()
                data[key] = value.strip().strip("\"'")
        return data, None
    except Exception as exc:  # pragma: no cover - depends on installed parser
        return None, f"invalid YAML frontmatter: {exc}"


def code_spans_and_links(text: str) -> list[str]:
    candidates: list[str] = []
    candidates.extend(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    candidates.extend(re.findall(r"`([^`\n]+)`", text))
    return candidates


def path_tokens(raw: str) -> list[str]:
    cleaned = raw.strip().strip("<>,.;:")
    if not cleaned or cleaned.startswith(("http://", "https://", "mailto:")):
        return []

    tokens = re.split(r"\s+", cleaned)
    result: list[str] = []
    for token in tokens:
        token = token.strip().strip("\"'()[],.;:")
        if not token or token in {"bash", "sh", "python", "python3", "node"}:
            continue
        token = token.split("#", 1)[0]
        if looks_like_local_ref(token):
            result.append(token)
    return result


def looks_like_local_ref(token: str) -> bool:
    if token.startswith(("<skill-dir>/", "$", "/", "~")):
        return False
    if token.startswith(("references/", "scripts/", "templates/", "../", "./", "skills/")):
        return True
    if token in {"PRD-TEMPLATE.md", "ISSUE-TEMPLATE.md", "UPSTREAM.md", "TRACKER-MAPPING.md"}:
        return True
    if re.match(r"^[A-Za-z0-9_.-]+/(references|scripts|templates)/", token):
        return True
    if token.endswith(("/TRACKER-MAPPING.md", "/PRD-TEMPLATE.md", "/ISSUE-TEMPLATE.md", "/UPSTREAM.md")):
        return True
    return False


def resolve_ref(skill_path: Path, token: str) -> Path:
    resolved = resolve_literal_ref(skill_path, token)
    if resolved.exists():
        return resolved
    # Chezmoi stores an executable target with this source filename prefix.
    executable_source = resolved.with_name("executable_" + resolved.name)
    if executable_source.is_file():
        return executable_source
    return resolved


def resolve_literal_ref(skill_path: Path, token: str) -> Path:
    if token.startswith("skills/"):
        return ROOT / token
    if token.startswith(("../", "./", "references/", "scripts/", "templates/")):
        return skill_path.parent / token

    parts = token.split("/", 1)
    if len(parts) == 2:
        sibling = skill_path.parent.parent / parts[0] / parts[1]
        if sibling.exists():
            return sibling
    return skill_path.parent / token


def validate_refs(skill_path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for raw in code_spans_and_links(text):
        for token in path_tokens(raw):
            resolved = resolve_ref(skill_path, token)
            if not resolved.exists():
                rel = skill_path.relative_to(ROOT)
                errors.append(f"{rel}: missing referenced file `{token}`")
    return errors


def should_check_refs(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if len(rel.parts) >= 2 and rel.parts[1] == "pstack":
        return False
    if len(rel.parts) >= 2 and rel.parts[1].startswith("plannotator"):
        return False
    return True


def validate_lockfile() -> list[str]:
    lock_path = ROOT / ".skill-lock.json"
    if not lock_path.exists():
        return []
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f".skill-lock.json: invalid JSON: {exc}"]

    warnings: list[str] = []
    missing = []
    for name, item in sorted((data.get("skills") or {}).items()):
        skill_path = item.get("skillPath") if isinstance(item, dict) else None
        if skill_path and not (ROOT / skill_path).exists():
            missing.append(f"{name} -> {skill_path}")

    if missing:
        sample = "; ".join(missing[:8])
        suffix = "" if len(missing) <= 8 else f"; +{len(missing) - 8} more"
        warnings.append(f".skill-lock.json: {len(missing)} missing skillPath entries: {sample}{suffix}")
    return warnings


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    names: dict[str, Path] = {}
    skill_paths = sorted(path for directory in SKILLS_DIRS if directory.exists() for path in directory.rglob("SKILL.md"))

    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        data, error = load_frontmatter(path)
        if error:
            errors.append(f"{rel}: {error}")
            continue

        assert data is not None
        unsupported = set(data) - {"name", "description", "license", "allowed-tools", "metadata", "disable-model-invocation", "argument-hint"}
        if unsupported:
            errors.append(f"{rel}: unsupported frontmatter fields: {', '.join(sorted(unsupported))}")
        invocation = data.get("disable-model-invocation")
        if invocation is not None and not isinstance(invocation, bool) and invocation not in ("true", "false"):
            errors.append(f"{rel}: `disable-model-invocation` must be a boolean")
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{rel}: missing non-empty `name`")
        elif name in names:
            errors.append(f"{rel}: duplicate skill name `{name}` also in {names[name].relative_to(ROOT)}")
        else:
            names[name] = path
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                errors.append(f"{rel}: invalid skill name `{name}`")
            if name != path.parent.name:
                errors.append(f"{rel}: name must match skill directory `{path.parent.name}`")

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{rel}: missing non-empty `description`")
        else:
            if len(description) > 1024 or "<" in description or ">" in description:
                errors.append(f"{rel}: description must be at most 1024 characters without angle brackets")
            if len(description) > LONG_DESCRIPTION_LIMIT:
                warnings.append(f"{rel}: long description ({len(description)} chars)")

        for dead_name in DEAD_SKILL_NAMES:
            if dead_name in text:
                errors.append(f"{rel}: stale skill reference `{dead_name}`")

        if should_check_refs(path):
            errors.extend(validate_refs(path, text))

    warnings.extend(validate_lockfile())

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(skill_paths)} skills checked, {len(errors)} errors, {len(warnings)} warnings")
        return 1

    print(f"OK: {len(skill_paths)} skills validated, {len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
