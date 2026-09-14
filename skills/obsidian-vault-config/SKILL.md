---
name: obsidian-vault-config
description: Manage the shared Obsidian config at ~/.obsidian-shared that every vault symlinks into. Use when onboarding a new Obsidian vault, installing or removing a plugin or theme across vaults, changing appearance/hotkeys/core-plugin settings, or when a vault's settings stopped syncing with the others.
---

# Shared Obsidian vault config

All of the user's Obsidian vaults share one config directory. Each vault's
`.obsidian/` contains symlinks into `~/.obsidian-shared`, so a plugin installed
or a setting changed in any vault lands in all of them.

Never hand-copy `.obsidian` contents between vaults, and never edit a vault's
`.obsidian/` expecting it to stay local — that silently forks the config.
Everything goes through the bundled script, `scripts/obsidian-link` next to this
file. It is on the user's PATH as `obsidian-link` via a `~/bin` symlink; if that
symlink is missing, invoke it by its path in this skill directory or restore it:

```bash
ln -sfn ~/.claude/skills/obsidian-vault-config/scripts/obsidian-link ~/bin/obsidian-link
```

The script is the source of truth and lives with this skill; `~/.obsidian-shared`
holds only the config *data* it links.

## What is shared and what is not

Shared (symlinked into every vault):

| Entry | Notes |
|---|---|
| `plugins/` | directory link — safe, Obsidian never replaces the dir itself |
| `themes/` | directory link |
| `snippets/` | directory link |
| `app.json` | editor prefs (vim mode, line numbers, view mode) |
| `appearance.json` | fonts, theme |
| `hotkeys.json` | |
| `core-plugins.json` | |
| `community-plugins.json` | which community plugins are **enabled** — global |

Per-vault, deliberately left alone: `workspace.json` (open panes/tabs),
`graph.json`, `templates.json` (holds a vault-relative folder path), and any
other file already in that vault's `.obsidian/`.

Because `plugins/` is shared, each plugin's `data.json` is shared too — plugin
settings are global. That is the intent; only break it if the user asks.

## The commands

```bash
obsidian-link <vault> [more vaults...]  # link or re-link; creates .obsidian if absent
obsidian-link --relink-all              # re-link every registered vault
obsidian-link --check                   # report link health, changes nothing
obsidian-link --list                    # registered vaults (~/.obsidian-shared/vaults.txt)
obsidian-link --init                    # create an empty shared config (new machine)
```

The shared config location defaults to `~/.obsidian-shared` and can be overridden
with `$OBSIDIAN_SHARED` — useful for testing against a throwaway directory before
touching the real one.

Linking is idempotent — re-running prints `ok` per entry and touches nothing.
Anything displaced is moved to `~/.obsidian-shared/backups/<vault>-<timestamp>/`,
never deleted.

## Obsidian must be closed

The script refuses to link while Obsidian is running, because Obsidian rewrites
its config on exit and would overwrite fresh symlinks with real files. Ask the
user to quit it and wait — do not reach for `--force`, which exists only for the
user's own deliberate override.

`--check` and `--list` are read-only and safe at any time.

## Common tasks

**New vault.** `obsidian-link ~/path/to/vault`. It opens with every shared plugin,
theme, hotkey and setting already active. No other step.

**Add a plugin or theme for everyone.** Install it from inside any linked vault the
normal way — it writes straight into `~/.obsidian-shared/plugins`, so every vault
has it. Then add its id to `~/.obsidian-shared/community-plugins.json` if Obsidian
did not (that file is the enabled list).

**Remove one.** Deleting it in one vault deletes it everywhere. Confirm the user
means all vaults before doing it.

**A plugin present but disabled in one vault.** Not possible while
`community-plugins.json` is shared. That vault needs its own real copy of the
file — replace the symlink with a copy and note it will no longer track the
others.

## Troubleshooting: "settings stopped syncing"

Run `obsidian-link --check`. A `DETACHED` entry means Obsidian replaced that
symlink with a real file — that vault has forked for that setting. Fix:

1. Check whether the detached file holds changes worth keeping; if so, copy them
   into `~/.obsidian-shared/<file>` first.
2. Quit Obsidian.
3. `obsidian-link --relink-all` (the detached copy is backed up, not discarded).

A recurring detach on the same file is the known Obsidian-version-dependent
failure mode — if it keeps coming back, the fallback is to stop sharing that one
file and leave it per-vault, rather than fighting it.

## New machine

`obsidian-link --init` creates an empty `~/.obsidian-shared` skeleton
(`plugins/ themes/ snippets/ backups/` plus the registry). Populate it by copying
the richest existing vault's `.obsidian` contents into it — plugins, themes and
the settings JSONs listed above, but *not* `workspace.json`/`graph.json`/
`templates.json` — then link the vaults. Entries absent from the shared config
are simply skipped when linking, so a partial shared config is fine.

## Gotchas

- Keep `~/.obsidian-shared` **outside** every vault. A parent directory can be
  a vault that contains nested vaults, so a shared directory placed inside it
  would get indexed or refer to itself.
- Never symlink the whole `.obsidian` folder — `workspace.json` is genuinely
  per-vault and thrashes when two vaults are open at once.
- Two vaults open simultaneously: a settings change is last-write-wins on the
  shared JSONs. Harmless in practice, worth knowing when a change seems to revert.
