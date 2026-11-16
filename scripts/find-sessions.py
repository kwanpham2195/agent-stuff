#!/usr/bin/env python3
"""List saved agent sessions for a workspace's directories across harnesses.

Reads session metadata only (id, directory, title, last activity, model) from
Claude Code, Codex, Pi and OpenCode. T3 Code threads are not covered; search
them through the T3 MCP tools. Transcript text is never printed.
"""

import argparse
from datetime import datetime, timezone
import itertools
import json
from pathlib import Path
import re
import sqlite3
import sys

HOME = Path.home()
CONTEXT = HOME / ".agents/context"
HEAD_LINES = 400
TITLE_LIMIT = 100


def workspace_directories(workspace, context=CONTEXT):
    """Read explicit singular registrations and plural lists, in source order.

    Associated targets and other backticked paths do not register directories.
    """
    index = context / "workspaces" / workspace / "index.md"
    text = index.read_text(encoding="utf-8")
    directories = []
    list_indent = None
    for line in text.splitlines():
        registration = re.fullmatch(
            r"([ \t]*)(?:- )?Registered (directory|directories):[ \t]*(.*)", line)
        if registration:
            directories.extend(re.findall(r"`(/[^`]+)`", registration[3]))
            list_indent = len(registration[1]) if registration[2] == "directories" else None
        elif list_indent is not None:
            if not line.strip():
                continue
            item = re.fullmatch(r"([ \t]+)-[ \t]+(.*)", line)
            if item and len(item[1]) > list_indent:
                directories.extend(re.findall(r"`(/[^`]+)`", item[2]))
            else:
                list_indent = None
    return list(dict.fromkeys(directories))


def inside(cwd, directories):
    return any(cwd == d or cwd.startswith(d.rstrip("/") + "/") for d in directories)


def clip(text):
    text = " ".join((text or "").split())
    return text[:TITLE_LIMIT]


def iso_from_ms(value):
    return datetime.fromtimestamp(value / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


def iso_from_mtime(path):
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M")


def first_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") in ("text", "input_text"):
                return part.get("text", "")
    return ""


def head(path):
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in itertools.islice(stream, HEAD_LINES):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict):
                yield entry


def claude_sessions(directories):
    root = HOME / ".claude/projects"
    for path in root.glob("*/*.jsonl"):
        cwd = title = prompt = branch = None
        for entry in head(path):
            cwd = cwd or entry.get("cwd")
            branch = branch or entry.get("gitBranch")
            if entry.get("type") == "ai-title":
                title = entry.get("aiTitle")
            if entry.get("type") == "user" and not prompt:
                prompt = first_text(entry.get("message", {}).get("content"))
        if cwd and inside(cwd, directories):
            yield dict(harness="claude", id=path.stem, cwd=cwd, last=iso_from_mtime(path),
                       title=clip(title or prompt), model="", ref=str(path), branch=branch or "")


def codex_sessions(directories, subagents=False):
    database = HOME / ".codex/state_5.sqlite"
    if not database.exists():
        return
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    rows = connection.execute(
        "SELECT id, cwd, COALESCE(name, title), first_user_message, updated_at_ms, model, rollout_path,"
        " git_branch, archived FROM threads"
        + ("" if subagents else
           " WHERE COALESCE(thread_source, '') NOT IN ('subagent', 'guardian_review')"
           " AND id NOT IN (SELECT child_thread_id FROM thread_spawn_edges)"
           " AND first_user_message NOT LIKE 'Act as the % sub-agent%'"))
    for sid, cwd, title, prompt, updated, model, rollout, branch, archived in rows:
        if inside(cwd, directories):
            yield dict(harness="codex", id=sid, cwd=cwd, last=iso_from_ms(updated or 0),
                       title=clip(title or prompt), model=model or "", ref=rollout,
                       branch=branch or "", archived=bool(archived))
    connection.close()


def pi_sessions(directories):
    for path in (HOME / ".pi/agent/sessions").glob("*/*.jsonl"):
        cwd = prompt = model = None
        for entry in head(path):
            if entry.get("type") == "session":
                cwd = entry.get("cwd")
            elif entry.get("type") == "model_change":
                model = entry.get("modelId")
            elif entry.get("type") == "message" and not prompt:
                message = entry.get("message", {})
                if message.get("role") == "user":
                    prompt = first_text(message.get("content"))
        if cwd and inside(cwd, directories):
            yield dict(harness="pi", id=path.stem.split("_", 1)[-1], cwd=cwd,
                       last=iso_from_mtime(path), title=clip(prompt), model=model or "",
                       ref=str(path), branch="")


def opencode_sessions(directories):
    database = HOME / ".local/share/opencode/opencode.db"
    if not database.exists():
        return
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    rows = connection.execute(
        "SELECT id, directory, title, time_updated, model, time_archived FROM session"
        " WHERE parent_id IS NULL")
    for sid, cwd, title, updated, model, archived in rows:
        if inside(cwd, directories):
            yield dict(harness="opencode", id=sid, cwd=cwd, last=iso_from_ms(updated or 0),
                       title=clip(title), model=str(model or ""), ref=str(database),
                       branch="", archived=bool(archived))
    connection.close()


def find(directories, since=None, subagents=False):
    found = []
    sources = (claude_sessions, lambda d: codex_sessions(d, subagents), pi_sessions, opencode_sessions)
    for source in sources:
        try:
            found.extend(source(directories))
        except (OSError, sqlite3.Error) as error:
            print(f"warning: {error}", file=sys.stderr)
    if since:
        found = [s for s in found if s["last"] >= since]
    return sorted(found, key=lambda s: s["last"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", help="workspace id; reads its registered directories")
    parser.add_argument("--dir", action="append", default=[], help="extra directory (repeatable)")
    parser.add_argument("--since", help="only sessions active on or after YYYY-MM-DD")
    parser.add_argument("--subagents", action="store_true", help="include Codex subagent threads")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    directories = list(args.dir)
    if args.workspace:
        directories += workspace_directories(args.workspace)
    if not directories:
        parser.error("give --workspace or --dir")
    sessions = find(directories, args.since, args.subagents)[: args.limit]
    if args.json:
        print(json.dumps(sessions, indent=2))
        return
    for s in sessions:
        print(f"{s['last']}  {s['harness']:<8} {s['id'][:13]:<13} {s['model'][:18]:<18} {s['title']}")
        print(f"    {s['cwd']}" + (f"  [{s['branch']}]" if s["branch"] else ""))


if __name__ == "__main__":
    main()
