---
name: delegated-execution
description: "Use when deciding whether to delegate, coordinating subagents, or consulting an advisor on a consequential decision. Defines execution choices, delegation authority, ownership, review, and recovery requirements."
---

In a top-level thread, delegate hands-on work to subagents by default; this is the user's standing request. Work inline when the user says not to delegate, or when a step costs less than a subagent round trip. Subagents and delegates do their brief without delegating further unless it allows. Within those rules, choose the approach likely to complete and verify the task efficiently. Direct work, tool batching or code mode when supported by the harness, and subagents are all options. Consider expected elapsed time, context and token cost, coordination overhead, and the value of independent evidence. Keep tightly coupled work in one place, inline or with one worker.

When supported, code mode can batch tool calls, filter results, or process data without another agent. Follow the harness's tool contracts, sequence dependent actions, and preserve permission and verification gates. Tool parallelism does not provide an independent review. Honor explicit requests and workflow requirements for independent reviewers.

Execution task owners may delegate exploration, independent review, or implementation assistance without separate per-launch approval, within the authorized outcome, source scope, and recorded effort and launch reservations. The parent keeps responsibility for scope, synthesis, integration, verification, and acceptance.

Explicit task restrictions and human gates take precedence. Advisors keep their separate consent policy. The active harness owns launch, permission, resume, and failure protocols.

For each new general T3 work item, classify its difficulty under [model policy](references/model-policy.md#general-top-level-tasks) and pass it to the resolver for the task assignment. Choose helpers and specialists independently by role or explicit choice; never inherit the parent's difficulty automatically. Mixed items retain separate selections and approvals, and the existing parent model is not changed by resolving a candidate.

At a task checkpoint, record the source and version of tool guidance, the relevant invocation and limitations, and the evidence checked. After compaction or resume, reuse unchanged guidance from that checkpoint. Re-read that guidance source when the operation or version changes, evidence is missing, or an error requires detail. Before dispatch, check current availability, permissions, model, and capacity. A checkpoint does not show that these remain available.

Before dispatch or resume, read [model policy](references/model-policy.md) and [resolver usage](references/model-policy-configuration.md). Resolve future launches immediately before dispatch, retaining winning source/key, hashes and native arguments; compare returned runtime settings. Existing runs and schedules retain their contracts. Check permission, capacity and budgets separately. When using T3 Code orchestration, read [T3 routing](references/t3-routing.md) for task identities, completion and timeout evidence, and independent review rounds. When working in Claude Code, read [Claude Code routing](references/claude-code-routing.md) for confirming the session, launching and continuing children, completion, cross-session reports, schedules, and the per-session permission boundary. Neither routing reference grants additional authority.

Read [work-lifecycle](../references/work-lifecycle.md) for feedback, checkpoint, resume, and acceptance rules. Include its absolute path in worker briefs that span sessions or implement a plan. Pass the entry and its linked current state (or the legacy current owner), and tell the worker which records it owns. Use [shared audience placement](../references/context-routing.md#local-work-audience-layout) for warranted durable reports. Runtime output bindings still own the actual report paths, and required report formats remain intact.

For a parent-owned queue or dependency frontier, read [queue orchestration](references/queue-orchestration.md). For bounded unattended completion, read [autonomous runs](references/autonomous-runs.md). For worktree inventory or cleanup planning, read [worktree cleanup](references/worktree-cleanup.md). These references extend this skill's ownership and recovery rules. They do not grant remote, merge, or deletion authority.

## Outcome and delegation authority

Apply [role applicability and resumption](../references/work-lifecycle.md#role-applicability-and-resumption) before task-thread requirements. Helpers return to their assigning parent. In a direct session, the main agent is the execution task owner. A task thread asks and reports to the user directly in its own thread. Do not require T3 identifiers or probe T3 in a standalone session. T3 mechanics separately require [current session identity](references/t3-routing.md#confirm-the-current-session).

Keep one accountable task owner per outcome. Substantial project research, investigation, implementation, or verification goes to the outcome's task thread, not the Desk. Execution helpers and independent reviewers belong under that owner.

For an existing outcome, reconcile and resume its saved owner and never duplicate it. Before dispatching a new outcome, settle source scope, task or top-level thread permission, acceptance, and reporting. The task owner records and announces its finite cumulative effort and launch reservations. Missing nonbudget authority blocks dispatch. A missing effort estimate calls for owner notification and never an approval question.

Apply this boundary to future dispatch and scope growth. Surface a scoped handoff need rather than automatically interrupting, replacing, restarting, or migrating active work. Preserve narrower role agreements, direct human steering, local acceptance and human gates, privacy, and resource constraints. This grants no blanket top-level thread permission.

Source access and write authority are separate. Explorers and reviewers default to no writes, owner messaging, or independent report chains. Explorers never delegate. Other children delegate only under [T3 exploration nesting](#t3-exploration-nesting). Findings return to the assigning parent for source verification and acceptance checks. Any write exception needs explicit scope and reservation from the task's authority. A read-only helper does not become a competing implementation owner. Shared writes must be reserved and serialized.

Within otherwise authorized scope, the accountable task owner sets and records a finite effort allowance in agent-minutes, cumulative launch reservations, and concurrency reservations. The owner informs the user and proceeds without approval solely for agent time, effort, or delegation budget. When the work has no durable record, the owner states this bound, and any later revision, in the conversation with the user instead of in a checkpoint. Parent work, children, retries, and corrections share cumulative usage. Record spent and remaining effort and launches before dispatch or resume. A new turn, replacement, or correction never resets them. If more effort or budgeted launches are needed, disclose the revised finite bound, the cumulative usage, the reason, and any actual overruns. Inform the user and continue without a budget-only question or silent reset.

Owner budgeting does not grant source access, new top-level threads, paid generation or external spend, destructive actions, cancellation, or human acceptance authority. Explicit nonbudget safety, role, privacy, and runtime restrictions remain gates. Fixed concurrent, model, and runtime limits remain until separately changed, and reservations do not mutate configuration. Notification does not resume stopped work or retry an uncertain operation.

Each recurring job's per-report cap stays as recorded in that job's contract. Parent and descendant effort share that cap. Owner notification does not extend the cap or grant recursion. Scheduled inspections have no delegation authority unless their specific contract permits it. These exceptions grant no new top-level conversations, source access, scheduler mutation, or acceptance bypass. Advisors retain separate consent.

## Bounded exploration

Under the default above, delegate exploration of unfamiliar behavior across subsystems, comparisons against source evidence, and multiple independent questions. Scope the questions and dispatch only under the authority and remaining allowance above. Keep quick intake and known-file routing reads inline.

Run at most two read-only explorers concurrently, with no further delegation. One explorer is enough for one substantial question. Use the [model policy](references/model-policy.md#concurrent-subagents) for initial time limits and lower caps. Each brief states the workspace, repository, or path scope; the sources and skills to read first; one question; the expected evidence; and a stop condition. Resolve the `exploration` role for the worker's execution context.

The parent owns synthesis and decisions. It verifies consequential claims, reconciles contradictions, and distinguishes observation, inference, and proposal. Runtime output bindings determine child report paths and give no write permission. A read-only child returns findings through the harness unless an artifact write is explicitly authorized. Promote only useful evidence into durable research. Never use hidden shared plan writers. When decomposing an accepted plan, reuse sufficient existing research.

## Choose the role

- **Worker:** assist the accountable execution owner with a bounded implementation task within reserved scope and remaining budget. Exploration or review does not authorize implementation. An explicit no-assistance or no-descendant contract keeps implementation inline. When a script can apply the same edit to every unit in one pass, run it yourself instead of delegating hand edits. Edit the first unit by hand, then run the script on that unit's original state and diff the result with the hand edit before running it on the rest. When workers share one procedure, put its steps, verification contract and the paths they must not touch in one file outside their write scope.
- **Reviewer:** independently assess completed work against requirements and evidence. Default to no edits or owner messaging. Only the T3 exploration-nesting exception permits children. Return findings to the parent and retain responsibility for the independent verdict. When the user asks an agent to review and also change the work, read [review and fix](references/review-and-fix.md).
- **Advisor:** help choose a direction before or during work. Read [advisor dialogue](advisor.md) for triggers, user preferences, decision briefs, supervisor exchange, and completion. Its decision format replaces implementation report fields. Shared permission and harness rules still apply.

## T3 exploration nesting

Only in confirmed T3 Code work, a direct worker or reviewer may spawn read-only exploration leaves. The outcome owner is depth 0, its direct helper is depth 1, and an exploration grandchild is depth 2. No deeper delegation is permitted, and nested writers, reviewers, and advisors are not permitted. An explorer may not delegate. Ordinary standalone restrictions and explicit task grants of no descendants remain binding. This permission grants no new source, action, model-switch, schedule, or top-level-thread authority.

Before dispatching a depth-1 helper, the root owner must reserve its possible exploration leaves within the original outcome's cumulative effort and launch allowance and the [shared role and total limits](references/model-policy.md#concurrent-subagents). Give the helper subtree slots that do not overlap with other slots, plus its maximum launches, remaining effort, exact source scope, exploration model and effort, stop conditions, and depth ceiling. Active, waiting, and uncertain parents and descendants consume capacity, and a waiting helper does not free its slot. No child may mint a new allowance or reuse a sibling's reservation. If these reservations or supported nested controls are missing, return the bounded search request to the parent instead of launching or bypassing the limit.

Each exploration leaf gets a narrow question bounded to its sources, no writes, no descendants, and output limited to findings for its immediate parent. The helper checks the findings and retains its own implementation, review, and synthesis responsibility. It reports leaf task and run identities, terminal or pending state, costs or unknowns, and unresolved issues to the root. Reconcile the entire reserved subtree before accepting completion or releasing capacity under [T3 task routing](references/t3-routing.md#retain-identity-and-inspect-completion). Policy limits are parent-managed accounting. They make no claim of native global enforcement or tested nested-runtime support.

## Scope and ownership

- Include the relevant agreed acceptance criteria, their authoritative location, and the required evidence in each brief. Workers report pending criteria and evaluated results (passed, failed, blocked, or awaiting human review). They may propose contract changes but cannot silently redefine success. If the assignment is to clarify ambiguous intent, pass [define-outcome](../define-outcome/SKILL.md).
- Give each worker one bounded task with exact paths, acceptance criteria, verification commands, out-of-scope items, and a numeric size ceiling. Stop and report if it grows beyond that ceiling.
- Pass relevant repository constraints and known baseline results. Do not invent counts or assume the child inherited instructions. Default to no further delegation. Only an explicit depth and slot reservation under the T3 exploration-nesting contract permits exploration leaves.
- Resolve required skill paths before dispatch and include their absolute paths in the brief. Tell the child to read applicable repository instructions, those skills, and their matching references before acting. Do not assume it sees the parent's skill catalog or conversation. If a required resource is missing, stop the dependent work and report it.
- Keep one accountable implementation owner and one active writer per shared checkout. Reserve exact write scopes and serialize shared writes. Do not create worktrees; the only exception is an agent-pickup lane, when the experimental `agent-pickup` skill is installed. Parallel writers on one checkout must have disjoint reserved write scopes or run serially. Read-only reviews do not become implementers. Follow the model policy's role limits and lower outcome and harness caps rather than inferring extra capacity.
- Probe unfamiliar capabilities before building on them. Prefer read-only queries and return the invocation and actual output.
- Delegate only authority the user granted. A worker assignment does not itself authorize commits, pushes, or destructive cleanup.

## Select skills for the assigned work

Resolve these paths relative to this skill directory, then pass only those the assignment needs:

- Code implementation in any language: [coding-standards](../coding-standards/SKILL.md).
- Naming or changing code: [write-discoverable-code](../write-discoverable-code/SKILL.md). Use repository standards for other language-specific concerns.
- Bug investigation: [work-lifecycle](../references/work-lifecycle.md#plan-act-verify-accept) for evidence and verification, plus the actual `browser` or `terminal` owner for live reproduction. Pass the original scenario and the surface and profile. Include implementation skills if fixing.
- Explicit research or deeper investigation of a consequential uncertainty: the research steps of [rpi](../rpi/SKILL.md), with subagents launched under [RPI local rules](../references/rpi-local.md#subagents-and-models).
- Human-facing artifacts, including any file saved under a workspace `review/` folder: [Writing reviewable artifacts](../references/reviewable-writing.md) and [unslop](../unslop/SKILL.md).
- Authorized commits: [commit](../commit/SKILL.md). Authorized PR work: [pr](../pr/SKILL.md), which routes to PR writing standards.

For implementation, have the worker inspect relevant code, callers, tests, and conventions before editing. It should identify the change location, the affected contracts, and the verification approach. Ordinary exploration needs no research artifact. If an uncertainty prevents a safe change, report the bounded question and investigate within scope or request the missing authority.

## Dispatch and report formats

Use this brief structure so a fresh worker can find its authority, inputs, and finish condition. Fill only applicable fields, and record missing baseline evidence as unknown. Resolve paths and commands before dispatch rather than sending placeholders.

```text
Task: one outcome or question
Scope: exact source/read paths; reserved write paths if any; exclusions; numeric size ceiling
Budget: announced owner-set finite bound; cumulative consumed/remaining effort and launches; concurrency reservations; fixed caps
Read first: applicable repository instructions; required absolute skill paths
Context: entry artifact; accepted decisions; current baseline and source revision
Acceptance: criterion IDs/text and required evidence
Verification: commands/actions, working directory, expected observations
Stop: missing resources, scope/decision limits, failed gates
Ownership: checkout/artifacts this worker may change; checkpoint link and write owner
Reporting: the parent for a helper; the user in the task thread for a task thread; a stable `clientRequestId` only for T3 delegation
Restrictions: no further delegation unless T3 exploration-only reservations of depth, slots, and effort are supplied; commits and pushes only if explicitly authorized
```

Require the worker to return this result structure, with evidence rather than expected results:

```text
Status: complete / partial / blocked
Event (helpers only): stable request IDs supported by the transport; report time; evidence/source times
Checkpoint: owning record link and write owner
Criteria: each ID: pending / passed / failed / blocked / awaiting human review
Work: changed paths, or source-backed findings for read-only work
Verification: commands/actions actually run; results; evidence paths
Discoveries: refuted assumptions and resulting changes
Remaining: blockers, unverified claims, next action
Artifacts: output paths; commit SHAs only if created with authorization
```

The runtime's required structured output can carry these fields instead of duplicating them in prose. Bind durable output through the harness when supported. Do not rely on a filename mentioned only in the brief.

Keep large logs and inventories in bound artifacts. Return concise findings, exact checks and errors, pending criteria, and artifact references in the fields above. The parent still inspects decisive source, diff, and verification evidence before acceptance.

A task thread reports meaningful milestones, blockers, decisions needed, scope changes, and verification results to the user in its own thread, and reports before pausing or finishing. Each report leads with the decision or result needed and links the checkpoint and artifacts instead of pasting them. It also gives the remaining work and next action, and evidence with source times. Task-owned helpers return only to their parent.

Sending does not prove processing. Check the thread for the message before an uncertain retry, and preserve uncertainty instead of duplicating a report. Do not send every-tool updates or create acknowledgment-only turns.

Apply [human contact and direct steering](../references/work-lifecycle.md#human-contact-and-direct-steering). The user's direct steering is recorded in the task checkpoint like any other decision.

## Review and recovery

- Before an authorized pause or finish, preserve the owned checkpoint and send the task report above. A pause does not waive reporting or human acceptance.
- At a required human review, follow [the review pause](../references/work-lifecycle.md#pause-for-human-review). Ask the user directly in the task thread with the exact question, the artifact and evidence, and the reviewed revision. Then end the turn. Do not replace human acceptance with agent review. Stop new dependent dispatches and bring affected running workers to safe checkpoints through the harness. Preserve authorized independent work and the pending-review state explicitly.
- Inspect the actual diff and verification output before accepting work. Check changed assertions, suppressions, call sites, failure handling, and possible data loss.
- Compare the result with the original request and each acceptance criterion. Accept only when evidence satisfies the required criteria and checks. Return unmet criteria for correction or report a blocker. A worker's completion report alone is not acceptance. For read-only work, inspect cited sources and resulting findings instead of requiring a diff.
- For a regression claim, prove the test catches the original bug when feasible, using an isolated copy or safely reversible patch. For pure moves, compare removed and added code and run existing tests unchanged.
- Send corrections to the original worker when it is resumable, within the same remaining outcome budget. Repeated corrections or timeouts call for a smaller task. Preserve partial work and follow the harness recovery protocol before any authorized retry. A replacement or new turn does not reset cumulative usage.
- Check the result fields above against the actual evidence. Pending or unsupported required criteria prevent acceptance. Request the missing evidence rather than assuming an omitted field passed.
- An accurate partial report is preferable to unsupported success. Escalate uncovered decisions, failed gates, missing authority, and removal of intentional functionality.

For long tasks, record progress, verified facts, corrected assumptions, and remaining work in the task's durable artifact. Continue through authorized steps and stop at an actual decision or blocker.
