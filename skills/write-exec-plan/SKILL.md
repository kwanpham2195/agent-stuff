---
name: write-exec-plan
description: "Write or maintain a plan for complex work across phases or PRs. Resolve consequential technical unknowns through prototypes before defining implementation checklists and their evidence."
disable-model-invocation: true
---

# Write an execution plan

The deliverable is a restartable plan an owner can execute and a reviewer can audit from evidence. Resolve consequential technical unknowns before committing to implementation phases. A planning request ends with the plan for review; it does not authorize production implementation.

Follow repository `AGENTS.md`, `PLANS.md`, and required templates first. Use [context-routing](../references/context-routing.md) when selecting or resolving the artifact home; reuse a workspace mapping already established in this session. For drafting or material restructuring, read [exec-plan-guide](references/exec-plan-guide.md). For execution updates or resumption, use the existing plan and the relevant checkpoint/resumption sections of [work-lifecycle](../references/work-lifecycle.md). Read its review-pause section when handing back a plan for approval. Preserve explicit-only invocation.

## Establish the outcome

- Use this skill when requested or when the user agrees substantial work needs a plan. If the change is small with an obvious approach, explain that an inline sequence is sufficient and stop unless the user still wants a durable plan.
- Reuse the agreed outcome, constraints, and acceptance criteria. Use [define-outcome](../define-outcome/SKILL.md) for missing product intent. Ask about preferences that experiments cannot settle.
- Inspect relevant implementation, callers, tests, conventions, prior decisions, and verification commands. Identify the contracts and likely change boundaries. Use [show-me](../show-me/SKILL.md) for a concrete sketch when it helps review.
- Record checkout/revision, dirty-work ownership, granted actions, and the intended execution workflow. Planning does not authorize branches, commits, deployments, external writes, or delegation. Use [delegated-execution](../delegated-execution/SKILL.md) only when delegation is authorized and independent exploration earns its cost.

## Prove the uncertain parts first

1. List the consequential technical questions that could change the design, phase boundaries, or acceptance criteria. Reuse sufficient existing evidence; do not manufacture a prototype for a settled question.
2. For each unresolved question, define the smallest experiment, pass/fail observation, resource or time boundary, and how each outcome changes the plan. Record this before running it. Prototype feasibility, integrations, state behavior, or performance where source inspection cannot establish the answer.
3. For a state-model walkthrough or UI exploration, use [prototype](../workflow/prototype/SKILL.md). For other technical questions, use a small runnable probe in the relevant environment; an HTML demonstration cannot establish backend integration or performance. Keep the probe disposable and identified as experimental. Use scratch state and authorized locations, and ask before any action outside current authority.
4. Run the experiment and capture its actual result. Record the question, command/environment, source revision and branch when applicable, artifacts, verdict, limitations, and resulting decision. Capture screenshots or recordings when an interaction is the evidence. Do not create a branch or commit merely to fill an evidence field.
5. If evidence refutes the approach, revise it and probe the remaining question. Stop when the question is answered, a stated bound is reached, or further attempts yield no new evidence. Seek a product decision or missing permission when required.

Do not postpone unresolved foundational questions into ordinary implementation phases. If a probe is blocked, return a clearly marked blocked or provisional plan with the missing evidence and next action. Dependent implementation remains blocked; independently supported phases may be described. Prototype success establishes only its stated finding. Carrying prototype code into production requires explicit approval and production verification.

## Draft evidence-backed phases

Use the guide's skeleton after the prototype findings establish the route. One phase or PR delivers one independently verifiable outcome. A phase need not be a PR unless branch/PR work is in scope.

- Name dependencies, affected paths/contracts, concrete build steps, observable results, and evidence for each checkbox. Split by outcomes rather than file count. State whether dependencies must complete first or may use an explicitly authorized stack.
- Include automated checks, live verification, and performance verification for every phase. Specify commands/actions, environment, artifact location, and pass predicates. An inapplicable category needs a concrete rationale; missing access is blocked verification. Follow required repository gates.
- For interaction changes or live bugs, verify on the actual surface/profile with the selected control skill. Use the user's browser/TUI/native tooling rules. Choose scenarios for the changed behavior and meaningful failures; do not invent a fixed lane count or model requirement.
- For performance-sensitive work, specify the metric, baseline, comparable probe, and numerical failure threshold. Measure the baseline before implementation where feasible. If trunk lacks the feature, use absolute budgets for the added work and the user-visible end state; do not compare unlike scenarios with a ratio. Mark unmeasured baselines pending.
- Interaction changes require human review of appropriate screenshots/recordings before acceptance or merge. Name other required decision gates and who clears them. For phases without a human gate, state why none is needed.
- Include stop/recovery conditions for risky or non-repeatable work. Preserve repository rules and authority for commits, pushes, merges, and compatibility or migration work. Name the execution workflow and owner; a checklist cannot grant permissions.
- Keep the body actionable. Put prototype findings, alternatives, risks, and reading links in the appendices. Link design decisions to their authority. If issues own assigned scope/status, link them rather than maintaining a competing status list.
- Give each phase a short read-first set that identifies its accepted criteria/decisions, dependency evidence, relevant prototype verdicts, required skills, and code entry points. Follow [bounded working context](../references/work-lifecycle.md#keep-working-context-bounded) for evidence placement and checkpoint timing.

## Check and hand back a new or materially revised plan

Run the guide's review checks. Confirm commands, paths, dependencies, prototype evidence, and acceptance coverage against the sources. Report checks actually performed; structural review does not establish that the proposed implementation works.

Return the plan path, phase order/dependencies, review-gated phases, prototype findings, unresolved evidence, and validation result. Request approval for the proposed plan and name the next action that waits. Record review-pending state and end the turn. Existing explicit execution authority may be resumed only after any requested review gate is cleared; creating the plan does not supply that authority. Do not arm a goal, schedule audits, or spawn execution owners from the planning request.

## Maintain during authorized execution

- Follow [resume and hand off](../references/work-lifecycle.md#resume-and-hand-off) and [checkpoint before context is lost](../references/work-lifecycle.md#checkpoint-before-context-is-lost). Update the existing plan; check a phase box only when its stated evidence exists.
- When an assumption fails, return to a bounded experiment and revise affected phases. Keep accepted and proposed decisions distinct; obtain renewed approval for changed scope, acceptance, or user-owned decisions.
- Continue through authorized phases without asking between every step. Stop at failed gates, missing authority, unresolved decisions, or human review. Link delegated evidence through the approved orchestration workflow.
- Finish by mapping delivered behavior to acceptance criteria and recording residual gaps. Close only when required evidence and human acceptance exist. Keep partial or handed-off plans accurate.
