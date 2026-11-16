---
type: project
workspace: replace-with-workspace-id
id: replace-with-project-id
title: Project title
status: draft
progress: Goal identified; bounded work has not started.
next_action: Confirm goal, milestones and child outcomes.
blocker: ""
updated: YYYY-MM-DD
# initiative: optional-shared-goal
---

# Project title

Save as `workspaces/<workspace-id>/projects/<project-id>/index.md`. Follow
[projects and bounded work](../../skills/references/context-routing.md#projects-and-bounded-work).
Replace placeholders; omit unused optional fields. A context project groups outcomes and does not
authorize execution or agent pickup.

## Goal and authority

State the long-lived goal, scope, accountable owner, approval source and acceptance authority. Link
any existing tracker project/epic, repository decisions and shared documents; preserve their
authority.

## Milestones

Name the delivery outcomes and their acceptance evidence. Link the work that delivers each; do not
copy child progress.

## Children

Link bounded `work/<work-id>/agent/state.md` owners, or the Base view grouping by `project`. Each
child sets `project`; sub-issues also set `parent` to their parent work ID. Organizational links
grant no dispatch or status change.

## Project authorities

Create only needed files and link existing authorities until migration is authorized:

- `tracker.md` owns the backlog and project-wide questions.
- `decisions.md` owns accepted cross-work decisions when no existing shared authority owns them.
- `reference/` owns project contracts, crosswalks, guides and reference maps.

## Attention

Publish `brief_checked_at` and `brief_attention` together in frontmatter only after actual owner
reconciliation under
[brief reporting fields](../../skills/references/context-routing.md#brief-reporting-fields).
Project-wide asks link their governing tracker question. Preserve unanswered ask IDs and resolution
evidence; child attention contains only blockers of its own outcome. Missing reporting is a Coverage
gap, not an empty attention list.
