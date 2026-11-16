# Results digest

Read as the scheduled `Report: Agent results` run. It is read-only except for its own report files. Send no messages, launch nothing, use no subagents; 15 agent-minutes.

## Inputs

- `runtime.md` and `lanes.md` in `~/.agents/context/workspaces/<workspace-id>/agent-pickup/`, and the previous digest in `~/.agents/context/workspaces/<workspace-id>/reports/agent-results/`.
- `list_scheduled_tasks` for the dispatch schedule's last run status. It exposes no run time, which is not a gap. Take the sweep date from the newest `PR sweep (<date>` line in `lanes.md`; last night's date means the sweep ran.
- Each lane thread in `lanes.md`, with `t3_thread_read`.
- Work states and packets of every task in `lanes.md`, plus any `workspaces/*/work/*/agent/state.md` whose frontmatter has `status: ready-for-agent`.
- For those tasks' context projects, designated frontmatter from `workspaces/<ws>/projects/<project-id>/index.md`, using [brief reporting](../../references/context-routing.md#brief-reporting-fields). Report project-wide attention once per owning project; do not infer asks from its tracker or body. Missing or conflicting project reporting is Coverage, not permission to repair records, read other project material or dispatch work.
- Each agent PR, read-only with the profile's forge account: state, reviews, mergeability, changed files. Agent PRs are the ones on a branch named by an `agent/packet.md` whose work state is not `complete`, including tasks no longer in `lanes.md`. Other open PRs in the repository are not agent PRs.
- Each worktree the previous digest listed: whether the path still exists and the current state of its PR. Drop it once the path is gone or the PR merged.

## Report

Cover everything since the previous digest. Write `YYYY-MM-DD.md` and `YYYY-MM-DD.receipt.json` (input paths, byte hashes, read times) in the reports folder, then post the report in this thread followed by one line with the file path. Use Markdown headings and bullet lists in both the saved report and the thread message. Separate bullets and paragraphs with blank lines for mobile readability. Link each PR and task when its link is known. Do not wrap the report in a code block.

```markdown
# Agent results

Since <previous digest time>. Sweep: <recorded for YYYY-MM-DD | not recorded for last night>; <n> lanes; <n> open agent PRs.

## Ready for review

- **<task>** — <PR>; checks: <outcome>; live: <outcome>; size: <actual> (est. <n>).

## Needs you

- **<task>** — <result>; <decision needed>.

## Waiting

- **<task>** — <reason: dependency, capacity, start window, lane held, not placed: check failed>.

## Housekeeping

- **PR conflicts:** <same files changed in one repository, or none>.
- **Worktrees from closed, unmerged PRs:** <paths, or none>.
- **Effort:** <tasks finished>; <agent-minutes where known>.
```

Run every input check, including when `lanes.md` has no lanes. An empty result is a finding: write "None". A check you did not run is a failed run, so run it within the cap.

Report held queued work under Waiting and the holding task's unresolved recovery ask under Needs you. A withdrawn `draft` task retained only as a recovery entry is consistent with a held lane, not a coverage gap.

Only these go under Needs you as a coverage gap: a sweep not recorded for last night, a command or read that failed (name it and its error), and a task whose work state contradicts its lane. Never repair records or guess an outcome.
