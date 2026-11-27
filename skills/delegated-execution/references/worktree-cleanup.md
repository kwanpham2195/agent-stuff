# Worktree cleanup

Use this reference when reclaiming a managed worktree or other delegated-run resource. Cleanup is a separate operation for each path, and a terminal child status never authorizes deletion. Worktrees an app owns, such as a review tool's own worktrees, are not delegated-run resources; leave them to that app.

## Audit before planning

Collect an audit manifest for each candidate and retain its owner and source identity:

- worktree path, repository, branch, base and head refs;
- tracked and untracked Git status, saved patch or handoff artifact, and last known child or run state;
- active processes, pinned or ongoing chats, and any linked PR or review state;
- the proposed reason for retention or cleanup and the evidence timestamp.

In Pi, use the native cleanup planner with `subagent({ action: "worktree.cleanup", mode: "plan", repo: "..." })` when a managed handoff exists. Without a native planner, build the plan from the audit manifest alone and apply nothing without the approval below. Inspect `lane.status` and its emitted plan when the lane manifest supplies the candidate. The planner is plan-only in the current native API; it does not remove a worktree or branch.

## Apply only after approval

Ask for explicit approval before any destructive cleanup, after a fresh audit. One approval may cover a batch, such as "clean up all worktrees", when the request lists each repository and path with its audit result; it covers only the listed paths. Preserve resources when ownership, active use, process state, branch state, saved patch, or external result is unknown. Preserve any worktree with uncommitted or uncaptured work until its owner saves or transfers that work.

After approval, use the supported native cleanup workflow when it becomes available and revalidate the manifest, owner, active processes, Git status, saved patch, and current refs at apply time. Never infer deletion from a clean terminal status, a merged PR label, elapsed time, or a missing chat. Never issue broad `git worktree remove`, `rm`, reset, branch deletion, or simulator cleanup commands from this skill.

Report the audit manifest, candidates, the approval covering each path, retained resources and reasons, planner result, and any unavailable apply capability. A plan is not an applied cleanup. An unavailable capability is a blocker and gives no permission for a fallback.
