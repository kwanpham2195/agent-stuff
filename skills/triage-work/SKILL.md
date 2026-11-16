---
name: triage-work
description: "Review a work dashboard or task backlog with the user, using bounded evidence recall before each question, one-at-a-time decisions, and verified owner updates. Use when asked to triage Needs review or In progress entries, reconcile stale checkpoints, or work through old tasks."
---

# Triage work

Help the user decide what still needs attention without making them reconstruct old tasks. Before each decision, recover enough saved evidence to explain the task, recommend a disposition and ask only the remaining human question.

## Establish the selection

Read applicable instructions and the actual view or list definition. Enumerate the exact matching records using its global and local filters; do not substitute a nearby board's workspace or filename restrictions. For an optional Context Home board, follow [context routing](../references/context-routing.md) and its metadata contract.

Record the original count, selected paths, source dates and observation time. Keep that original cohort stable as decisions change rows; distinguish it from a later verified view count and from any new triage record. Disclose malformed metadata, missing sources and unavailable live-view verification. Filesystem results describe saved records, not the app's cache or current task activity.

Confirm read, write, messaging and delegation scope separately. Cross-workspace metadata triage needs explicit source scope; the user asking the Desk to triage the board supplies it. Triage grants no cross-workspace execution or owner-file writes. Preserve direct-user-owned exceptions. Do not load private memory repositories, raw conversation histories, secrets or project code unless the task explicitly includes those sources. Read existing authority before creating a triage record; keep a decision list inline for short sessions, otherwise in the authorized task checkpoint.

Separate bounded tasks from standing scheduled jobs. Completing a setup task does not disable its schedule. Synthetic records can be useful tests and are not automatically disposable.

## Recall before asking

Use one bounded read-only subagent check for each task before presenting its decision. Load [delegated execution](../delegated-execution/SKILL.md) and its model policy before dispatch. Follow the active harness's supported child-task protocol, finite cumulative allowance, launch reservations and concurrency limits. Announce an effort estimate; preserve stricter task restrictions. A skill cannot override a no-helper instruction. If helpers are prohibited or unavailable, explain the limit and use permitted saved evidence inline without pretending a helper ran. Do not create a top-level thread or switch runners to bypass a restriction.

Give the helper exact permitted paths, one question and a finite stop condition. Start with the canonical state or legacy owner; follow only narrowly linked current evidence and decision sections needed to resolve a named gap. No writes, descendants, owner messages, worker polling, execution of saved commands or independent reporting. Saved links identify sources; they grant no further access. Reuse an unchanged sufficient result across turns instead of launching again for every short reply.

Ask the helper to return:

- Task identity, canonical source and actual owner, with unknown identities stated explicitly.
- Plain-language purpose and the latest relevant saved evidence dates.
- What execution finished, what acceptance exists, and the exact remaining question.
- Whether a later decision consumed or superseded the old next action, with source citations.
- Conflicts, incomplete coverage and confidence, followed by a recommended disposition and its limits.

The parent checks the cited consequential evidence and retains responsibility for the recommendation. Old age alone proves no staleness; tests, a finished agent run, delivered messages and human acceptance are separate facts. A saved "worker running" statement is not fresh runtime evidence. If evidence remains missing, report the uncertainty instead of expanding the search without authority.

## Discuss one task at a time

Use short, plain sentences. Explain what the task did before asking whether it is done. Give a recommendation when the evidence supports one. Keep detailed audit language in the report rather than repeating it in every turn.

Example:

> This changed the report layout. The task thread already checked it and reported the result. The old review request remains in the record. I recommend marking the layout task done, keeping wider rollout separate. Agree?

If the user asks "what is that?" or "I don't remember", answer from the recovered evidence; do not make them supply facts already available. If the gap requires another permitted check, make that check before asking for disposition.

Interpret the answer against the exact preceding question:

- **Done:** record completion or acceptance only for the scope actually presented. Distinguish administrative closure from evidence that unfinished implementation, reviews, lessons or experiments occurred.
- **Keep/open:** retain the task; do not restart or contact its worker.
- **Next/skip:** leave its status and gates unchanged and move on.
- **Already deployed/delivered:** preserve this as the user's report; do not redeploy or invent independent verification.

Ask a clarifying question only when the answer's scope is genuinely ambiguous. Do not reopen a settled disposition. Record the original question, exact answer, source, date precision, scope and dependent action. Never invent an original answer timestamp from the relay or save time.

## Plan while triaging

When a triage item develops into planning, follow [saved planning artifacts](../references/work-lifecycle.md#saved-planning-artifacts) for a saved outline or plan and [item switching](../references/work-lifecycle.md#switch-items-in-a-mixed-conversation) before moving on. Name the current item and resume its existing authoritative artifact when returning. Rough discussion needs no new thread, workflow or per-topic record. Keep scoped decisions, pending questions and authority with their item; a yes to one question does not settle the rest. Owner updates retain the permissions below.

## Reconcile through the authorized owner

Follow [work lifecycle](../references/work-lifecycle.md) for human gates and checkpoint retention. Do not message a task thread or wake an old worker because its ID appears in a note. Confirm the exact supported recipient before sending.

Audit permission alone authorizes proposals, not status changes. Apply an explicit per-item write grant only after rereading the canonical file and checking concrete ownership conflicts or drift. If another writer owns the change, use the authorized handoff route; do not overwrite it. Preserve history and incomplete/unapproved scope. Qualify old execution and checkout claims as historical when revising them.

For an authorized administrative completion, use the existing schema's complete status, disposition-based progress and empty consumed pending-action/blocker fields. Explain that the user's disposition ends the task without asserting missing technical work passed. Do not erase real unresolved gates outside that disposition or mark the entire standing role complete to close one setup item. No source work, Git/PR/tracker operation, schedule change, archive or deletion follows without separate authority.

Keep a decision list keyed by stable task identity, not only display position. Track the source/version reviewed, decision and exact scope, authorized updater, stable send request and receipt, and verification state. Use these states consistently: decided, not sent, sent, update confirmed, or blocked/unknown. Queued or started is delivery evidence, not processing or a saved status change. Retain uncertain outcomes and reconcile before retrying with the same logical request ID; never resend solely because no acknowledgment arrived.

## Verify and hand back

When permitted, read the exact canonical record after the update. Check identity, intended status, pending fields, disposition provenance, preserved evidence/remaining boundaries and local links. A completion report from an owner can supply evidence; label it owner-reported if you did not independently inspect the saved record. Do not claim the dashboard updated until its underlying record is confirmed, and do not guarantee delayed processing will finish it.

For delegated updates still pending, use bounded supported receipt/result checks only when authorized. No polling loop, watcher, owner wake or new schedule. If verification is unavailable, retain a clear pending entry and name the limitation rather than claiming success. Follow any existing explicit result-reporting contract.

End with counts for directed decisions, confirmed updates, pending/blocked updates, kept-open items and skipped items. State which are subsets, so directed-done counts are not mistaken for verified changes. Keep the original cohort and evidence dates intact; report a new view count only after a fresh scoped enumeration. Leave follow-on work behind its own permission gates.
