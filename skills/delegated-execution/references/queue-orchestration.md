# Queue orchestration

Use this reference when a parent coordinates a bounded inventory of work rather than one inline task. The parent owns the queue, frontier, acceptance decisions, and recovery. The harness's native launch path owns child launch and completion delivery: Pi workflow execution in Pi, and the `Agent` tool with its background completion notification in Claude Code (see [Claude Code routing](claude-code-routing.md)).

## Record one work entry per item

Before launch, record the approved inventory and these fields in the existing work entry:

- item identity, scope, acceptance criteria, dependencies, readiness, and blockers;
- owner, writer checkout or cwd, branch, base ref, and current head;
- attempt number, artifact or report reference, and reviewer identity;
- status, last inspected evidence, and the next permitted transition.

Do not create a second queue or hidden tracker when the existing entry can hold the state. An item is ready only when its dependencies are complete and its current source and acceptance evidence have been inspected. A dependency completion message is a pointer to inspect and is no proof that the item can advance.

## Launch and advance

1. Freeze the approved bounded inventory and identify one writer per cwd.
2. Compute a deterministic frontier from item dependencies and current inspected heads. Keep blocked, unknown, and stale items out of the ready set.
3. Launch ready children through the harness's native path. In Pi, use `workflowScript` calls with `runs.run` or `runs.all`. In Claude Code, use the `Agent` tool. Use stable keys and explicit labels. Do not nest a runner, invoke an external CLI, or make a child responsible for queue state.
4. Accept a completion event only after reading the child result, changed paths, acceptance evidence, and current head. Record the attempt and artifact before advancing a dependent item.
5. Invalidate readiness and prior verdicts when a base or head changes. Re-inspect the affected item and descendants before requeueing them.
6. Keep one writer per checkout and serialize writers on the shared cwd. Do not create worktrees; the experimental `agent-pickup` skill's lanes, when installed, are the only exception.

The harness's native completion notification is the wake mechanism: Pi completion notifications, or the background `Agent` completion notification in Claude Code. Do not wait or poll for a running child. A failed launch, workflow, extension, or tool setup is an infrastructure blocker. Preserve the item and report the exact failure. Never switch runners to get around a failed native path.

## Recovery and handoff

Use a finite retry policy tied to the failure class. Retry a transient infrastructure failure only through the same native path, reduce scope after a resource limit, and stop after the approved attempt bound. An unknown external write outcome is unreconciled. Do not continue the item or repeat the write until the owner reconciles its actual state.

At each checkpoint, record completed items, current frontier, invalidated evidence, attempts, artifacts, blockers, and the next authorized action. At close, reconcile every launched child to complete, failed, stopped, or abandoned and preserve the queue record for parent review. Queue metadata does not authorize commits, pushes, comments, merges, cleanup, or other remote writes.

An abandoned item does not establish that its process stopped. Keep its writer ownership and concurrency slot until the native runtime confirms termination or safe handoff; unknown state cannot release a checkout for another writer.
