#!/usr/bin/env python3
"""Count skill loads, subagent models and delegate model/effort in one Claude Code session log.

Counts unique tool_use IDs, so repeated log entries are not double counted.
Usage: session-usage.py <session.jsonl>
"""

from __future__ import annotations

import collections
import json
import sys


def main(path: str) -> None:
    seen: set[str] = set()
    skills: collections.Counter = collections.Counter()
    agents: collections.Counter = collections.Counter()
    delegates: collections.Counter = collections.Counter()
    for line in open(path, encoding="utf-8"):
        entry = json.loads(line)
        if entry.get("type") != "assistant":
            continue
        for item in entry.get("message", {}).get("content") or []:
            if not isinstance(item, dict) or item.get("type") != "tool_use" or item["id"] in seen:
                continue
            seen.add(item["id"])
            name, args = item["name"], item.get("input") or {}
            if name == "Skill":
                skills[args.get("skill")] += 1
            elif name == "Agent":
                agents[args.get("model") or f"default ({args.get('subagent_type', 'general-purpose')})"] += 1
            elif name.endswith("delegate_task"):
                target = args.get("target") or {}
                options = target.get("options") or {}
                effort = options.get("reasoningEffort") or options.get("reasoning_effort") or options.get("effort") or "default"
                delegates[(target.get("model"), effort)] += 1
    print(f"unique tool calls: {len(seen)}")
    print("skill loads:", dict(skills.most_common()))
    print("native subagents:", dict(agents.most_common()))
    print("delegates (model, effort):")
    for (model, effort), n in delegates.most_common():
        print(f"  {n:4d}  {model}  {effort}")


if __name__ == "__main__":
    main(sys.argv[1])
