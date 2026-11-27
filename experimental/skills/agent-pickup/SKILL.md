---
name: agent-pickup
description: "Run planned tasks unattended in T3 Code once their work state reaches ready-for-agent: packets, the dispatcher thread, lane threads in worktrees, results and follow-ups. Use when the user says \"ready for agent\" or \"back to agent\", or when acting as the dispatcher, a lane or the results digest."
---

# Agent pickup

A task whose work state reaches `status: ready-for-agent` is implemented without the user present. One long-lived dispatcher thread places ready tasks into lanes. Each lane is a top-level T3 thread with its own worktree that implements tasks in order, verifies them, gets one review, pushes its branch and opens a PR without reviewers. Night is the common case; nothing depends on it.

This skill runs only in T3 Code. Confirm the session under [confirm the current session](../delegated-execution/references/t3-routing.md#confirm-the-current-session). Outside T3, tell the user agent pickup runs only in T3 and stop.

## Find your role

| You are | Read |
| --- | --- |
| A planning thread or the Desk, and the user says "ready for agent" | [packet](references/packet.md) |
| The dispatcher thread, woken by a message or the nightly schedule | [dispatcher](references/dispatcher.md) |
| A lane thread | [lane](references/lane.md), then [packet](references/packet.md#grants) for your authority |
| The scheduled results digest | [digest](references/digest.md) |

Runtime records live in `~/.agents/context/workspaces/<workspace-id>/agent-pickup/`: `runtime.md` (dispatcher thread and schedule IDs, caps) and `lanes.md` (the lane ledger, written only by the dispatcher).

## The state

`ready-for-agent` is a value of the work state's `status`, between `draft` and `active` ([work metadata](../references/context-routing.md#work-metadata-and-overview)). The status is a signal; the authority is the task packet's recorded approval. A task may hold the status only while `agent/packet.md` records the user's approval for the packet's current content hash. A card dragged into the column by hand starts nothing until the nightly sweep, which runs the entry check and skips a packet without that approval.

```text
draft -> ready-for-agent        packet approved, entry check passes (mover)
ready-for-agent -> active       lane takes the task (lane)
active -> needs-review          PR open, partial or stopped result (lane)
active -> blocked               question or missing access (lane)
needs-review -> active          authorized follow-up; unresolved stops require the user's decision (lane)
needs-review -> draft           the user withdraws a stopped task (lane)
blocked -> ready-for-agent      the user answers, entry check passes again (mover)
needs-review -> complete        the user merged; no unresolved stop or local-work hold (lane)
ready-for-agent -> draft        the user withdraws the task (mover)
```

Each record keeps one writer. Movers write the work state only to enter or leave `ready-for-agent`. The lane owns the work state from `active` on. The dispatcher writes only its own runtime files.

## Worktree exception

This is the only exception to the rule against creating worktrees:

> Exception for agent-pickup lanes. The agent-pickup dispatcher creates one worktree per lane, only through `t3_thread_launch` with `workspaceStrategy` type `worktree`, for a T3 project whose root is the lane's repository, for tasks that passed the entry check. A lane may create stacked branches inside its own worktree. A later run on that lane reuses the worktree with type `existing_worktree`. Nothing else creates worktrees: not lane threads, not subagents (`delegate_task` `isolation: "worktree"`), not shell `git worktree add`, not Claude Code `isolation`. T3 removes lane worktrees under its cleanup settings; agents never delete them.

## Stop rules for every role

- Never wait by sleeping, polling or shell watchers. End the turn; wakes, child completions and the schedule start the next one.
- Never ask a question during a run. An unclear requirement or missing access sets `blocked` with the question as a `brief_attention` ask; independent work continues.
- Never use a credential the repository profile does not name, print a credential, ask for a secret, change global git or `gh` config, or run `gh auth switch`. Select the `gh` account per command with `GH_TOKEN="$(gh auth token --user <account>)"`.
- Never merge, request reviewers, mark a draft ready, close a PR, force push, push outside the lane's branches, rewrite published history, edit trackers, deploy, or touch production or shared systems.
- An external write with an unknown result (push, PR creation, thread launch, sandbox write) is reconciled against its target before any retry. Never repeat a write blindly.
- A failed launch, worktree setup or tool is an infrastructure blocker. Record the exact error. Never switch runner, harness or model to get around it.

The user stops the system by disabling the dispatch schedule (`update_scheduled_task enabled: false`), stopping a lane thread in T3, or moving a task back to `draft`.
