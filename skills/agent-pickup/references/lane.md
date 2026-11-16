# Lane

Read as a lane thread. You own the work states of your tasks from `active` on, your worktree and your branches. The user is usually away: never ask a question in the thread and never wait for an answer.

## Before the first task

1. Run `t3_worktree_status`. Confirm the worktree path and branch match the brief. Never create another worktree.
2. Read the repository's `AGENTS.md` and `CONTRIBUTING.md`, the profile, and the skills they name. Repository rules win over this file where they are stricter.
3. Check `git config user.email` against the profile. A mismatch blocks the lane: set every queued task `blocked` with a dependency ask naming the email, and stop.
4. Run the profile's setup. Copy only the ignored files the profile names, from the main checkout, without printing their contents.

## Each task

1. Re-read the work state and packet. Check for a [held lane](#held-lane) before taking another task. Check the packet hash against the brief. A changed packet without a matching fresh approval blocks the task. Read agreed stop conditions in the packet's linked acceptance, plan, issue or design at their recorded hashes. A missing or mismatched required source hash blocks execution under the packet entry check; report the source needing approval rather than treating its current content as approved. If verified sources state no stop condition, continue.
2. Set `status: active`, `owner_thread` to this thread, `next_action`, `brief_attention: []` and `brief_checked_at`; commit the context change.
3. Put the task on its own branch. The lane's first task uses the branch T3 created. A stacked task branches from its parent task's branch. Any other later task runs `git fetch origin` and `git switch -c <branch> origin/<profile base>` after the previous task's branch is pushed or committed.
4. Implement within the packet's scope. Apply [coding-standards](../../coding-standards/SKILL.md) and [write-discoverable-code](../../write-discoverable-code/SKILL.md). For an outline with phases, follow RPI's [implement process](../../rpi/references/implement-outline/process.md) and [RPI local rules](../../references/rpi-local.md#subagents-and-models), running all phases continuously: verify between phases and leave manual checks pending for the user's final review instead of pausing.
5. Run the profile's checks. At most 2 fix rounds. After each commit, measure size per [size limit](packet.md#size-limit); stop at 1000 changed lines.
6. Run the live verification the packet requires, following the profile and the repository's verification skill. Keep evidence outside the repository, under the task's `evidence/` folder.
7. Delegate one review with `delegate_task` (role `review`, the profile's review model, a stable `clientRequestId`, `mode: "async"`) using [code-review](../../code-review/SKILL.md) with the packet's acceptance as the spec. End the turn; the completion wakes you. Fix accepted findings once and rerun the affected checks.
8. Commit with the [commit](../../commit/SKILL.md) skill and the repository's hooks. Push the branch without force, using the profile's account.
9. Open the PR with the profile's command and the [write-pr](../../write-pr/SKILL.md) standards: link the source ticket, state the checks and live evidence actually run, and list anything not verified. Then `link_pull_request` and `write_pull_request_guides`. If the repository runs PR checks, `watch_pull_request`, allow one fix round or one rerun, then `unwatch_pull_request`; otherwise skip the watch.
10. Set `status: needs-review` with a `brief_attention` decision ask `Review PR #<n>` whose source is the PR URL, and post the result in this thread (format below).
11. If the task failed, skip queued tasks that depend on it and report them as skipped.

Spend at most the packet's budget (default 90 agent-minutes) per task. When it runs out, stop as partial.

If evidence shows an agreed outcome stop condition holds at any point, stop that task and skip its remaining implementation, push and PR steps. Budget, fix-round and size limits retain their existing Partial handling; an outcome stop condition takes precedence if both apply. Report the evidence as `Stopped` in `needs-review`, asking the user to resume with a scoped follow-up or withdraw. Record the condition and unresolved decision in the work state, and skip dependent queued tasks. Do not infer completion or resume without that decision.

Preserve local work and record its branch, revision and dirty paths in the checkpoint. Save a recoverable patch and task-owned untracked files in the task's evidence folder under existing privacy rules, since worktree retention is not guaranteed. Verify the saved recovery material before handoff. Do not force a commit of unverified work, stash, discard files or carry them into another task. If the worktree remains dirty, follow the held-lane procedure below. A later decision must resolve local work before branch changes; preserve the lane's ownership meanwhile.

## Held lane

Record the hold and every deferred task or follow-up in the holding task's checkpoint, including its source message and packet hash. Report them in the Stopped result. Send `lane held: <repository>, <holding task>, <deferred work>` to the dispatcher with `t3_thread_send`, mode `queue`, and a stable `clientRequestId`. End the turn without starting queued work or reporting the lane free.

While held, record later task and follow-up messages as deferred, notify the dispatcher, and end the turn. Leave unstarted tasks `ready-for-agent`. Process only the user's scoped decision or recovery instructions for the holding task, or record a verified merge without closing out. A withdrawal does not clear a local-work hold.

After authorized recovery, verify the worktree is clean and record how local work was resolved. Send `lane released: <repository>, <holding task>, <deferred work>` to the dispatcher using the same transport and a new stable request ID. Wait for the dispatcher to re-send eligible deferred work; do not also start it locally. On receipt, re-read its state and approval. Track each original task or follow-up message as pending, started or handled in the checkpoint; skip a duplicate message already started or handled. Mark withdrawn deferred work handled without executing it. Releasing a local-work hold does not resolve an outcome stop decision.

## Results

| Result | Push and PR | Work status | Ask |
| --- | --- | --- | --- |
| Ready | Branch pushed, PR open, checks and live verification pass | `needs-review` | decision: review the PR |
| Needs attention | PR open, a review finding unresolved | `needs-review` | decision: the named problem |
| Partial | Branch pushed, no PR | `needs-review` | decision: accept partial or change scope |
| Blocked | Nothing pushed | `blocked` | dependency: the missing answer or access |
| Stopped | No further push or PR; report any existing PR | `needs-review` | decision: resume with a scoped follow-up or withdraw |

Post each result in this thread:

```text
<Result>: <task title>
PR: <url or "none">  Branch: <branch>  Size: <actual> lines (estimate <n>)
Checks: <commands and outcomes>
Live: <what ran and its evidence path, or "not required">
Review: <findings fixed, dismissed with reasons, or open>
Read first: <the most important changed locations or evidence links>
Not proven: <material limits of the evidence, or "none beyond the scope stated above">
Decided for you: <defaults, exclusions or interpretations within granted scope worth checking, or "none">
Needs you: <decision or "nothing">
```

## Follow-ups and closeout

A follow-up message (from the dispatcher sweep or a mover's "back to agent") names the PR or stopped result and what to address. Check for a held lane before switching tasks or branches. Before acting, check for an unresolved stop decision in the work state. A sweep message or base conflict cannot resolve it; report still Stopped and end the turn. Resume only when the user's scoped decision addresses the condition, and revalidate approval hashes when the decision changes approved content. If the user withdraws, the lane records the user's decision, sets the task to `draft`, clears only the resolved stop ask, and preserves recovery evidence. If local work still holds the lane, retain a dependency ask for its disposition. Notify the dispatcher with `task withdrawn: <task>, <hold remains or released>` using `t3_thread_send`, mode `queue`, and a stable request ID. Withdrawal grants no cleanup or PR closure permission.

For an authorized follow-up, append it to the packet's Follow-ups section, set the task `active`, fix it on the same branch, rerun checks and live verification as affected, request one review round, push, and report again. Resolve a base conflict by merging the base into the branch; never rebase a pushed branch. Classify teammate and bot comments with the [pr maintenance](../../pr/references/maintenance.md) rules (fix with proof, dismiss with a reason, or ask) and list the asks in your result. Never reply to or resolve other people's threads.

A closeout message means the user merged the PR. Verify and record the merge on the forge. If an outcome stop decision or local-work hold remains unresolved, preserve its ask and report still Stopped; a merge alone does not resolve it. A withdrawn task stays `draft`. Otherwise set the task `complete` with empty `next_action`, `blocker` and `brief_attention`, run the [closeout memory step](../../references/work-lifecycle.md#preserve-reusable-project-knowledge), and set any source local issue to `done`. After the user resolves a stop or hold on an already merged task, re-evaluate closeout using the recorded decision and a fresh merge check.

When your queue is empty and no local-work hold or deferred work remains, send `t3_thread_send` to the dispatcher thread: `lane free: <repository>, <tasks finished>`, mode `queue`, `clientRequestId` `lane-free-<thread id>-<n>`. Then end the turn.
