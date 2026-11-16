---
name: apple-reminders
description: "Manage Apple Reminders via remindctl when asked to add, list, edit, complete or organize personal reminders."
license: MIT
metadata:
  version: 1.0.0
  author: Hermes Agent
  platforms: [macos]
  hermes:
    tags: [Reminders, tasks, todo, macOS, Apple]
  prerequisites:
    commands: [remindctl]
---

# Apple Reminders

Use `remindctl` to manage Apple Reminders from the terminal. Reminders sync across Apple devices when their account and list use iCloud.

## Prerequisites

- macOS with Reminders.app and `remindctl`.
- To install, run: `brew install steipete/tap/remindctl`.
- Grant Reminders permission when prompted.
- Check permission with `remindctl status`; request it with `remindctl authorize` when needed for the user's task.
- Check `remindctl <command> --help` before relying on version-specific options.

## When to Use

- User requests Apple Reminders or personal to-dos with due dates that sync to iOS.
- Managing Apple Reminders lists.
- User wants tasks to appear on their iPhone or iPad.

## When NOT to Use

- Scheduled agent alerts: use the active harness's scheduler.
- Calendar events: use the requested calendar app.
- Project task management: use the project's configured tracker.
- If “remind me” could mean either an Apple reminder or an agent alert, clarify first.

## Quick Reference

### View Reminders

```bash
remindctl show today          # Today
remindctl show tomorrow       # Tomorrow
remindctl show week           # This week
remindctl show overdue        # Past due
remindctl show all            # Everything
remindctl show 2026-01-04      # Specific date
```

### Manage Lists

```bash
remindctl list                        # List all lists
remindctl list Work                   # Show specific list
remindctl list Projects --create      # Create list
remindctl list Work --delete          # Delete list
```

### Create Reminders

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

Examples use illustrative dates; resolve the user's actual date and timezone before creation.

### Due Time and Early Notifications

The due date and an early notification are distinct requirements. `--due` sets the due date/time. Do not move the due time earlier to imitate an early notification.

The installed version 0.1.1 does not advertise `--alarm` for `add` or `edit`. If the user requests an early nudge, report this limitation and check an authorized alternative. Do not install or upgrade tools solely because an option is unavailable.

On a version that explicitly supports `--alarm`, these examples set a 14:00 due time and a 13:30 notification:

```bash
remindctl add --title "Hairdresser" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
remindctl edit 87354 --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

Use JSON to verify the result rather than inferring due time from UI grouping. Inspect the actual version's output schema; do not assume it contains `alarmDate`. Where supported, `dueDate` represents the due time and `alarmDate` the notification time.

### Edit, Complete and Delete

```bash
remindctl edit 4A83 --due tomorrow
remindctl complete 1 2 3          # Complete by index or ID
remindctl delete 4A83 --force     # Delete by ID
```

Resolve IDs against fresh output before acting; list indexes can change.

### Output Formats

```bash
remindctl show today --json       # JSON for scripting
remindctl show today --plain      # Stable line-based output
remindctl show today --quiet      # Minimal output
```

## Date Formats

Accepted by `--due` and date filters:

- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601, for example `2026-01-04T12:34:56Z`

## Rules

1. When “remind me” is ambiguous, clarify Apple Reminders versus a scheduled agent alert.
2. Confirm reminder content and due date before creating; an explicit user request containing both supplies that confirmation.
3. Use `--json` for programmatic parsing and verify changes from fresh output.
