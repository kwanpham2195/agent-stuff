# Work lifecycle

Use this contract for work that needs planning, review, multiple sessions, transfer to another owner, or two unsuccessful corrections of the same issue. Also load it before substantial handbacks or consequential recommendations, and when the user asks to understand before hearing a recommendation. Loading it alone requires no saved artifact. It applies to the main agent and delegated workers. Repository instructions and the user's authorization determine permitted actions.

## Sections

| Read when | Section |
| --- | --- |
| Choosing when to act or ask | [Collaboration defaults](#collaboration-defaults) |
| Resuming or acting under a role | [Role applicability and resumption](#role-applicability-and-resumption) |
| Asking the user a question or decision | [Human contact and direct steering](#human-contact-and-direct-steering) |
| Picking inline, durable or tracked work | [Choose the smallest mode](#choose-the-smallest-mode) |
| Deciding whether to save a work record | [Recognize when to save](#recognize-when-to-save) |
| Saving memory at closeout or correction | [Preserve reusable project knowledge](#preserve-reusable-project-knowledge) |
| Limiting what context to load | [Keep working context bounded](#keep-working-context-bounded) |
| Explaining an outcome or change | [Explain with visuals](#explain-with-visuals) |
| Revising an experiment, direction or result | [Iterate according to the question](#iterate-according-to-the-question) |
| Running plan, act, verify, accept steps | [Plan, act, verify, accept](#plan-act-verify-accept) |
| Reporting results and choices | [Help the user judge the result](#help-the-user-judge-the-result) |
| Saving an implementation outline or plan | [Saved planning artifacts](#saved-planning-artifacts) |
| Handling several items in one conversation | [Switch items in a mixed conversation](#switch-items-in-a-mixed-conversation) |
| Requesting review and waiting for a decision | [Pause for human review](#pause-for-human-review) |
| Acting on feedback | [Route feedback](#route-feedback) |
| Keeping decisions and evidence | [Checkpoint before context is lost](#checkpoint-before-context-is-lost) |
| Setting up local context Git history | [Initialize local context history](#initialize-local-context-history) |
| Committing local context changes | [Commit local context changes](#commit-local-context-changes) |
| Resuming or handing off existing work | [Resume and hand off](#resume-and-hand-off) |

## Collaboration defaults

Resolve factual gaps yourself. For ambiguous intent, give plausible interpretations and recommend one before acting on the uncertain part. Make routine choices within scope and ask about consequential changes to behavior, architecture or scope.

Show an early sketch for direction and a coherent proposal for approval. Say what feedback you need. Group related choices with consequences and a recommendation. Ask sequentially if answers depend on each other.

For subjective work, revise once per feedback round. Continue objective fixes until the criteria pass or a decision or blocker intervenes. Clarify which mode applies if unclear. Follow the [review pause](#pause-for-human-review) for the scope of approval. Honor explicit instructions and reuse settled decisions.

## Role applicability and resumption

Work directly with the user unless explicitly assigned a role or resuming one under its saved agreement. Skills, tools, directories, links and history do not assign roles. Only confirmed T3 Code sessions can be assigned as the Desk (experimental `desk` skill), which can coordinate across workspaces. Helpers report to their parent. Task threads report directly to the user alone. When durability is needed, retain the role, outcome, owner, authority and assignment evidence in the owning record or thread.

On authorized resumption, reconcile ownership, restrictions, pending gates and uncertain operations or receipts. Keep the last established authority while resolving uncertainty. Missing transport grants no takeover or duplicate dispatch. Tell the user and pause dependent work. Continue independently authorized work.

Revocation ends future role actions in scope. Reconcile existing workers, pending delivery and ownership before replacement or another consequential action. Confirm T3 identity through [T3 routing](../delegated-execution/references/t3-routing.md#confirm-the-current-session) when T3 operations matter.

## Human contact and direct steering

Ask the user directly in the owner thread, without relays. Use the harness's question tool when it has one, so the host can mark the thread as waiting. Lead with the decision or result needed. Include the exact question, a link and review version, and any supported recommendation and consequence. Keep the gate in that thread and pause dependent work.

Use platform permission and private-secret dialogs where applicable. Never ask for secrets in chat. Asking or completing a dialog grants no additional authority, restart or retry. Follow the user's direct scoped steering within permissions and gates. Pause affected work for material conflicts in authority, safety or ownership.

## Choose the smallest mode

- **Inline:** state the outcome and check, act, and report evidence. Small work needs no plan or research document.
- **Durable:** use one current authority when work must survive context loss. Link existing evidence and plans using [context-routing](context-routing.md). Discussion needs no full ExecPlan.
- **Tracked:** use [issue](../issue/SKILL.md) for requested queueing or assignment. Resolve the destination and scope from the request or an approved default. Drafting grants no implementation, publishing, assignment or status changes.

Recheck the mode at changes of scope or ownership and explain a switch briefly.

## Recognize when to save

Choose durable or tracked work for requested plans, checkpoints, resumptions and handoffs, or when unfinished work, a pending review or costly evidence must survive the session. Use the smallest authorized record and reuse existing owners. For multiple outcomes, follow [projects and bounded work](context-routing.md#projects-and-bounded-work).

During read-only work, save durable findings within the authorized workspace context. Keep other checkpoints inline unless approved. For unregistered workspaces, follow [context-routing](context-routing.md) and ask. Routine lookups, edits and clarification stay inline.

## Preserve reusable project knowledge

For learning-worthy outcomes, link receipts in a compact Outcome section under [improvement records](../retro/references/improvement-records.md). Technical improvements stay within the agreed outcome, write scope and regression gates. Taste, intent, acceptance and expanded authority remain human decisions. `retro` requires explicit authorization.

At closeout, use `agent-memory-repo` to save up to three reusable lessons beyond the repo or record. Report saved links or that there were none in the closeout message. Save lasting corrections and preferences promptly under [global memory](context-routing.md#global-memory). Use [registered workspace memory](context-routing.md#workspace-memory-registration) for project knowledge, or the work record if none exists. These scoped writes need no further approval. Read-only tasks and scheduled runs may not write memory.

Cite current evidence. Distinguish verified facts, observations and proposals. Link authoritative sources and omit transient, duplicate, sensitive or easily rediscovered details. Follow registered update and deletion limits. Commit separately in the memory repo. If dirty, unavailable or disputed, preserve the finding in the work record and report why memory is pending.

## Keep working context bounded

Resolve the workspace and owner through [context-routing](context-routing.md). Load current criteria, dependencies, prototype findings, instructions and relevant code. Follow links to answer named gaps. Use adequate excerpts as evidence. Reopen changed, insufficient or consequential sources as needed. Stop once the change location, affected contracts and checks are known.

Keep large evidence in its authorized home and link it. Use isolation only when authorized and worth the cost. Give children only the context needed for their task. Follow [delegated-execution](../delegated-execution/SKILL.md) for briefs, scoped sources, ownership and evidence. The parent synthesizes results and evaluates acceptance.

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

Name what each iteration should learn or improve, what will decide it, and what remains provisional. Do not interpret “iterate” as unlimited authority.

- Explore an idea with the smallest authorized experiment. Verify the learning goal and label omitted production checks.
- Refine an agreed direction using evidence or feedback. Check changed behavior and affected contracts.
- Finish against accepted criteria and required checks.

Distinguish proposed from accepted changes. Pause for missing decisions, changed scope, agreed limits or repeated attempts without new evidence. After two failed corrections, check assumptions, missing context and inadequate evidence using [diagnostics](../ayo/references/diagnostics.md). Honor stricter limits. Report what was learned and propose a different probe or ask for help. Start a fresh session only when needed, authorized and handed off. Treat experiment results as evidence for the question tested.

## Plan, act, verify, accept

Beyond trivial edits, `rpi` and its [local rules](rpi-local.md) own research, design, planning and implementation. Apply the verification and acceptance steps below to `rpi` too. Read [Writing reviewable artifacts](reviewable-writing.md) before drafting or materially revising human-facing artifacts.

1. Agree the outcome, scope, constraints, observable criteria and evidence. Use [define-outcome](../define-outcome/SKILL.md) for ambiguity. Keep criteria inline or in their authoritative artifact, with proposals clearly marked.
2. Inspect relevant code, callers, tests and conventions. Stop when the change, contracts and checks are understood. Use `rpi` research for consequential gaps.
3. Plan to the scale of the change. Use a short sequence or code sketch for small work. Resolve material unknowns through `rpi` research or an authorized [prototype](../prototype/SKILL.md) before planning dependent work. Use [show-me](../show-me/SKILL.md) for behavior, contracts, tradeoffs and decisions. Follow the saved planning rules below.
4. Execute an authorized slice. Revise the plan when evidence refutes it. Confirm scope changes with the decision owner.
5. Run required repository and behavior checks. For live bugs, reproduce and verify on the relevant surface and profile. Record commands, results and limits. Distinguish source evidence from runtime proof. If a consequential decision trail is doubtful, check entries against the authorized transcript and record missing pivots or corrections.
6. Compare results with the original need and agreed criteria. Passing tests alone do not establish that the intended problem was solved. Report each evaluated criterion as passed, failed, blocked or awaiting human review, with evidence. Finish only when all required evidence and acceptance are present. Otherwise correct the work or report partial completion. Keep the agreed contract when implementation falls short.

Close research when its scope and acceptance are met. Missing evidence can answer a bounded research question. Otherwise report the blocker. Close planning or discussion when requested decisions are settled and recorded. Keep explicit disagreements in review (`needs-review` for legacy records). Completion grants no implementation authority.

### Help the user judge the result

Follow the user's stated writing and presentation preferences, such as those in `USER.md`. Lead with the conclusion and the user's one decision, if any. Use `Decided for you` for material choices within your authority. “Decided for you” never replaces approval for a decision outside your authority. Give at most five key points connecting evidence, limits and gaps to the result. Link supporting details or provide them on request. Commands, hashes and counts go in the details layer unless a check failed. Surface failed checks and any details required by the task or decision.

For real choices, show the strongest supported objection and what evidence could change the recommendation. If the user asks to understand first, explain the evidence and hold the recommendation. Invite one prediction only when they want to test their reasoning. Compare it with evidence. Answer routine requests directly and omit teaching questions from unattended runs. If asked whether the help worked, assess whether it exposed an assumption or changed a decision.

### Saved planning artifacts

Use the `rpi` outline template and show-me views when saving or materially revising an implementation outline or plan, unless the user or repo requires another format. Reuse the owning artifact. Rough discussion and inline sketches need no template. Using a format grants no workflow, metadata, stage credit, child role or execution authority.

Show exact code shapes in each phase's Change Outline when decisions support them. Before delivering, check required metadata, sections and phase headings. Ground proposed paths and code in evidence. Name the check environment, runnable checks and expected results. Mark unavailable checks, unresolved choices and their dependent actions. Preserve conditional sections that apply and retain technical detail needed for review. Label the draft, blocked or ready state according to evidence and review.

### Switch items in a mixed conversation

Name the current item and authoritative artifact. Scope answers to the question and version they resolve. Before switching, incorporate accepted decisions where authorized. Keep unresolved questions, waiting actions and authority with the owner. If the owner update lacks authorization, preserve the scoped decision where permitted and flag the pending update. Rough discussion needs no new thread or record.

On return, reconcile the item's version, decisions and permissions. A brief yes settles only the unambiguous question asked. Ask before dependent action when its scope is unclear.

## Pause for human review

Pause before dependent work when the user asks to review an artifact or response before proceeding, when choosing between proposals requires their judgment, or when the acceptance contract requires human approval. A request to draft a plan, prototype, or proposal for discussion ends with that deliverable for review unless the user also authorizes the next step. Do not impose a new approval gate on ordinary completed work whose scope and acceptance are already clear.

Before requesting review, finish the artifact to the agreed review depth: check its facts, links, relevant rendering or interactions, and label unverified claims and open questions. Do not ask the user to review unfinished scaffolding unless rough work was requested. If readiness is blocked, explain the limitation and the narrower question they can answer.

Present the artifact or response with enough context to decide:

```text
Review: path/link or the response below; version/iteration when relevant
Decision needed: the specific question or approval requested
Evidence: focused visual, example, or verification result
Options / recommendation: only when a choice is needed
Would change this: evidence that would change the recommendation and the smallest check, when applicable
Waiting on your answer: dependent actions that will not proceed yet
Independent work: only if already authorized and unaffected by this decision
```

Then end the turn and wait for the actual scoped decision through the human-contact route above. Do not announce a pause and continue implementing, publishing, dispatching dependent workers, or silently revising the review target. For delegated work, stop new dependent dispatches and use the harness protocol to bring affected running workers to a safe checkpoint; preserve partial work. Independent work may continue only when already authorized, it cannot prejudice the decision, and the user did not ask for a full pause. State it explicitly.

Ask through the harness question tool by default. Use chat only when the harness has none. Open Plannotator or another review surface only when requested or covered by an established preference, following its skill. Silence, timeout, or closing a review surface without a decision leaves review pending. A tool returning successfully means the interaction completed, not that the user approved. Read the actual decision and notes.

On feedback, identify whether the user approved, requested revisions, rejected the direction, or asked a question. Answering a question is not approval. A brief "yes" or "go" is sufficient when its scope is unambiguous; ask when multiple proposals make it unclear. Approval applies to the reviewed version and stated next actions, not unrelated changes. Material changes to reviewed behavior, scope, or acceptance need another review unless the user explicitly delegates that decision; routine corrections within accepted feedback do not need repeated approval.

Keep the pending question and exact review version in the owner thread. Once the user answers, record a decision only when it explains a change. Resume only the authorized dependent steps.

## Route feedback

Fix defects and rerun relevant checks. Update refuted assumptions in the owning plan or research with evidence and consequences. Ask the decision owner about changed requirements or disputes before exceeding scope. Report access, environment and authority blockers with the next action. Fold accepted feedback into the artifact and plan. Keep unresolved comments and known decision owners visible. Silence does not establish consensus.

Update stale visuals and criteria. For recurring failures, propose a focused repository check or skill correction backed by evidence. Follow [ayo's suggestion rules](../ayo/SKILL.md#suggesting-a-skill) for optional [correct](../correct/SKILL.md) or [retro](../retro/SKILL.md). Keep lessons under their existing authority and seek approval for user policy changes. Avoid automatic rule additions or unrelated deletions.

## Checkpoint before context is lost

Follow the [work record contract](context-routing.md#work-metadata-and-overview) for retention and commit triggers. Keep pending questions and recovery instructions in the owner thread and recoverable evidence in its authorized home.

### Initialize local context history

On first-time setup, initialize one Git repo at the context root, stage only reviewed files, and never add a remote. The root repo holds the shared tools: `index.md`, templates, hooks, validators and lint settings. Each workspace folder `workspaces/<id>/` then becomes its own private repo, ignored by the root repo. For a new workspace, once the owner approves registering it:

1. Create `workspaces/<id>/index.md` from the root's `templates/workspace.md`, and run `git init` in that folder.
2. Copy the root's ignore rules into the workspace's `.gitignore`, with paths relative to the workspace.
3. Install the shared hooks in the new repo so it runs the same pre-commit checks as the root.
4. Commit the workspace's first files in its own repo.
5. In the root repo, add `/workspaces/<id>/` to `.gitignore` and a directory-hint entry to `index.md`, then commit.
6. If the host organizes work by project, add the context folder to the workspace's project as a tracked folder.

If history is missing later, stop and ask before recreating it.

### Commit local context changes

Standing authorization covers an agent's own context additions under the work record contract. Before editing, find the repo that owns the file: a workspace folder with its own `.git` is a separate repo, so run Git from that folder; everything else belongs to the root repo. Confirm that repo's top level by physical path, check status and note existing changes. Limit edits to owned workspace files and authorized shared files.

Follow [commit](../commit/SKILL.md) for a nonempty staged change. Use `<type>(<workspace>): <summary>` and describe the change that matters on resume. Use `context` for shared templates or rules. Exclude Obsidian state and unnecessary personal data. Leave mixed-owner files and unrelated staged changes untouched until ownership is resolved. Add no remote. If blocked, preserve the record and report the pending commit. Read back uncertain results before considering another attempt. Read the current record on resume and consult scoped history only to explain earlier changes.

## Resume and hand off

1. Start with `index.md`, `decisions/` and any linked task thread through [recall](../recall/SKILL.md). Read the current legacy owner when the record has yet to be converted.
2. Check the current worktree, tracker and relevant external state. Reconcile any status edit with evidence and granted permissions before acting. Ask before dependent work if intent remains unclear.
3. Preserve unrelated changes. If ownership or an in-flight mutation is uncertain, stop the dependent action and resolve it.
4. Continue the next authorized step; follow the work record contract for additions.

Follow [context-routing](context-routing.md#accepted-decisions) for decision ownership and [artifact placement](context-routing.md#place-context-and-artifacts) for promotion or tracker transfers. Research owns evidence; plans own execution sequencing; issues own assigned scope/status. Local paths are not shareable links.
