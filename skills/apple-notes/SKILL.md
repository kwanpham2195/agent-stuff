---
name: apple-notes
description: "Manage Apple Notes via memo CLI when asked to create, view, search, edit, organize or export notes."
license: MIT
metadata:
  version: 1.0.1
  author: Hermes Agent
  platforms: [macos]
  hermes:
    tags: [Notes, Apple, macOS, note-taking]
    related_skills: [obsidian-cli]
  prerequisites:
    commands: [memo]
---

# Apple Notes

Use `memo` to manage Apple Notes directly from the terminal. Notes sync across Apple devices when the account and folder use iCloud.

## Prerequisites

- macOS with Notes.app and `memo`.
- To install, run: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`.
- Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation).
- Check `memo notes --help` before use; installed versions may differ.

## When to Use

- User asks to create, view, or search Apple Notes.
- Saving information to Notes.app for access across devices.
- Organizing notes into folders.
- Exporting notes to Markdown/HTML.

## When NOT to Use

- Obsidian vault management: use obsidian-cli or obsidian-markdown.
- Bear Notes: not supported here.
- Agent-internal memory: use agent-memory-repo within its authorized scope.

## Quick Reference

### View Notes

```bash
memo notes                        # List all notes
memo notes -f "Folder Name"       # Filter by folder
memo notes -s                     # Interactive fuzzy search
memo notes -fl                    # List folders and subfolders
```

The installed `-s`/`--search` option is a bare flag; enter the query at its prompt.

### Create Notes

```bash
memo notes -a                     # Add a note (opens your $EDITOR)
memo notes -a -f "Folder Name"    # Add a note into a specific folder
```

`-a`/`--add` is a bare flag. It opens `$EDITOR` to compose the note and does not take a title argument. Use `-f`/`--folder` to target a folder. Set `$EDITOR` first, for example `export EDITOR=vim`.

### Edit Notes

```bash
memo notes -e                     # Interactive selection to edit
```

### Delete Notes

```bash
memo notes -d                     # Interactive selection to delete
```

### Move Notes

```bash
memo notes -m                     # Move note to folder (interactive)
```

### Export Notes

```bash
memo notes -ex                    # Export to Desktop; follow format prompts
```

## Limitations

- Cannot edit notes containing images or attachments.
- Interactive prompts and editors require a real terminal. Use terminal-control for those interactions.
- macOS only; requires Apple Notes.app.

## Rules

1. Prefer Apple Notes when the user wants iCloud sync across iPhone, iPad and Mac.
2. Use agent-memory-repo for agent-internal memory within its registered scope.
3. Use the Obsidian skills for Markdown-native knowledge management.
