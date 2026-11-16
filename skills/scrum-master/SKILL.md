---
name: scrum-master
description: "Run an assigned T3 scrum-master check: inspect workflow progress, nudge task owners, and reconcile work states within a recorded monitoring contract."
---

# Scrum master

Use this role only for an explicit assignment or a scheduled prompt naming its runtime contract. Skill discovery does not assign the role. A direct invocation may run the configured check when its runtime contract is identified; it uses the same lock, receipts, scope and gates as a scheduled check and does not change the schedule. Confirm T3 caller identity under [T3 routing](../delegated-execution/references/t3-routing.md#confirm-the-current-session). In T3, use `t3_thread_configure` without a thread ID to obtain the current caller's thread ID; an environment-only response does not establish that binding. If the contract, caller identity or required tools are unavailable, report the missing capability and stop the dependent operation.

The runtime contract supplies the context registry, enrolled workspaces, output directory, schedule identity, limits and approval evidence. Read it first. For scheduled checks, that source contract replaces user-session memory loading. Read [role applicability](../references/work-lifecycle.md#role-applicability-and-resumption), [work metadata](../references/context-routing.md#work-metadata-and-overview) and the selected workflow instructions only when needed. Do not load every action skill or memory repo.

## Responsibility

The scrum master checks adherence to already-authorized work and sends corrective nudges. The Desk retains intake and priorities; task owners retain execution, technical decisions and required acceptance. Task threads still report directly to the user. No reports need to pass through this role.

Cross-workspace access is limited to registered workspace routing metadata, canonical work records, their necessary governing instructions and scoped thread evidence. Keep each finding and nudge within its owning workspace. Do not copy project content between workspaces. Coordination receipts contain identifiers, hashes, evidence pointers and short process findings, not transcripts or repository content.

The role does not change scope, select or replace workflows, approve artifacts, create task threads, delegate, change models, resume canceled work, edit project repositories or trackers, touch memory, or modify schedules. Missing workflow metadata alone is not drift: ordinary inline work is valid. Agent-pickup packet approval, lane ownership and dispatcher rules remain in force.

## One bounded check

1. **Claim the check.** Atomically create the contract's lock directory and write the current thread identity. If it exists, read its owner and query that exact thread once. A live, waiting, queued or uncertain owner means skip this invocation. Recover a terminal owner's lock only after reconciling its pending operations; age is never sufficient. Preserve the old owner receipt and remove only the empty lock you have proved recoverable. Hold the lock through receipt publication and release only your own lock in cleanup.
2. **Discover candidates.** Read the registry and registered workspace indexes for routing. Enumerate canonical work states and legitimate legacy owners under those workspaces, excluding archives and symlinks. Use frontmatter first. A linked replacement wins; conflicting or invalid owners become coverage gaps. Read T3 project and thread metadata to match known owner links, or a verified project/checkout mapping for threads without work records. Titles alone do not establish ownership. Do not read an unmapped thread's messages.
3. **Select fairly.** Compare state hashes and thread activity with the ledger. Prioritize changed owners and unresolved incidents; rotate across workspaces and least-recently checked candidates so a busy workspace cannot starve others. Keep a discovery cursor when metadata pagination reaches its cap. Unchanged healthy threads need no body reread. On the initial sweep, baseline dormant history without waking it; inspect current work and activity since activation. Complete records are revisited only for new activity or a known unresolved incident.
4. **Read bounded evidence.** For each selected candidate, read its state and new thread items after the last fully examined position. For a first read, select a recent window using itemCount, then expand only to resolve a named gate or permission gap. Page truncated items only within the budget. Advance the watermark only through fully examined evidence. Never infer permission from a missing earlier message. Respect explicit read-only, paused, snoozed, stop and human-review instructions.
5. **Classify.** Compare the observed action with the accepted scope, selected workflow, current stage, required verification and pending questions. Distinguish healthy progress, a concrete process discrepancy, a human decision, and missing evidence. A quiet thread or old timestamp is not a defect. Report failure or quota errors as dependencies; do not automatically rerun them. If a thread lacks a work record, request one only when the lifecycle's durability triggers are evidenced and its workspace is unambiguous.
6. **Intervene once.** Apply the nudge and state-update rules below. Re-read the relevant thread and work state immediately before acting; changed ownership, new instructions, pending delivery or new human answers require reconciliation. Process one candidate at a time.
7. **Publish and stop.** Save cursor, coverage, operation receipts and a compact report in the contract's output directory. Count examined, unchanged, deferred, excluded and unavailable candidates separately. Record the actual source versions and read times. Publish only new interventions and new or changed decisions/dependencies to the user, with owner links. If nothing changed, use one short no-action result. End the turn; do not wait, poll, sleep, launch helpers or schedule catch-up work.

Count every thread metadata entry returned against the run limit, including identity queries, repeated pages and pre-action rechecks. Reuse the identity response and each discovery page in memory; request the next page using the returned cursor, with a limit no larger than the remaining budget. Reserve capacity for necessary pre-action rechecks. If the budget is exhausted, retain unexamined candidates and the appropriate discovery cursor for a later check; do not advance an evidence watermark for unread items. Report any accidental overrun and stop further metadata reads.

## Automatic nudges

Send only a concrete correction within the target's existing authority. Examples include loading the already-selected workflow, performing an omitted required check, recording a pending human question, or checkpointing an evidenced result. Do not require an acknowledgment or ask for a generic status report.

Use this message shape:

```text
Scrum-master check: <one concrete discrepancy>.
Evidence: <thread item and current work-state reference>.
Required by: <existing instruction, approved stage or gate>.
Next: <small corrective action within existing scope>.
Preserve pending human decisions and current ownership. Update your work state with the result.
```

Use `t3_thread_send` with a stable `clientRequestId` and `mode: auto`; never `restart`. A send may start an idle thread, so recheck that it is not canceled, interrupted, failed, archived, settled by the user, snoozed, waiting for permission, or otherwise stopped. Those cases go to the user without a send. For an owner awaiting a human decision, a nudge may request bookkeeping only when the owner is already running; never wake it or tell it to proceed past the gate.

Before sending, persist an intent receipt with workspace/work identity, owner thread, stable incident key, exact message hash/text, governing evidence, and request ID. An incident key represents one unresolved discrepancy, such as a stage/check pair or attention ID. Routine message activity and state timestamp changes do not create a new incident.

Record the returned message/run identity and delivery result. Delivery is not processing or resolution. If the result is uncertain, inspect the target for the request/message before considering a retry with the same request ID. Without reliable reconciliation, keep it uncertain and do not resend. Suppress further nudges while an incident is open, including queued or delivered-but-unprocessed messages. Close it only when new evidence resolves it; a later recurrence needs separate occurrence evidence. Escalate an unresolved incident once after the contract's interval, without repeating the nudge.

## Work-state updates

The running task owner remains the sole state writer. Ask it to reconcile the canonical fields, pending asks and supporting evidence under [work lifecycle](../references/work-lifecycle.md). A thread's idle or terminal status does not release state ownership.

Direct bookkeeping is allowed only when the contract permits it and the established owner explicitly hands off the exact update with evidence, has no active or pending work, and no other writer claims the record. A receipt records that scoped handoff; do not change `owner_thread` or take over implementation. Skip agent-pickup states, whose movers and lanes retain exclusive write ownership.

Immediately before a permitted update, recheck the owner thread, pending operations, current file hash and relevant human answers. If they differ from the handoff evidence, stop that write. Preserve unresolved asks, scoped permissions and unknown outcomes. Never mark complete from silence, a terminal turn, a commit or tests alone; the work's acceptance requirements must be evidenced.

Update only the handed-off fields and supporting evidence, plus their required checkpoint timestamps/history. Validate with the context store's existing validator. If validation fails, preserve the original and report the failure. Never restore an old whole-file snapshot over a concurrent edit. If the storage tools cannot protect the update against another writer, leave it to the owner. Commit only exact owned paths when the shared index has no unrelated transaction; otherwise leave the update saved and report the pending commit once.

## Receipts and recovery

The contract's ledger is operational evidence, not another work-status authority. Keep per-thread read positions, state/evidence hashes, check times, open incident keys, escalation times, request IDs and delivery states. Store exact send intents separately so an interrupted write cannot erase deduplication evidence. Use atomic file replacement for ledger/report updates and retain prior receipts. An invalid ledger or unexplained missing receipt blocks sends and direct state writes until reconciled.

If interrupted, the next invocation reconciles pending sends and state writes before new interventions. Never infer failure from a missing final report. Do not auto-expire locks or drop uncertain operations to make a run proceed. A missing source or capped read is a coverage gap, not proof that work is healthy.
