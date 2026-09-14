# Work lifecycle

Use this contract for work that needs planning, review, multiple sessions, or transfer to another owner. It applies to the main agent and delegated workers. Repository instructions and the user's authorization determine permitted actions.

## Collaboration defaults

- Clarify ambiguous requests before acting on the uncertain part. State the plausible interpretations and recommend one. Investigate factual unknowns yourself; do not ask the user to rediscover information available in the repository or tools.
- “Implement this” permits routine implementation choices within the stated scope. Present consequential alternatives in behavior, architecture, or scope for a decision before committing to one.
- Show an early useful sketch when the direction is uncertain; prepare a coherent proposal when requesting execution approval. Label which kind of feedback is needed.
- “Iterate on this” means one revision per feedback round for subjective design. For objectively verifiable fixes, continue within scope until agreed criteria are met or a decision/blocker requires the user. Clarify which mode applies when unclear.
- Ask a small batch of related decisions with visuals where useful, tradeoffs, and a recommendation. Ask sequentially when an answer determines the next question.
- “Looks good” approves the reviewed artifact. It authorizes implementation only when that broader workflow was already requested and this approval resolves its review gate. If the next action or approval scope is ambiguous, clarify it.

Explicit task instructions override these defaults. Do not repeatedly ask about decisions the user has already settled.

## Choose the smallest mode

- **Inline:** the scope is small and the relevant context fits comfortably in the conversation. State the outcome and verification approach, do the work, and report evidence. No mandatory document or research phase.
- **Durable:** research, planning, discussion, or implementation must survive context loss. Maintain one entry artifact using an existing relevant document, an ExecPlan, or the user's chosen path. Follow [context-routing](context-routing.md) to select its home or resume selected context. A discussion checkpoint does not require a full ExecPlan.
- **Tracked:** the user wants work queued or assigned through local workspace issues or a configured remote tracker. Use the `issue` skill's implementation-handoff mode. Destination and scope must be explicit or authorized by a workspace default before creation. Drafting does not authorize publishing, assigning people, implementation, or status changes.

Switch modes when scope grows, ownership changes, or unresolved decisions and evidence would be costly to reconstruct. Explain the switch briefly. Respect read-only requests: return a checkpoint inline or request permission to save it.

## Keep working context bounded

- Resolve the workspace and authoritative entry through [context-routing](context-routing.md) before mining history or creating records. Reuse the owning plan, issue, and accepted decisions. Small work stays inline; durable work has one entry point with links to the authorities for each concern.
- Load the current phase's outcome, acceptance criteria, dependency results, prototype findings, required instructions, and relevant code. Follow other links only to answer a named gap. Do not reload every phase, transcript, or research artifact on each step.
- Treat sufficient search snippets as already-read evidence; a source pointer alone is only a navigation aid. Return to the source when it changed, a consequential claim needs verification, or the available excerpt is insufficient. Stop exploration when the change location, affected contracts, and verification approach are known.
- Keep large logs, screenshots, experiment output, and worker reports in their authorized artifact locations. Put only the finding, implication, source/revision, unresolved limitation, and evidence link in the entry artifact. Preserve failed approaches and their reasons when they prevent repeated work; avoid transcript dumps and duplicate summaries.
- Checkpoint after a prototype verdict, phase completion, material decision, failed gate, or review pause, using the checkpoint contract below. Record the next authorized action before switching phases or handing off. A checkpoint preserves state; it does not grant authority or prove current code still matches old evidence.
- Use context isolation only when delegation is authorized and earns its cost. Follow [delegated-execution](../delegated-execution/SKILL.md) for a bounded brief, exact source paths, ownership, and evidence reports. The parent retains synthesis and acceptance; children do not need the full conversation or unrelated phase history.

## Iterate according to the question

The activities below are revisitable, not a mandatory one-way sequence. An iteration can be a discussion, sketch, prototype, code change, or verification probe:

```text
question / desired improvement
  → smallest useful experiment or change
  → observation or review
  → keep, revise, reject, or request a decision
  → next question or completion
```

Name what the iteration should learn or improve, what evidence or feedback will decide it, and what remains provisional. Use the appropriate intent:

- **Explore:** test a hypothesis or compare alternatives. Throwaway work is acceptable when authorized; verify the learning objective and label production checks not performed.
- **Refine:** improve an agreed direction using observed behavior or review feedback. Check the changed behavior and affected contracts.
- **Finish:** satisfy accepted criteria and required repository checks before claiming implementation complete.

A successful experiment does not establish production readiness. Revisit requirements or milestones when evidence warrants it; distinguish proposed changes from accepted decisions and seek approval when scope or a user-owned decision changes.

Continue useful iterations within authorized scope. Pause for missing decisions, a scope change, an agreed time/cost/iteration limit, or repeated attempts producing no new evidence. For stalled work, report what was learned and propose a different probe or request help. Do not invent an iteration count or interpret “iterate” as unlimited authority.

## Plan, act, verify, accept

1. Identify the intended outcome, scope, constraints, and observable acceptance criteria. When ambiguous, read [define-outcome](../define-outcome/SKILL.md). Keep the acceptance contract in the authoritative artifact or inline for small work; distinguish agreed criteria from proposals and name how each will be verified. Clarify only decisions that cannot be established from available evidence.
2. Explore relevant code, callers, tests, and conventions. Stop when the change location, affected contracts, and verification approach are known. Use `research` for a remaining question needing deeper evidence; do not turn routine exploration into a research project.
3. Plan proportionally. A small task needs a short sequence; complex or restartable implementation can use `write-exec-plan` to resolve consequential technical unknowns through prototypes before drafting verifiable phases. For developer discussion, use `show-me` to present the proposed behavior, contracts, tradeoffs, and decisions needed. Mark proposals separately from accepted decisions.
4. Execute an authorized slice. Update the plan when evidence refutes an assumption. Do not treat a plan or reviewer suggestion as permission to expand scope.
5. Run required repository checks and checks that exercise the requested behavior. For live bugs, reproduce and verify on the relevant surface/profile. Record commands, outcomes, and limitations; source inspection is not runtime verification.
6. Compare results with the agreed acceptance contract and original user need. Criteria are pending until evaluated; report evaluated criteria as passed, failed, blocked, or awaiting human review, with evidence. Finish only when required criteria are supported, including human acceptance when required. Otherwise correct the work or report partial completion. Passing tests alone does not establish that the intended problem was solved; do not weaken the contract to match the implementation.

Research completes when evidence answers its question or the missing evidence is identified. A discussion completes when the requested decisions are recorded or remaining disagreements are explicit. Neither implies implementation approval.

## Pause for human review

Pause before dependent work when the user asks to review an artifact or response before proceeding, when choosing between proposals requires their judgment, or when the acceptance contract requires human approval. A request to draft a plan, prototype, or proposal for discussion ends with that deliverable for review unless the user also authorizes the next step. Do not impose a new approval gate on ordinary completed work whose scope and acceptance are already clear.

Before requesting review, finish the artifact to the agreed review depth: check its facts, links, relevant rendering or interactions, and label unverified claims and open questions. Do not ask the user to review unfinished scaffolding unless rough work was requested. If readiness is blocked, explain the limitation and the narrower question they can answer.

Present the artifact or response with enough context to decide:

```text
Review: path/link or the response below; version/iteration when relevant
Decision needed: the specific question or approval requested
Evidence: focused visual, example, or verification result
Options / recommendation: only when a choice is needed
Waiting on your answer: dependent actions that will not proceed yet
Independent work: only if already authorized and unaffected by this decision
```

Then end the turn and wait for the user's response. Do not announce a pause and continue implementing, publishing, dispatching dependent workers, or silently revising the review target. For delegated work, stop new dependent dispatches and use the harness protocol to bring affected running workers to a safe checkpoint; preserve partial work. Independent work may continue only when already authorized, it cannot prejudice the decision, and the user did not ask for a full pause. State it explicitly.

Use chat by default. Open Plannotator or another review surface only when requested or covered by an established preference, following its skill. Silence, timeout, or closing a review surface without a decision leaves review pending. A tool returning successfully means the interaction completed, not that the user approved. Read the actual decision and notes.

On feedback, identify whether the user approved, requested revisions, rejected the direction, or asked a question. Answering a question is not approval. A brief “yes” or “go” is sufficient when its scope is unambiguous; ask when multiple proposals make it unclear. Approval applies to the reviewed version and stated next actions, not unrelated changes. Material changes to reviewed behavior, scope, or acceptance need another review unless the user explicitly delegates that decision; routine corrections within accepted feedback do not need repeated approval.

For durable work, record review pending, the exact artifact/version, decision needed, authorized independent work, and next action in the entry artifact. Preserve this state across compaction. After approval, record the decision and resume only the authorized dependent steps. Do not claim full acceptance while required human review remains pending.

## Route feedback

- Implementation defect: revise the affected code and rerun the relevant checks.
- Refuted assumption: update the authoritative plan or research finding, including evidence and consequences.
- Changed requirement or disputed decision: record the alternatives and ask the user or designated decision owner before proceeding beyond approved scope.
- Missing environment, access, or authority: report the blocker and next concrete action; do not silently weaken verification.
- Developer review: incorporate accepted feedback into the artifact and plan. Keep unresolved comments visible with their decision owner when known; do not claim consensus from silence.

Revise stale diagrams, pseudocode, and acceptance criteria when decisions change. A recurring failure may justify a narrow skill correction or executable check; propose it with the observed failure. Do not automatically promote task history into global policy.

## Checkpoint before context is lost

Update the entry artifact after a meaningful decision, discovery, verified slice, pause, or ownership transfer. Do not wait for a compaction warning. Preserve:

- Objective, scope, constraints, and granted/withheld permissions.
- Current acceptance contract or its authoritative link, evidence status, proposed changes, and the rationale and approval source for accepted changes.
- Current status and the next concrete action, including a command when known.
- Current iteration: explore/refine/finish, question or hypothesis, experiment/change, observations, keep/revise/reject decision, and next question. Preserve reasons rejected approaches failed when that prevents repeating them.
- Decisions with rationale; rejected alternatives and reasons; open questions and disagreements.
- Evidence links, dates or revisions, and whether each consequential claim is observed, inferred, or unverified.
- Completed and remaining work; exact verification results and failures.
- For implementation: checkout path, branch/revision, dirty files and ownership, active processes or external operations, and safe retry/recovery notes. Never replay an external write solely because its result was lost.
- Required skill paths and links to authoritative artifacts/issues. Exclude secrets and unnecessary personal data.

Keep the current state concise. Preserve historical decisions only when their rationale prevents repeating mistakes. Do not copy transcripts or duplicate large source material.

### Checkpoint format

Use this compact shape when no existing plan, research, or issue template owns the record. Update the existing entry artifact rather than creating another progress file. Link information already maintained elsewhere.

```text
Goal / scope / permissions:
Acceptance: authoritative contract and current evidence status
Read first: source artifacts and required skills
Current iteration: question → experiment/change → observation → decision
Decisions: accepted choices and reasons; rejected approaches worth remembering
Progress / evidence: completed, remaining, actual checks and sources
Open: disagreements, blockers, missing evidence or authority
Resume: next concrete action; what to reconcile before acting
Runtime, if applicable: cwd/branch/revision; dirty-file ownership;
  active operations; safe retry/recovery notes
Updated: date and relevant revision
```

For a read-only discussion, omit runtime fields that do not apply. Do not omit unresolved disagreements merely to make the record shorter. A handoff note may contain only the entry link, changed state, and next action when the linked record already supplies everything else.

## Resume and hand off

1. Read the entry artifact, applicable repository instructions, and required skills. Follow its source links for the next step.
2. Check current worktree, tracker, and relevant external state against the checkpoint. Mark stale claims and reconcile changed assumptions before acting. Stored plans are not evidence that a command ran or a deployment succeeded.
3. Preserve unrelated changes. If ownership or an in-flight mutation is uncertain, stop the dependent action and resolve it.
4. Continue the next authorized step; checkpoint corrections as they are discovered.

Use one authoritative home per concern: product requirements belong in the PRD when one exists, technical choices in the design/ADR authority, research owns evidence, plans own overall execution sequencing, and issues own assigned scope/status. Small-task decisions may remain in the work index. Follow [context-routing](context-routing.md) for durable same-workspace decisions. When ownership moves to a remote tracker, mark the local record promoted/handed off with the URL; avoid duplicate progress lists. Developer-facing artifacts belong in repository-standard locations; local paths are not shareable links, so publish or attach only with permission.
