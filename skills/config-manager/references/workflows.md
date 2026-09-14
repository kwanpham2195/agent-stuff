# Config Manager Workflows

## Chezmoi Edit

Use this sequence for managed dotfiles:

```bash
cd "$HOME/.local/share/chezmoi"
git status -sb
chezmoi diff ~/.zshrc
```

Edit the source file, then:

```bash
chezmoi diff ~/.zshrc
chezmoi apply ~/.zshrc
```

If `chezmoi apply` prompts but the diff is already reviewed:

```bash
chezmoi apply --force ~/.zshrc
```

Use `--force` only for the exact target already inspected.

## Managed agent and Pi configuration

Chezmoi source is authoritative for durable agent and Pi configuration:

```text
dot_agents/       -> $HOME/.agents
dot_pi/private_agent/     -> $HOME/.pi/agent
```

For global instructions, edit `dot_agents/AGENTS.md`. Codex reads `$HOME/.codex/AGENTS.md`, which resolves through `~/.agents/AGENTS.md` after the narrow `~/.agents` apply.

For skills, edit `dot_agents/skills/<skill-name>`, then inspect and apply only `~/.agents`. For durable Pi configuration, edit `dot_pi/private_agent`, then inspect and apply only `~/.pi/agent`.

Before adding any Pi or agent file, run the path-only installer audit below, secret-scan the exact candidate outside the repository, and keep secrets, chat data, runtime state, generated dependencies, and external symlinks unmanaged.

```bash
cd "$HOME/.local/share/chezmoi"
chezmoi diff --recursive ~/.agents
chezmoi apply --recursive ~/.agents
chezmoi diff --recursive ~/.pi/agent
chezmoi apply --recursive ~/.pi/agent
```

## Reconcile config drift

Use this workflow only when the user says `audit config drift`. It is read-only until the user approves a reconciliation.

Chezmoi source is authoritative. A change made by Brew, an installer, `npx`, or a person is a proposal. Do not trust it automatically.

### Existing managed file

Inspect one exact target first:

```bash
cd "$HOME/.local/share/chezmoi"
chezmoi status <exact-target>
chezmoi diff <exact-target>
```

Accept a reviewed change by editing or merging it into the source. Reject it by applying that exact target:

```bash
chezmoi apply <exact-target>
```

`chezmoi merge <exact-target>` helps merge a reviewed live change into a plain source file. Use it only when the source is plain and the result is reviewed. It does not safely replace a template or encrypted source, and it is not a tree-wide reconciliation command.

`chezmoi add <exact-target>` writes a source representation from the live file. Use it only for a plain, reviewed file after accepting the proposal. Do not use it for templates or encrypted sources. Never run broad `chezmoi re-add`, `chezmoi add ~/.agents`, or `chezmoi add ~/.pi`.

### Managed agent and Pi trees

Directory diff without `--recursive` is insufficient. Inspect both trees explicitly:

```bash
cd "$HOME/.local/share/chezmoi"
chezmoi status --recursive ~/.agents ~/.pi/agent
chezmoi diff --recursive ~/.agents
chezmoi diff --recursive ~/.pi/agent
```

### New installer files

Ordinary `chezmoi status` does not show unmanaged files. After `npx skills install`, inventory the installer-controlled skill roots without following symlinks and report paths only. Secret-scan a candidate before reading or copying it. Never print secret values. Modified managed files and mode or symlink changes still come from the preceding recursive `chezmoi status` and `chezmoi diff` commands.

Run this path-only audit from the chezmoi source. Chezmoi managed paths are the durable inventory. It uses Python 3 standard library only, does not read live file contents, prunes generated subtrees, shows at most 50 paths per group, and exits nonzero only for unmanaged candidates.

```bash
python3 - <<'PY'
from __future__ import annotations

import fnmatch
import os
import subprocess
from pathlib import Path

roots = {
    "agents": (Path.home() / ".agents" / "skills", {"**/.DS_Store", "**/.ruff_cache/**", "**/__pycache__/**", "**/*.pyc", "**/node_modules/**"}),
    "pi": (Path.home() / ".pi" / "agent" / "skills", {"**/.DS_Store", "**/.ruff_cache/**", "**/__pycache__/**", "**/*.pyc", "**/node_modules/**"}),
}
limit = 50


def matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(path, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatchcase(path, pattern[3:])
    )


def excluded_subtree(path: str, patterns: set[str]) -> bool:
    return any(
        pattern.endswith("/**") and matches(path, pattern[:-3])
        for pattern in patterns
    )


def live_paths(root: Path, patterns: set[str]) -> tuple[set[str], set[str]]:
    paths: set[str] = set()
    pruned: set[str] = set()
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                if entry.is_symlink():
                    paths.add(relative)
                elif entry.is_dir(follow_symlinks=False):
                    if excluded_subtree(relative, patterns):
                        pruned.add(f"{relative}/**")
                    else:
                        pending.append(path)
                elif entry.is_file(follow_symlinks=False):
                    paths.add(relative)
    return paths, pruned


def managed_paths(root: Path) -> set[str]:
    result = subprocess.run(
        ["chezmoi", "managed", "--include=files,symlinks", str(root)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    paths = set()
    for path in result.stdout.splitlines():
        if not path:
            continue
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = Path.home() / candidate
        paths.add(candidate.relative_to(root).as_posix())
    return paths


def report(name: str, label: str, paths: set[str]) -> None:
    ordered = sorted(paths)
    print(f"{name}: {label} ({len(ordered)})")
    for path in ordered[:limit]:
        print(path)
    if len(ordered) > limit:
        print(f"... {len(ordered) - limit} more")


exit_code = 0
for name, (root, patterns) in roots.items():
    live, pruned = live_paths(root, patterns)
    managed = managed_paths(root)
    excluded = {path for path in live if any(matches(path, rule) for rule in patterns)} | pruned
    candidates = live - managed - excluded
    report(name, "unmanaged candidates", candidates)
    report(name, "managed paths missing live", managed - live)
    report(name, "excluded paths", excluded)
    exit_code |= bool(candidates)

raise SystemExit(exit_code)
PY
```


Classify every candidate as one of these:

- Owned source: add one reviewed source path after approval.
- Third-party or generated content: keep it unmanaged and represent its generator with a Brewfile, mise entry, or third-party skill declaration or lock.
- Excluded runtime state: leave it unmanaged. This includes Pi runtime data, chat data, caches, sessions, auth, and generated dependencies.

Keep churning files unmanaged. Manage generator inputs instead. Neovim remains an independent repository.

### Drift report

Report these groups separately:

- Modified managed files
- Missing managed files
- Unknown live files
- Excluded files
- Mode or symlink changes
- Recommended action

Do not edit source, add files, merge, or apply anything until the user approves the reconciliation.

## Skill Work

Create and edit managed local skills under:

```text
$HOME/.local/share/chezmoi/dot_agents/skills
```

Before edits:

```bash
cd "$HOME/.local/share/chezmoi"
git status -sb
```

After `SKILL.md` edits:

```bash
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" dot_agents/skills/<skill-name>
```

## Node Tooling Cleanup

Check active resolution:

```bash
zsh -ic 'which node; which npm; which npx; node -v; npm -v; npm config get prefix'
zsh -ic 'mise doctor'
```

Remove obsolete local shims with Trash:

```bash
trash ~/.local/bin/node ~/.local/bin/npm ~/.local/bin/npx
```

Manage global npm CLIs through mise config:

```toml
[tools]
node = "22.22.3"
"npm:@example/cli" = "latest"
```

Then install and verify:

```bash
mise install
mise ls
zsh -ic '<cli> --version'
```

## Package Management

Durable Homebrew package changes go through chezmoi:

```bash
cd "$HOME/.local/share/chezmoi"
git status -sb
rg -n 'brew "(package-name)"|cask "(package-name)"' dot_brewfile.tmpl
```

Edit `dot_brewfile.tmpl`, then:

```bash
chezmoi diff ~/.brewfile
chezmoi apply ~/.brewfile
brew bundle --file ~/.brewfile
brew list --versions <package-name>
```

For removals:

```bash
brew uses --installed <package-name>
brew leaves | rg '^<package-name>$'
```

Only uninstall after checking references in chezmoi and shell config:

```bash
rg -n '<package-name>|<command-name>' "$HOME/.local/share/chezmoi"
```

Durable global CLI tools should usually use mise:

```toml
[tools]
"npm:<package-name>" = "latest"
"go:<module-path>" = "latest"
"pipx:<package-name>" = "latest"
```

Then:

```bash
chezmoi apply ~/.config/mise/config.toml
mise install
mise ls
zsh -ic 'which <command-name>; <command-name> --version'
```

Use direct installs only for urgent live repair or explicit user requests. If the package should survive rebuilds, add it to Brewfile or mise config in the same task.

## Safety Checks

- If live target differs from source in unrelated lines, do not broad-apply; patch narrowly or ask.
- If a command would write outside the active writable root, request escalation.
- If removing files, use `trash`, not `rm`.
- Keep final response explicit about what was applied live versus only edited in source.
