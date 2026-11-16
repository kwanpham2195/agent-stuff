# Claude Code routing

Read when delegating, resuming, or reporting from Claude Code. [Delegated execution](../SKILL.md) and [model policy](model-policy.md) own role, permissions, budget, models, and concurrency. The live tool schemas own supported arguments and runtime behavior. This reference grants no launches, new source access, model changes, extra concurrency, or human-gate bypass.

## Confirm the current session

The Claude Code system prompt identifies the harness. `ListAgents` lists the sessions and agents this session can message, each row led by its name. Use that list to confirm a recipient's name before sending. A name seen elsewhere does not establish that the recipient is reachable.

## Launch and continue children

Use the `Agent` tool for a child helper. For a read-only explorer that locates code, use the `Explore` type. When the child must read files in full, review, or audit, use `general-purpose`. Resolve `direct.claude` for the assigned role immediately before launch under [resolver usage](model-policy-configuration.md), with verified native model/effort and inheritance evidence. Copy emitted `model` and `effort`, set `subagent_type`, and retain source/key and hashes. Compare exposed returned settings; missing metadata means requested but unverified. Set `run_in_background` for work that should not block the turn. Do not use `isolation: "worktree"` or `EnterWorktree`, because worktrees are not allowed in any harness.

Continue a child with `SendMessage` to its id or name. Stop it with `TaskStop` when stopping is authorized. A stop request does not release the child's capacity until the child is confirmed stopped.

A task owner in a separate conversation is a separate Claude Code session that the user starts. No tool launches a new local session, so do not simulate one.

## Completion

A background `Agent` completion notification wakes the parent. End the turn when waiting instead of polling. Read the child's result, changed paths, and verification evidence before acceptance. A completion notification does not signal parent acceptance.

## Messages to another session

Task threads talk to the user in their own conversation; they do not report to other sessions. When a helper must reach its parent session, or the user asks you to message one, use `SendMessage` with the name shown by `ListAgents`. Delivery means the message reached that session, not that it was read. `SendMessage` has no idempotency key, so check the recipient or its checkpoint file before resending.

To learn when another session finishes, use `SendMessage` with `notify_when_idle: true`. This works from the main conversation only and fires once.

No tool reads another session's history. Ask the session for a report, or read its checkpoint file.

## Schedules, monitoring, and alerts

`CronCreate` schedules a recurring prompt for this session only. The job ends when the session exits, and recurring jobs expire after 7 days. For durable schedules, use cloud routines through `RemoteTrigger` or the `schedule` skill. Cloud sessions cannot message local sessions back. Create a schedule only when the user or assignment authorizes it.

`Monitor` watches a process or pull request with a polling command. Each arm lasts at most 30 minutes, so re-arm it on expiry. `PushNotification` alerts the user when away, only when an authorized reporting route calls for it.

## Permission boundary

Permissions apply per session. Never ask a peer session to do something that this session's own permissions would block.
