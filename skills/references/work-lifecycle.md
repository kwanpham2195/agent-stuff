# Work lifecycle

Use this contract for work that needs planning, review, multiple sessions, or transfer to another owner. It applies to the main agent and delegated workers. Repository instructions and the user's authorization determine permitted actions.

## Collaboration defaults

- Clarify ambiguous requests before acting on the uncertain part. State the plausible interpretations and recommend one. Investigate factual unknowns yourself; do not ask the user to rediscover information available in the repository or tools.
- "Implement this" permits routine implementation choices within the stated scope. Present consequential alternatives in behavior, architecture, or scope for a decision before committing to one.
- Show an early useful sketch when the direction is uncertain; prepare a coherent proposal when requesting execution approval. Label which kind of feedback is needed.
- "Iterate on this" means one revision per feedback round for subjective design. For objectively verifiable fixes, continue within scope until agreed criteria are met or a decision/blocker requires the user. Clarify which mode applies when unclear.
- Ask a small batch of related decisions with visuals where useful, tradeoffs, and a recommendation. Ask sequentially when an answer determines the next question.
- "Looks good" approves the reviewed artifact. It authorizes implementation only when that broader workflow was already requested and this approval resolves its review gate. If the next action or approval scope is ambiguous, clarify it.

Explicit task instructions override these defaults. Do not repeatedly ask about decisions the user has already settled. Use the human-contact route below for clarification, decisions, and review.

## Role applicability and resumption

Use ordinary direct-user workflow unless the current assignment explicitly establishes a role or an authorized same-task resumption reconciles its saved agreement. Record the role, outcome, accountable owner, granted authority, and evidence of assignment in the existing checkpoint when durable state is needed. Skill discovery, a working directory, available tools, pasted links, and historical notes alone do not assign a role. The Desk is assigned only in confirmed T3 Code sessions. Helpers report to their assigning parent. A task thread reports to the user directly and to no one else.

Distinguish no assignment from an established assignment whose current state is uncertain. On an authorized resumption, preserve the last established ownership, restrictions, pending human gates, cumulative usage, and uncertain operations or receipts while reconciling current authority and state. Missing transport does not dissolve that ownership or authorize duplicate dispatch or takeover. Pause dependent actions and tell the user about the limitation; continue only independent work already authorized. Historical notes may identify what needs reconciliation, not grant fresh authority.

Explicit revocation ends future role actions within its stated scope. It does not prove existing workers stopped, resolve pending delivery, transfer ownership, or reset usage. Reconcile outstanding work before replacement or another consequential action. Confirm T3 session identity separately under [T3 routing](../delegated-execution/references/t3-routing.md#confirm-the-current-session) only when T3 operations are relevant; role assignment is not platform identity.

An assigned [scrum master](../scrum-master/SKILL.md) may send evidence-backed corrections within an owner's existing workflow and authority. A nudge is not a new user decision, approval, workflow selection or ownership transfer. Task owners reconcile it against current instructions and retain execution and state-writing responsibility. Scoped bookkeeping handoffs follow that skill; idle threads do not implicitly hand off ownership.

## Human contact and direct steering

A task thread asks the user directly in its own thread, which T3 shows in the user's inbox. Nothing relays through another thread. Lead the message with the decision or result needed. Give the exact question, a link to the artifact or evidence and the current reviewed revision instead of pasting them, and a recommendation and consequence when supported. Keep the pending gate in the task checkpoint. Pause dependent work; independently authorized work may continue.

Silence, cached text, or a completed tool interaction never substitutes for the user's actual decision. Actual platform permission and private-secret dialogs remain human/tool gates, and secrets never go in chat. Asking grants no source, thread, spend, acceptance, model, or schedule authority, and does not resume canceled or stopped work or retry an uncertain operation.

The user may steer any task thread directly at any time. Follow the user's actual scoped instructions within permissions and human gates, and save consequential decisions in the task's own checkpoint. Material authority, safety, or ownership conflicts still require scoped handling and a pause of affected work.

## Choose the smallest mode

- **Inline:** the scope is small and the relevant context fits comfortably in the conversation. State the outcome and verification approach, do the work, and report evidence. No mandatory document or research phase.
- **Durable:** research, planning, discussion, or implementation must survive context loss. Maintain one current state owner and link existing relevant documents, an ExecPlan, or the user's chosen authority. Follow [context-routing](context-routing.md) to select its home or resume selected context. A discussion checkpoint does not require a full ExecPlan.
- **Tracked:** the user wants work queued or assigned through local workspace issues or a configured remote tracker. Use the `issue` skill's implementation-handoff mode. Destination and scope must be explicit or authorized by a workspace default before creation. Drafting does not authorize publishing, assigning people, implementation, or status changes.

Recheck the save triggers below when scope or ownership changes. Explain a mode switch briefly.

## Recognize when to save

A work item is a bounded outcome or question: a feature, bug investigation, comparison, migration, or design discussion. It can exist before implementation starts. Use [projects and bounded work](context-routing.md#projects-and-bounded-work) for goals spanning several outcomes; keep each outcome's state separate from the project backlog.

At intake and when scope changes, check whether any of these applies:

- The user asks to plan, checkpoint, resume later, queue, or hand off the work.
- Work has unfinished steps that must survive another session or owner.
- A review or unresolved decision pauses dependent work.
- Findings, rejected approaches, or verification evidence would be costly to reconstruct.

When a trigger applies, use the durable or tracked mode above. Reuse an existing entry; otherwise create the smallest authorized work record using context-routing. Do not wait for the user to say "save context" during authorized work. For a read-only request, save findings worth keeping to the workspace context record without asking; offer other checkpoints inline or ask permission to save them. If no registered workspace owns the directory, follow context-routing and ask. A quick lookup, completed small edit, or ordinary clarification stays inline when none of these triggers applies.

Once work is durable, checkpoint at meaningful progress, a new or resolved blocker, review readiness or feedback, an answer or acceptance change, and completion. Checkpoint before a handoff, pause, or end of turn when resume state changed. Read the current owner before writing and reconcile any manual metadata edits. Replace the snapshot and update the [canonical work metadata](context-routing.md#work-metadata-and-overview) and [brief reporting fields](context-routing.md#brief-reporting-fields) as one file checkpoint. Set `updated` only for a meaningful change and `brief_checked_at` only after actual reconciliation. A commit or routine passing gate alone is not a save trigger. If the snapshot is semantically unchanged, skip the write and context commit. File checkpoints do not depend on Obsidian running. Link existing policy, design, and tracker authorities instead of copying them.

The task owner reconciles decisions; the brief only checks reporting consistency. At each checkpoint, compare pending attention with actual answers, approval scope and supporting artifacts. Record answer evidence before removing its stable ask ID; preserve all other unanswered asks, even old ones. Never infer acceptance from silence, archive placement, a helper recommendation or a completed administrative step. Keep status/progress/next action/blocker, attention and the body semantically consistent. If reconciliation is incomplete, do not advance `brief_checked_at` or replace attention with `[]`; preserve the uncertainty so consumers report a Coverage gap. Update only owned records; consolidation/backfill and other owners' work require their own authority.

## Preserve reusable project knowledge

For a learning-worthy outcome, add a compact Outcome section and link receipts under [improvement records](../retro/references/improvement-records.md). This is optional for trivial work and does not duplicate canonical status. Technical improvements may proceed within recorded outcome, finite budget, write scope and regression gates; taste, intent, acceptance and expanded authority remain human decisions. Explicit-only retro discovery is preserved; an explicitly authorized loop may invoke it.

Memory is saved at three moments, using `agent-memory-repo`:

1. **Closeout.** When a task thread sets its work state to `complete`, ask what the next session should know that is not in the repository or the work record. Save 0–3 entries, then add one line to the state: `Memory: <links to the saved entries>` or `Memory: none`. List the saved entries in the final message to the user.
2. **Correction.** When the user corrects an agent or states a lasting preference, save it to global memory right away.
3. **Weekly sweep.** The Friday review lists completed work without a `Memory:` line; the user decides what to save.

The user grants standing permission for these writes within each memory's registered write scope: closeout and correction need no separate approval. Read-only requests and scheduled runs still write no memory, except the weekly [memory dream](context-routing.md#memory-dream), which tidies saved entries and adds none.

Save project knowledge in the workspace's registered memory repo under [workspace memory registration](context-routing.md#workspace-memory-registration). Save personal preferences and lessons that apply across workspaces in [global memory](context-routing.md#global-memory). A workspace without a registered memory repo uses global memory for cross-workspace lessons and keeps project-only facts in its work records.

Cite the source artifact or current repository evidence, and distinguish verified facts from observations and proposals. Link authoritative docs and decisions instead of copying them, and do not promote task-specific findings into global rules. Skip transient status, duplicates, secrets, and cheap-to-rediscover facts. Reconcile outdated entries under the registered memory's update scope and the [global memory approval rules](context-routing.md#global-memory); this closeout procedure grants no additional archival or deletion permission.

Commit memory changes in the memory repo under the skill's workflow, separately from context commits. If memory is dirty, unavailable, or disputed, keep the finding in the work record, write `Memory: pending (<reason>)`, and tell the user.

## Keep working context bounded

- Resolve the workspace and authoritative entry through [context-routing](context-routing.md) before mining history or creating records.
- Load the current phase's outcome, acceptance criteria, dependency results, prototype findings, required instructions, and relevant code. Follow other links only to answer a named gap. Do not reload every phase, transcript, or research artifact on each step.
- Treat sufficient search snippets as already-read evidence; a source pointer alone is only a navigation aid. Return to the source when it changed, a consequential claim needs verification, or the available excerpt is insufficient. Stop exploration when the change location, affected contracts, and verification approach are known.
- Keep large logs, screenshots, experiment output, and worker reports in their authorized artifact locations. Apply the retention test in [Checkpoint before context is lost](#checkpoint-before-context-is-lost); link detailed evidence rather than copying it.
- Before switching phases or handing off, apply the checkpoint contract below.
- Use context isolation only when delegation is authorized and earns its cost. Follow [delegated-execution](../delegated-execution/SKILL.md) for a bounded brief, exact source paths, ownership, and evidence reports. The parent retains synthesis and acceptance; children do not need the full conversation or unrelated phase history.

## Explain with visuals

Use [show-me](../show-me/SKILL.md) proactively when explaining behavior, relationships, failure paths, or structural changes. Lead with the smallest useful flow, structural diff, pseudocode, or concrete example, followed by short rationale. Do not wait for a visual request or a choice requiring approval.

- Feature: show the proposed user flow or input/output before implementing a substantial behavior change.
- Refactor: show current and proposed structure, including contracts that remain unchanged.
- Investigation: show the evidenced failure path; mark inferred or unverified connections and link the supporting evidence.
- Decision: compare options through concrete consequences.
- Completion: show meaningful before/after when a file list would not explain the change.
- Resume: reuse the owning visual and update it when current evidence or accepted decisions change.

Keep simple answers inline. Prefer small inline representations; use HTML, rendering tools, or separate files only when they improve understanding and their use is authorized. A visual creates no additional approval gate and does not replace verification. For durable work, maintain useful visuals in the owning artifact rather than a duplicate document.

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

Continue useful iterations within authorized scope. Pause for missing decisions, a scope change, an agreed time/cost/iteration limit, or repeated attempts producing no new evidence. For stalled work, report what was learned and propose a different probe or request help. Do not invent an iteration count or interpret "iterate" as unlimited authority.

## Plan, act, verify, accept

Beyond a trivial edit, [rpi](../rpi/SKILL.md) owns research, design, planning and implementation phases under [RPI local rules](rpi-local.md). Steps 5 and 6 below still apply to its verification and acceptance; steps 1 to 4 cover work that stays inline.

Before drafting or materially revising a human-facing plan, design, proposal, or review report, read and apply [Writing reviewable artifacts](reviewable-writing.md).

1. Identify the intended outcome, scope, constraints, and observable acceptance criteria. When ambiguous, read [define-outcome](../define-outcome/SKILL.md). Keep the acceptance contract in the authoritative artifact or inline for small work; distinguish agreed criteria from proposals and name how each will be verified. Clarify only decisions that cannot be established from available evidence.
2. Explore relevant code, callers, tests, and conventions. Stop when the change location, affected contracts, and verification approach are known. Use RPI's research steps for a remaining question needing deeper evidence; do not turn routine exploration into a research project.
3. Plan proportionally. A small task needs a short sequence. When code is cheaper to write and review than prose that describes it, a code sketch or the change itself is the plan; saved implementation outlines and plans follow [saved planning artifacts](#saved-planning-artifacts), including in mixed triage/planning conversations. Resolve consequential technical unknowns through RPI research or an authorized [prototype](../prototype/SKILL.md) before planning dependent implementation. For developer discussion, use `show-me` to present the proposed behavior, contracts, tradeoffs, and decisions needed. Mark proposals separately from accepted decisions.
4. Execute an authorized slice. Update the plan when evidence refutes an assumption. Do not treat a plan or reviewer suggestion as permission to expand scope.
5. Run required repository checks and checks that exercise the requested behavior. For live bugs, reproduce and verify on the relevant surface/profile. Record commands, outcomes, and limitations; source inspection is not runtime verification. When a consequential result rests on a decision trail you doubt, such as a checkpoint or attempt log, check its entries against the run's transcript where access is authorized. Confirm that each entry's evidence shows what the entry claims, and record pivots and corrections the trail left out.
6. Compare results with the agreed acceptance contract and original user need. Criteria are pending until evaluated; report evaluated criteria as passed, failed, blocked, or awaiting human review, with evidence. Finish only when required criteria are supported, including human acceptance when required. Otherwise correct the work or report partial completion. Passing tests alone does not establish that the intended problem was solved; do not weaken the contract to match the implementation.

Research completes when its requested scope and acceptance are satisfied. Identifying missing evidence may satisfy a bounded research question; otherwise preserve the remaining blocker. A planning or discussion item completes when all requested decisions are settled and recorded. An explicit unresolved disagreement remains `needs-review`. Neither completion grants implementation approval.

### Saved planning artifacts

When saving or materially revising an implementation outline or plan, read and use the RPI [outline template](../rpi/references/create-structure-outline/references/structure_outline_template.md) and the [show-me views](../rpi/references/show-me.md), unless the user or repository requires another format. Ordinary conversation, rough triage and inline sketches stay lightweight. Reusing a format does not select RPI, add workflow metadata, establish prior stages, require child roles, or grant implementation authority.

Choose depth from evidence and decision maturity. When settled decisions support exact changes, show the exact code shapes in each phase's Change Outline instead of writing a separate plan. Keep unsupported details and consequential decisions explicit as unknowns; a blocked draft does not become ready by being formatted. Preserve required headings and useful technical detail. Reuse the current authoritative artifact and its existing home rather than creating a competing plan.

Before delivering, check the artifact against its selected template:

- Required sections, metadata and phase headings are present; conditional sections match the work.
- Proposed changes, paths and code shapes have evidence; checks are runnable in the named environment and state expected results. Label unavailable verification explicitly.
- Unknowns and pending decisions remain visible, with their dependent actions.
- Readiness matches current evidence, decisions and required review. State draft, blocked or ready truthfully; formatting alone proves neither readiness, approval nor implementation authority.

### Switch items in a mixed conversation

Identify the current work item and its authoritative artifact before planning or interpreting an answer. Apply a scoped answer only to the question and artifact version it resolves. Before switching items, incorporate accepted decisions into the affected artifact and preserve unresolved questions, waiting actions and authority in the existing owner. If an owner write is not authorized, retain the scoped decision in the permitted checkpoint and leave the owner update pending. Do not require a new thread or record for every topic.

When returning, resume that item's artifact and reconcile its current version, decisions and permissions. A decision on one item leaves other items' questions and gates intact; a brief yes resolves only the unambiguous question presented. Ask before dependent action when the intended scope is unclear.

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

Then end the turn and wait for the actual scoped decision through the human-contact route above. Do not announce a pause and continue implementing, publishing, dispatching dependent workers, or silently revising the review target. For delegated work, stop new dependent dispatches and use the harness protocol to bring affected running workers to a safe checkpoint; preserve partial work. Independent work may continue only when already authorized, it cannot prejudice the decision, and the user did not ask for a full pause. State it explicitly.

Use chat through the human-contact route above by default. Open Plannotator or another review surface only when requested or covered by an established preference, following its skill. Silence, timeout, or closing a review surface without a decision leaves review pending. A tool returning successfully means the interaction completed, not that the user approved. Read the actual decision and notes.

On feedback, identify whether the user approved, requested revisions, rejected the direction, or asked a question. Answering a question is not approval. A brief "yes" or "go" is sufficient when its scope is unambiguous; ask when multiple proposals make it unclear. Approval applies to the reviewed version and stated next actions, not unrelated changes. Material changes to reviewed behavior, scope, or acceptance need another review unless the user explicitly delegates that decision; routine corrections within accepted feedback do not need repeated approval.

For durable work, set `status` to `needs-review` and name the decision in `next_action`. Record the exact artifact/version, decision needed, and authorized independent work in the current state body. Preserve this state across compaction. After approval, record the decision and resume only the authorized dependent steps. Do not claim full acceptance while required human review remains pending.

## Route feedback

- Implementation defect: revise the affected code and rerun the relevant checks.
- Refuted assumption: update the authoritative plan or research finding, including evidence and consequences.
- Changed requirement or disputed decision: record the alternatives and ask the user or designated decision owner before proceeding beyond approved scope.
- Missing environment, access, or authority: report the blocker and next concrete action; do not silently weaken verification.
- Developer review: incorporate accepted feedback into the artifact and plan. Keep unresolved comments visible with their decision owner when known; do not claim consensus from silence.

Revise stale diagrams, pseudocode, and acceptance criteria when decisions change. A recurring failure may justify a narrow skill correction or executable check; propose it with the observed failure. Do not automatically promote task history into global policy.

## Checkpoint before context is lost

Follow the timing in [Recognize when to save](#recognize-when-to-save). Replace the existing snapshot in place; do not append dated checkpoints or commit sections. Read the current note first and update its metadata and body as one checkpoint. For each meaningful checkpoint, add one dated entry to `agent/history.md`, newest first, linking the evidence used. Content digests belong in that evidence or history entry. Context Git also preserves earlier snapshots. Keep only information whose omission would change the next safe action, obscure authority, repeat expensive learning, or erase useful rationale. Use Markdown by default and apply [writing-for-agents](../writing-for-agents/SKILL.md). Keep the current state body at most 600 words, and 150-300 for a typical state. Link older detail from the state through `agent/history.md` or its evidence owner. Keep permission, acceptance, and recovery information in the state itself. Exclude secrets and unnecessary personal data. Existing unmigrated histories retain their authority until an authorized migration preserves them.

Preserve the current objective, scope, acceptance authority and status or authoritative link, granted and withheld permissions with approval source, decisions and useful reasons, blocker or unresolved disagreement, and next authorized action. Retain the exact pending review artifact/version and required next-step reading. Link the owning plan, issue, design, research, and required skills rather than copying their content. Distinguish proposals from accepted choices and observed facts from unverified claims. Retain important failed approaches and unresolved limitations with concise evidence links. Keep the latest verification scope, actual result, and tested revision; Git commits do not establish that checks ran. Superseded checks and completed implementation chronology belong in context Git history or their existing evidence owners, not the snapshot.

For implementation, retain checkout/revision and dirty-file ownership when needed to resume safely. Keep process identifiers and external-operation receipts only while active, uncertain, or needed for recovery. Once resolved, replace them with the result and evidence link. Never replay an external write solely because its result was lost. Before a pause or handoff, ensure a fresh reader can find the current status, authority, blocker, next action, and evidence; skip writing when those facts have not changed.

### Initialize local context history

During authorized first-time setup of `~/.agents/context/`, initialize Git at that root without a separate Git-init question. Use the user-approved root if it differs. All workspaces share this repository; do not initialize repositories inside individual workspace or work-item directories. This permission does not authorize creating or registering a workspace, saving read-only work, or adopting unrelated existing files.

1. Resolve the context root's physical path and inspect its Git state before writing. Reuse a repository whose top-level path is exactly that root. If an ancestor owns the directory, a descendant contains a repository, or Git metadata is broken or ambiguous, stop and ask; do not create nested history or repair metadata automatically. Check both `.git` files and directories without following directory symlinks. A failed Git command alone does not prove no repository exists.
2. If the root has no repository and no enclosing or nested repository, run `git init <context-root>`. Preserve existing files. Merge `.obsidian/` and `.DS_Store` into the root `.gitignore` without replacing existing rules; add exclusions for known editor/runtime files before staging. Never add a remote automatically.
3. Review the initial files for ownership, secrets, and unnecessary personal data. Stage only the `.gitignore` changes and context files created or explicitly approved for this setup, using exact paths. Existing unreviewed files stay untracked; ask if mixed ownership prevents a clean commit. Do not stage the entire directory.
4. Create the initial local commit under [commit](../commit/SKILL.md), with hooks enabled and the configured identity. Do not change identity or bypass a failed hook to finish setup. If committing is blocked, preserve the files and report the initialized repository and pending commit.
5. Verify the repository top level, initial commit, ignored editor/runtime paths, and remaining status. For a newly initialized repository, confirm `git remote` lists no remotes. Do not alter remotes on an existing repository. Report unresolved files or failures separately from completed setup.

On later use, follow the checkpoint commit procedure below. If history is unexpectedly missing after prior setup, stop and ask before recreating it.

### Commit local context changes

The user authorizes agents to commit their own context changes in the separate local Git repository at `~/.agents/context/`. After saving changed resume state under [Checkpoint before context is lost](#checkpoint-before-context-is-lost), commit before a review pause, handoff, or end of turn. An unchanged snapshot needs no context commit. This is an agent instruction, not a background watcher.

1. Before editing, check `git -C ~/.agents/context status -sb` and confirm its repository root is `~/.agents/context`, comparing physical paths. For authorized first-time setup, follow [Initialize local context history](#initialize-local-context-history); unexpectedly missing history requires asking before reinitialization. Record pre-existing changes and limit work to the selected workspace and authorized shared context files. Use the approved alternate root when applicable.
2. Inspect the diff for the agent's changes and check for secrets or unnecessary personal data. Stage explicit file paths only. If a file also contains another owner's uncommitted changes, or the index contains unrelated changes, leave them untouched and resolve ownership before committing.
3. Follow the `commit` skill for attribution, staged-diff review, and hooks. Context commit subjects use `<type>(<workspace>): <summary>`, for example `docs(example): checkpoint owner probe`. Use `context` as the scope for shared templates or rules spanning workspaces. Commit only when the staged changes are nonempty. Describe the changed resume state in the message.
4. Verify the commit and remaining status. On failure, preserve the checkpoint and report the pending commit and blocker; do not bypass hooks or silently retry an operation whose result is unknown.

This section governs local context checkpoints. Completed, verified project code and chezmoi source changes follow the global local-commit policy and [commit](../commit/SKILL.md). Do not add a remote, push, amend, change branches, or include Obsidian state, secrets, or unrelated files under this permission. On resume, read the current checkpoint first; inspect scoped Git history only when an earlier decision or change needs explanation.

### Checkpoint format

Use this compact shape when no existing plan, research, or issue template owns the record. Update the current state owner rather than creating another progress file. For new or migrated local work this is the linked `agent/state.md`, not the navigation index. Legacy records keep their current owner until explicitly migrated. Link information already maintained elsewhere.

```text
Goal / scope / permissions: granted and withheld actions; approval source
Acceptance: authoritative contract/owner and current evidence status
Pending review, if any: exact artifact/version; decision; waiting actions
Read first: required next-step source artifacts and skills
Decisions: accepted choices, useful reasons, and approval sources
Evidence: latest verification scope/result/tested revision;
  links to findings, important failed approaches and unresolved limitations
Open: disagreements, blockers, missing evidence or authority
Resume details: what to reconcile before the metadata's next action
Runtime, if needed: cwd/revision; dirty-file ownership; active or uncertain
  external operations and safe retry/recovery notes
```

Use the properties in [work metadata](context-routing.md#work-metadata-and-overview) above this body. Do not duplicate their status, progress, blocker, or next action as separately maintained body fields. Body details explain the evidence and resolution conditions. For a read-only discussion, omit runtime fields that do not apply. Do not omit unresolved disagreements merely to make the record shorter. Update existing fields in place when state changes; do not add a new section per save. A handoff note may contain only the entry link when the linked record already supplies the current state and next action.

## Resume and hand off

1. Read the entry and its linked current state, or the legacy current owner if unmigrated. Read applicable repository instructions and required next-step skills; follow source links for the next step.
2. Check current worktree, tracker, and relevant external state against the checkpoint. Reconcile manual Kanban status edits with evidence and granted permissions before acting. A drag to `active` grants no new permission; a drag to `complete` does not establish acceptance. Preserve unknown historical state as `needs-review` with the confirmation question. If the edit's intent conflicts with evidence or is unclear, ask before the dependent action and retain the uncertainty. Mark stale claims and reconcile changed assumptions. Stored plans are not evidence that a command ran or a deployment succeeded.
3. Preserve unrelated changes. If ownership or an in-flight mutation is uncertain, stop the dependent action and resolve it.
4. Continue the next authorized step; checkpoint corrections as they are discovered.

Follow [context-routing](context-routing.md#accepted-decisions) for decision ownership and [artifact placement](context-routing.md#place-context-and-artifacts) for promotion or tracker transfers. Research owns evidence; plans own execution sequencing; issues own assigned scope/status. Local paths are not shareable links.
