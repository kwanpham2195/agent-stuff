---
name: config-manager
description: "Manage local machine configuration through chezmoi and global config files. Use when the user asks about dotfiles, PATH, Brewfile, package managers, Codex config, or config drift."
---

# Config Manager

Use this skill for user-machine configuration that should be grounded in the current checkout and applied safely to live home files.

## Ground Rules

- Start in `$HOME/.local/share/chezmoi` for dotfiles work.
- Run `git status -sb` before edits; preserve unrelated dirty work.
- Treat chezmoi source as truth. Inspect live targets only to understand drift.
- Prefer `chezmoi diff <target>` before `chezmoi apply <target>`.
- Apply single targets. Avoid whole-repo `chezmoi apply` unless explicitly requested.
- Use `apply_patch` for source edits. Do not overwrite tracked files from live home files.
- Use `trash ...` for removing local files or shims.
- Do not push or commit unless asked.

## Config drift

Use this workflow when the user says `audit config drift`.

- Chezmoi source is authoritative. A change made by Brew, an installer, `npx`, or a person is a proposal, not an accepted source change.
- For one managed file, run `chezmoi status <exact target>` and `chezmoi diff <exact target>`. Accept it by editing or merging the reviewed change into source. Reject it with `chezmoi apply <exact target>`.
- For managed trees, run `chezmoi status --recursive ~/.agents ~/.pi/agent` and recursive diffs for both targets. A directory diff without `--recursive` is not enough.
- Never run broad `chezmoi re-add`, `chezmoi add ~/.agents`, or `chezmoi add ~/.pi`. Do not replace template or encrypted source from rendered live files.
- New unmanaged files need a path-only audit and secret scan. Classify them as owned source, third-party/generated content with a declaration or lock, or excluded runtime state. Never follow symlinks or print secret values.

See `references/workflows.md` for the reconciliation commands and report format.

## Common Paths

- Chezmoi source: `$HOME/.local/share/chezmoi`
- Home target: `$HOME`
- Global Codex instructions: `$HOME/.codex/AGENTS.md`
- Agent source: `dot_agents/` (target: `$HOME/.agents`)
- Pi agent source: `dot_pi/private_agent/` (target: `$HOME/.pi/agent`)
- Global AGENTS source: `dot_agents/AGENTS.md`
- Local skills source: `dot_agents/skills`
- Codex config: `$HOME/.codex/config.toml`
- Brewfile source: `dot_brewfile.tmpl`
- Brewfile target: `$HOME/.brewfile`
- mise config source: `dot_config/mise/config.toml`
- mise config target: `$HOME/.config/mise/config.toml`

## Workflow

1. Inspect:
   - `git status -sb`
   - `chezmoi managed | rg '<target-name>'`
   - `chezmoi diff <live-target>` for managed targets
2. Edit source:
   - dotfiles in the chezmoi checkout
   - global AGENTS in `dot_agents/AGENTS.md`
   - skills in `dot_agents/skills/<skill-name>`
   - durable Pi configuration in `dot_pi/private_agent/`
   - add Pi or agent files only after a path-only audit and secret scan; do not copy runtime state or external symlinks
3. Apply narrowly:
   - `chezmoi apply --recursive ~/.agents`
   - `chezmoi apply --recursive ~/.pi/agent`
   - `chezmoi apply ~/.zshrc`
   - `chezmoi apply ~/.shell/init`
   - `chezmoi apply ~/.config/mise/config.toml`
4. Verify from a fresh shell when shell/PATH/tooling changed:
   - `zsh -ic 'which node; which npm; npm config get prefix'`
   - `zsh -ic 'mise doctor'`
   - `which -a <cmd>` when shadowing is suspected

### Chezmoi synchronization and removals

- Chezmoi does not watch the source checkout. After editing `dot_agents/` or `dot_pi/private_agent/`, inspect the exact recursive diff and run the matching narrow apply command.
- `chezmoi apply --recursive ~/.agents` updates managed entries only. It does not remove a live path whose source entry was deleted; that path becomes unmanaged, and `chezmoi diff` may still be clean.
- After source deletions, inspect `chezmoi unmanaged ~/.agents/skills`. Remove only confirmed stale paths that correspond to reviewed source deletions; preserve installer-generated, runtime, external-symlink, and other intentional unmanaged entries.
- Use `trash <exact-live-path>` for confirmed stale local files or directories. For a future managed removal, prefer `chezmoi remove <exact-live-target>` before deleting its source entry, then review the result.
- Verify the final state with `chezmoi diff --recursive <target>` and `chezmoi verify --recursive <target>`.

## Node and Global NPM

- Current canonical manager: `mise`.
- Do not restore Volta or Hermes Node as the active global manager unless explicitly requested.
- Keep `~/.local/bin` for local commands, but remove `node`, `npm`, and `npx` shims if they shadow mise.
- Manage global npm CLIs in `dot_config/mise/config.toml` with `npm:<package>`.
- Verify CLIs with a fresh interactive shell, not only the current agent shell.

## Packages

- Use `dot_brewfile.tmpl` for durable Homebrew formulae/casks/taps.
- Use `dot_config/mise/config.toml` for durable language runtimes and global CLI tools where mise supports them.
- Treat direct install commands as live-state changes. Ask for escalation when needed and reflect durable installs back into the managed config.
- Do not add a package manager just because a one-off command exists. Prefer the existing canonical manager for that tool class:
  - system/macOS packages: Homebrew/Brewfile
  - runtimes and global npm CLIs: mise
  - local project dependencies: project-native lockfiles, not global config
- Before removing a package, check whether it is referenced by Brewfile, mise config, shell PATH, aliases, or scripts.
- After package changes, verify both the package manager state and command resolution.

See `references/workflows.md` for exact commands and checks.
