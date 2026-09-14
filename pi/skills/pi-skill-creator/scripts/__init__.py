"""Shared utilities for agent-skill-creator scripts."""

import os
from pathlib import Path

# Agent configurations
AGENTS = {
    "codex": {
        "cli": "codex",
        "headless_flag": "-p",
        "session_db": "~/.codex/sessions/",
        "project_marker": ".codex",
    },
    "opencode": {
        "cli": "opencode",
        "headless_flag": "run",
        "session_db": "~/.local/share/opencode/",
        "project_marker": ".opencode",
    },
    "pi": {
        "cli": "pi",
        "headless_flag": "-p",
        "session_db": "~/.pi/sessions/",
        "project_marker": ".pi",
    },
}


def get_agent() -> str:
    """Return the agent name from AGENT env var, defaulting to opencode."""
    return os.environ.get("AGENT", "opencode").lower()


def get_agent_config(agent: str | None = None) -> dict:
    """Return config dict for the given agent."""
    agent = agent or get_agent()
    if agent not in AGENTS:
        raise ValueError(f"Unknown agent: {agent}. Available: {list(AGENTS.keys())}")
    return AGENTS[agent]


def get_cli() -> str:
    """Return the CLI command for the current agent."""
    return get_agent_config()["cli"]


def find_project_root(start: Path | None = None) -> Path:
    """Find the project root by walking up looking for agent markers.

    Searches for (in order):
    - AGENTS.md (generic, all agents respect this)
    - .claude/ (Claude Code marker)
    - .codex/ (Codex marker)
    - .opencode/ (OpenCode marker)
    - .pi/ (pi marker)
    """
    current = start or Path.cwd()
    markers = ["AGENTS.md", ".claude", ".codex", ".opencode", ".pi"]

    for parent in [current, *current.parents]:
        for marker in markers:
            if (parent / marker).exists():
                return parent
        # Also check for pyproject.toml or package.json as generic project indicators
        if (parent / "pyproject.toml").exists() or (parent / "package.json").exists():
            return parent
    return current


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value in (">", "|", ">-", "|-"):
                continuation_lines: list[str] = []
                i += 1
                while i < len(frontmatter_lines) and (
                    frontmatter_lines[i].startswith("  ")
                    or frontmatter_lines[i].startswith("\t")
                ):
                    continuation_lines.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation_lines)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    return name, description, content
