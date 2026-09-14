---
name: delegated-execution
description: "Use when delegating work, coordinating subagents, or consulting an advisor on a consequential decision. Defines permission, ownership, dialogue, review, and recovery requirements."
---

Delegate when independent work or context isolation earns the coordination cost. Follow the user's delegation preference; handle small tasks inline. The active harness owns launch, permission, resume, and failure protocols.

Read [work-lifecycle](../references/work-lifecycle.md) for feedback, checkpoint, resume, and acceptance rules. Include its absolute path in worker briefs that span sessions or implement a plan; pass the current entry artifact and tell the worker which records it owns.

## Bounded exploration

The parent chooses independent substantial questions; do not delegate intake, quick fixes, or small factual gaps. Run at most three read-only explorers concurrently, with no further delegation. Each brief states workspace/repository/path scope, read-first sources and skills, one question, expected evidence, and a stop condition. For this user's exploration preference, use Sol with low reasoning only after discovering the harness's exact available model identifier; this is not a global override for workers, reviewers, or advisors.

The parent owns synthesis: verify consequential claims, reconcile contradictions, and distinguish observation, inference, and proposal. Runtime output bindings determine child report paths. Promote only useful evidence into durable research; never use hidden shared plan writers. When decomposing an accepted plan, reuse sufficient existing research.

## Choose the role

- **Worker:** perform a bounded task using the brief/report contract below.
- **Reviewer:** assess completed work against requirements and evidence; no edits unless separately authorized.
- **Advisor:** help choose a direction before or during work. Read [advisor dialogue](advisor.md) for triggers, user preferences, decision briefs, supervisor exchange, and completion. Its decision format replaces implementation report fields; shared permission and harness rules still apply.

## Scope and ownership
- Include the relevant agreed acceptance criteria, their authoritative location, and required evidence in each brief. Workers report pending criteria and evaluated results (passed/failed/blocked/awaiting human review); they may propose contract changes but cannot silently redefine success. If the assignment is to clarify ambiguous intent, pass [define-outcome](../define-outcome/SKILL.md).

- Give each worker one bounded task with exact paths, acceptance criteria, verification commands, out-of-scope items, and numeric size ceiling. Stop and report if it grows beyond that ceiling.
- Pass relevant repository constraints and known baseline results; do not invent counts or assume the child inherited instructions. Children must not delegate further.
- Resolve required skill paths before dispatch and include their absolute paths in the brief. Tell the child to read applicable repository instructions, those skills, and their matching references before acting. Do not assume it sees the parent's skill catalog or conversation. If a required resource is missing, stop the dependent work and report it.
- One writer per checkout. Parallel writers need isolated worktrees; parallel reviews need disjoint surfaces. At most three concurrent children.
- Probe unfamiliar capabilities before building on them. Prefer read-only queries and return the invocation and actual output.
- Delegate only authority the user granted. A worker assignment does not itself authorize commits, pushes, or destructive cleanup.

## Select skills for the assigned work

Resolve these paths relative to this skill directory, then pass only those the assignment needs:

- TypeScript/Go implementation: [coding-standards](../workflow/coding-standards/SKILL.md).
- Naming or changing code: [write-discoverable-code](../workflow/write-discoverable-code/SKILL.md); use repository standards for other language-specific concerns.
- Bug diagnosis: [diagnosing-bugs](../workflow/diagnosing-bugs/SKILL.md), plus implementation skills if fixing.
- Explicit research or deeper investigation of a consequential uncertainty: [research](../workflow/research/SKILL.md).
- Authorized commits: [commit](../commit/SKILL.md). Authorized PR work: [pr](../pr/SKILL.md), which routes to PR writing standards.

For implementation, have the worker inspect relevant code, callers, tests, and conventions before editing. It should identify the change location, affected contracts, and verification approach; ordinary exploration needs no research artifact. If an uncertainty prevents a safe change, report the bounded question and investigate within scope or request the missing authority.

## Dispatch and report formats

Use this brief structure so a fresh worker can find its authority, inputs, and finish condition. Fill only applicable fields; record missing baseline evidence as unknown. Resolve paths and commands before dispatch rather than sending placeholders.

```text
Task: one outcome or question
Scope: exact paths; allowed actions; exclusions; numeric size ceiling
Read first: applicable repository instructions; required absolute skill paths
Context: entry artifact; accepted decisions; current baseline and source revision
Acceptance: criterion IDs/text and required evidence
Verification: commands/actions, working directory, expected observations
Stop: missing resources, scope/decision limits, failed gates
Ownership: checkout/artifacts this worker may change
Restrictions: no further delegation; commits/pushes only if explicitly authorized
```

Require the worker to return this result structure, with evidence rather than expected results:

```text
Status: complete / partial / blocked
Criteria: each ID — pending / passed / failed / blocked / awaiting human review
Work: changed paths, or source-backed findings for read-only work
Verification: commands/actions actually run — results — evidence paths
Discoveries: refuted assumptions and resulting changes
Remaining: blockers, unverified claims, next action
Artifacts: output paths; commit SHAs only if created with authorization
```

The runtime's required structured output can carry these fields instead of duplicating them in prose. Bind durable output through the harness when supported; do not rely on a filename mentioned only in the brief.

## Review and recovery
- At a required human review, follow [the review pause](../references/work-lifecycle.md#pause-for-human-review). Return the artifact and decision to the user and end the turn; do not replace human acceptance with agent review. Stop new dependent dispatches and bring affected running workers to safe checkpoints through the harness. Preserve authorized independent work and pending-review state explicitly.

- Inspect the actual diff and verification output before accepting work. Check changed assertions, suppressions, call sites, failure handling, and possible data loss.
- Compare the result with the original request and each acceptance criterion. Accept only when required criteria and checks are satisfied by evidence; return unmet criteria for correction or report a blocker. A worker's completion report alone is not acceptance. For read-only work, inspect cited sources and resulting findings instead of requiring a diff.
- For a regression claim, prove the test catches the original bug when feasible, using an isolated copy or safely reversible patch. For pure moves, compare removed and added code and run existing tests unchanged.
- Send corrections to the original worker when resumable. Repeated corrections or timeouts call for a smaller task; preserve partial work and follow the harness recovery protocol before retrying.
- Check the result fields above against the actual evidence. Pending or unsupported required criteria prevent acceptance; request the missing evidence rather than assuming an omitted field passed.
- An accurate partial report is preferable to unsupported success. Escalate uncovered decisions, failed gates, missing authority, and removal of intentional functionality.

For long tasks, record progress, verified facts, corrected assumptions, and remaining work in the task's durable artifact. Continue through authorized steps; stop at an actual decision or blocker.
