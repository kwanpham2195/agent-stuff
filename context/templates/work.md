---
type: work
workspace: replace-with-workspace-id
id: replace-with-work-id
# project: replace-with-project-id
# parent: replace-with-parent-work-id
title: Work title
status: draft
progress: Planned work; execution has not started.
next_action: Confirm scope and acceptance before execution.
blocker: ""
updated: YYYY-MM-DD
---

# Work title

Use this template for `work/<work-id>/agent/state.md` when creating authorized durable work. Enable
`project` for work in a project and `parent` for a sub-issue, using IDs from the same workspace and
project; omit them otherwise. Keep one bounded outcome here. The project owns its backlog, decisions
and references. Keep `work/<work-id>/index.md` as navigation, optional when state is the only file.
Existing records remain authoritative until explicitly migrated. Follow
[context routing](../../skills/references/context-routing.md#place-context-and-artifacts) for
placement and
[work lifecycle](../../skills/references/work-lifecycle.md#checkpoint-before-context-is-lost) for
retention. Apply [writing for agents](../../skills/writing-for-agents/SKILL.md).

## Objective and authority

State the objective, scope, granted and withheld permissions, and approval source. Link the issue,
plan, or contract when it owns them.

## Acceptance

Link the criteria authority and record current evidence status. State may own a small task's
criteria only when no other artifact does. Include the exact pending review target/version and
decision, or state that no review is pending.

## Read first

Link only the authorities and instructions required for the next step.

## Decisions

Record accepted choices and useful reasons only when no other authority owns them. Otherwise link
the owning decision.

## Evidence

Record the latest verification scope, result, and tested revision. Link detailed findings, reports,
and raw evidence; retain specialist report formats there. Distinguish observed facts from proposals
and unverified claims. Keep compact progress and status in the frontmatter, with their supporting
evidence here.

## Resume details

Explain the decision or dependency resolution needed for the frontmatter's next action. Add
checkout, dirty-file ownership, active operations, or uncertain external receipts only when needed
for safe recovery. Never replay an uncertain write because its result was lost.

Use [brief reporting fields](../../skills/references/context-routing.md#brief-reporting-fields)
after owner reconciliation; list only asks blocking this outcome and link their question owner. Do
not copy project-wide attention here or infer approval from linkage.

Follow lifecycle retention for snapshot size and dated history entries. Keep digests in evidence or
history, raw output and one-off probes in `evidence/<yyyymmdd>-<slug>/`, and reusable tools in a
repository.
