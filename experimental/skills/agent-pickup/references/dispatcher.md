# Dispatcher

Read as the dispatcher thread `Dispatch: Agent-ready tasks`. Every wake arrives as a queued message, so turns never overlap. Start each turn from files and keep nothing important only in the conversation; T3 may compact this thread.

## Each turn

1. Read `runtime.md` and `lanes.md` in `~/.agents/context/workspaces/<workspace-id>/agent-pickup/`.
2. Reconcile lanes: for each lane with queued, active or held work, read its thread with `t3_thread_read` (status, last result) and the work states of its tasks. A lane is active while its thread is `running`, `queued`, `starting`, `preparing` or `waiting`, or a task it owns is `active`. A local-work hold also reserves its capacity and scope until the lane confirms release; an idle thread does not clear it. Reconcile hold, release and withdrawal messages under [held lanes](#held-lanes) before placement.
3. Find candidates: every `workspaces/*/work/*/agent/state.md` with `status: ready-for-agent`. Read designated frontmatter and `agent/packet.md` only. Skip archives.

   Project indexes supply reporting attention under [brief reporting](../../references/context-routing.md#brief-reporting-fields), never dispatch candidates. A project's status or its child's `project`/`parent` link does not satisfy packet approval or dependency checks.
4. Re-run the [entry check](packet.md#entry-check) for each candidate. A failure stays listed in `lanes.md` under "Not placed" with the reason; do not edit the work state.
5. Place each passing candidate (below), in order of the packet's Approval time.
6. On the nightly wake, also run the [sweep](#sweep).
7. Write `lanes.md`, commit it under [context commits](../../references/work-lifecycle.md#commit-local-context-changes), post a concise Markdown summary in this thread, and end the turn. Use three separate bullets with blank lines between them: **Sweep** (or not run), **Placement**, and **Ledger** (including any commit blocker). Link relevant PRs and tasks when known. Keep each bullet short and include the concrete result or next action; do not wrap the summary in a code block.

Spend at most 10 agent-minutes per turn. Launch nothing beyond the caps in `runtime.md`.

## Place a task

```text
if the task is deferred on, depends on, or overlaps a held lane
  leave it ready; "Waiting: lane held"
else if a dependency is not merged and is neither ready nor active in the same repository
  leave it ready; "Waiting on <dependency>"
else if a dependency or overlapping scope (shared files included) is in an existing lane of the same repository
  queue it on that lane
else if active lanes < cap for the current hour and the start window is open
  launch a new lane
else
  leave it ready; "Waiting: capacity" or "Waiting: start window"
```

Write the lane entry, or the queued task, to `lanes.md` before the T3 call. Then:

- **Launch:** `t3_thread_launch` with the profile's `projectId`, title `Implement [#key]: <task subject>`, `workspaceStrategy: {type: "worktree", baseRef: <profile base without "origin/">, branch: <packet branch>, startFromOrigin: true}`, `modelSelection` from the profile's lane model, `runtimeMode: "full-access"`, and the lane brief below as `message`. For a task stacked on another lane's branch, the task joins that lane instead. Record the returned `threadId`. If the call errors or its response is lost, check `t3_thread_list` for the title before launching again; `t3_thread_launch` has no retry key.
- **Queue:** `t3_thread_send` to the lane thread, mode `queue`, `clientRequestId` `pickup-<workspace>-<work-id>-<n>`, with the same brief for the new task.
- **Lane thread gone** (deleted or archived) while its worktree remains: launch a new lane with `workspaceStrategy: {type: "existing_worktree", worktreePath, branch}` from `t3_worktree_list`.

Lane brief:

```text
You are an agent-pickup lane. Read <absolute path to agent-pickup SKILL.md>, then references/lane.md and references/packet.md.
Task: <work state absolute path>; packet: <packet absolute path> (sha256 <hash>).
Profile: <workspace index absolute path>#agent-pickup, repository <identity>.
Base: <base>; branch: <branch>; stacked on: <parent branch or none>.
Dispatcher thread: t3-thread://v1/<dispatcher thread id>. Report results in this thread; notify the dispatcher of lane holds, releases and withdrawals per lane.md, and send "lane free" only when its conditions hold.
```

## Held lanes

Record `lane held` notifications in `lanes.md`, with the holding task, recovery ask and deferred work. Reconcile against the lane checkpoint even if its notification failed. Stop queueing work on that lane. List unstarted tasks as `Waiting: lane held`; retain deferred follow-ups with their original source and approval. Do not send automatic repair or closeout messages while the hold remains.

On `task withdrawn`, remove the task from the executable queue. Keep a separate recovery entry pointing to its `draft` state while a local-work hold remains. This entry is not an active task or a state contradiction. Drop it only after the lane confirms recovery. Withdrawal alone never frees the lane.

On `lane released`, verify the lane checkpoint records clean local work and its resolution. Reconcile each deferred message against current state and thread activity before re-sending it. Re-run the entry check for unstarted tasks; for follow-ups, retain their original authority and require the user's decision for any unresolved stop. Skip withdrawn, completed or already active work. Re-send eligible briefs in their original order with new request IDs recorded before sending; do not replay uncertain deliveries without reconciliation. Track each original message and its replacement delivery, and remove its deferred marker only after the lane records it started or handled. Keep ineligible work listed with its reason and exclude already queued deliveries from normal placement. The lane waits for these messages rather than independently replaying its checkpoint.

## Sweep

On the nightly wake only:

- Pick up hand-edited `ready-for-agent` states and tasks waiting for the night window; place them as above.
- For each open agent PR (from lane work states in `needs-review`), read reviews, threads and mergeability with the profile's read-only forge commands. When it finds the user's "request changes" review, an unresolved thread the user started, or a conflict with the base, send the owning lane a follow-up with `t3_thread_send` naming the PR and what to address. Teammate and bot comments are evidence for the lane, not triggers.
- If the work state records an unresolved agreed stop condition, list it as awaiting the user's decision and send no automatic repair follow-up. The lane owns reconciliation of a scoped resume or withdrawal decision; a base conflict never overrides the stop.
- For each merged agent PR whose task is not `complete`, record the merge. If a stop decision or local-work hold remains, list it as awaiting resolution and send no automatic closeout. Otherwise send the owning lane a closeout message, excluding withdrawn tasks.
- Clear `lanes.md` entries whose tasks are all complete or explicitly withdrawn, whose threads are idle, and which have no held or deferred work. Preserve recovery entries until the lane confirms release.

## Failures

- Launch or send failure: record the exact error in `lanes.md`, leave the task `ready-for-agent`, and do not retry through another path.
- Unknown launch result: reconcile with `t3_thread_list` before any new launch.
- Missing or unreadable state, packet or profile: list the task under "Not placed" with the reason.

## Schedules

`runtime.md` records both schedules. Change them only when the user asks.

- `Dispatch: Agent-ready tasks`: bound to this thread (`bindToCurrentThread: true`), `fixed_time` the user's chosen night time, daily. Prompt: "Agent pickup wake (scheduled nightly): run a dispatcher turn including the sweep, per the agent-pickup skill."
- `Report: Agent results`: fresh thread per run (`bindToCurrentThread: false`), `fixed_time` the user's chosen morning time on weekdays, following [digest](digest.md).
