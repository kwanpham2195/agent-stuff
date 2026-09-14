# Execution plan structure

Use repository templates first. Otherwise copy the skeleton below and fill it with observed facts and proposed steps. Keep the main sections stable on revisions. Add one phase per independently verifiable outcome or PR. Use logical IDs such as P1 until real PRs exist; never invent forge numbers.

An execution box is checked only when its stated evidence exists. Distinguish planned checks from observed results. Required verification must pass; an inapplicable category needs a rationale. Missing access or an untested claim remains blocked or pending.

## Copyable skeleton

```markdown
# <Outcome> plan

<What changes, for whom, the rule it enforces, and phases in order. Under ten lines.>

## How to read this

Each checkbox names the evidence needed to complete it. Prototype findings support the route; production verification remains required. Proposed decisions and pending evidence are labeled explicitly.

Outcome and acceptance contract: <criteria or authoritative link>
Scope and constraints: <included, excluded, affected contracts>
Execution workflow and owner: <real skill/playbook path or direct workflow; who accepts/merges if applicable>
Approval: <proposed/review pending/approved; version and approval source>
Permitted actions: <what is authorized; what requires a separate decision>

## Current state

Checkout and revision: <path, branch/SHA when applicable, dirty-work ownership>
Relevant behavior and entry points: <paths/contracts; observed versus inferred>
Required reading: <repository instructions and authoritative decisions>
<Current → proposed diagram, structural diff, or pseudocode if useful>

## Program checklist

- [ ] Resolve consequential technical questions before dependent implementation is planned as ready. Evidence: Appendix A verdicts and linked artifacts; unresolved questions block their dependent phases.
- [ ] Obtain review of this plan. Evidence: approval source identifying the version and permitted next actions.
- [ ] Reconcile current checkout, tracker, and active operations before execution. Evidence: dated state/checkpoint.
- [ ] Execute phases in dependency order. Evidence: each phase's completion record or authoritative issue link.
- [ ] Compare delivered behavior with the acceptance contract. Evidence: the final outcome below.

Dependencies: <graph or ordered list, including independent phases>
Ownership and file boundaries: <owner per phase, overlaps and sequencing; delegated ownership only if authorized>
Human review gates: <phase IDs and required decision>
Branch/PR mechanics, if authorized: <base, independent versus stacked workflow, required checks, reviewer and merge authority>

## P1: <Deliver one observable outcome>

**Depends on:** <phase IDs or none; completion/merge required before starting>
**Acceptance served:** <criterion IDs or explicit observable criteria>
**Prototype basis:** <Appendix A finding IDs, existing evidence, or no consequential unknowns with reason>
**Read first:** <only this phase's required instructions, accepted decisions, dependency evidence, prototype findings, and code entry points; resolve further links for a named gap>
**Scope and files:** <paths/symbols/contracts; allowed boundary>

### Build

- [ ] <Concrete change in a named location>. Evidence: <diff, file, or other inspectable result>.

### Observable result

- [ ] <User or operator action yields exact screen/state/log behavior>. Evidence: <artifact or observation>.

### Verify automatically

- [ ] Run `<command>` from `<cwd>` for <specific cases and required repository gates>. Pass when <predicate>. Save <result location>.
<Or: Not applicable because ...>

### Verify live

Environment and control: <boot command, readiness check, surface/profile, control skill or actual driver, cleanup ownership>

- [ ] Drive <load-bearing scenario> at <revision>. Pass when <observable end state>. Save <screenshot, recording, trace, or log>.
- [ ] Exercise <relevant failure/regression scenario>. Pass when <predicate>. Save <artifact>.
<Compare trunk/head when that establishes the regression. If trunk lacks the behavior, record that and gate the added behavior and end state. Add scenarios only when they cover a distinct risk. For work with no runtime surface, state why live verification is inapplicable and identify the meaningful artifact inspection.>

### Verify performance

Metric and scenarios: <metric for changed work and user-visible end state>
Probe: <command/procedure and environment; baseline first, interleaved baseline/head measurements for comparable scenarios>
Baseline: <measured value, revision, artifact; or pending and how it will be measured>

- [ ] Run the probe. Pass when <numerical threshold and failure rule>. Save <measurements and revisions>.
<If trunk lacks the feature, set absolute budgets for added work and the end state. If performance is inapplicable, replace this block with a specific rationale.>

### Human review

Gate: <decision owner, interaction evidence needed, and when execution/merge must stop; or none with reason>

- [ ] Present <screenshots/recording or other review artifact>. Evidence: <artifact path and reviewed revision>.
- [ ] Obtain <specific approval>. Evidence: <approval source and version>.
<Omit boxes when no human gate applies.>

### Complete the phase

Stop/recovery: <failure conditions; safe retries; risky operations requiring permission/state checks>

- [ ] Record verification and acceptance at <revision or artifact version>. Evidence: <commands/results and artifact links, including human approval when required>.
- [ ] <Handoff or merge only when authorized>. Evidence: <receiving authority or actual merge SHA; omit if inapplicable>.

## Progress and next action

Updated: <date and revision/artifact version>
Current phase and state: <pending/in progress/blocked/awaiting review/complete>
Actual evidence: <command/action → observed result → artifact → date/revision>
Discoveries and feedback: <finding/source → decision or phase change; unresolved feedback and owner>
Active operations and dirty work: <ownership, state to reconcile, safe recovery>
Next authorized action: <one concrete action; required decision if blocked>
<If issues own phase status, link them rather than copying their status here.>

## Final outcome

Acceptance status: <criterion → passed/failed/pending/blocked/awaiting human review → evidence>
Remaining work and limitations: <gaps or none supported by evidence>
Handoff: <owner/location if transferred>

## Appendix A: Prototype findings

### Q1: <Question that could change the plan>

Hypothesis and decision affected: <what this settles; dependent phases>
Experiment and boundary: <smallest probe, pass/fail predicate, time/resource bound, stopping condition>
Environment and permission: <scratch location, source revision, branch if one exists, allowed side effects>
Command/procedure: <reproducible steps>
Observed result: <actual result, or blocked/not run and why>
Evidence: <logs, artifacts, screenshots/recordings when relevant; date and revision>
Verdict and limitations: <supported/refuted/inconclusive; what this does not prove>
Plan consequence: <selected route, changed phases, or dependent work blocked>
Code disposition: <disposable experiment location; any production reuse requires explicit approval>
<Repeat for each consequential question. When prior evidence suffices, cite it instead of rerunning a prototype. When no consequential unknowns exist, record why.>

## Appendix B: Decisions and rejected alternatives

<Accepted/proposed decision → rationale → approval source or decision owner. Link the design/ADR authority when one exists. Include rejected alternatives and the evidence or constraint that ruled them out.>

## Appendix C: Risks

<Risk → affected phase → detection/mitigation → owner or unresolved authority. Include unavailable verification surfaces and unresolved prototype questions.>

## Appendix D: Links and reading list

<Instructions, source pointers, design decisions, prototype artifacts, execution skills, and tracker links required to continue without chat history.>
```

Replace placeholders and remove template commentary before handoff. State concrete inapplicability reasons instead of filling sections with invented work. A blocked plan may retain explicitly pending facts; it must name the evidence or decision needed and cannot present dependent phases as execution-ready.

## Review checks

Walk the actual plan in dependency order before requesting approval:

1. Can a fresh agent identify the desired result, artifact owner, current state, permitted next action, and acceptance criteria without the conversation? Verify required links and paths exist or mark access blocked.
2. Does every consequential technical unknown have a completed bounded experiment or sufficient prior evidence? For a blocked experiment, are its dependent phases explicitly blocked? Check recorded observations against original evidence; a successful demo does not prove production behavior.
3. Does each phase deliver one observable outcome, stay within named file/contract boundaries, and depend only on prior or independent work? Check the graph for cycles and conflicting concurrent writes.
4. Does every checkbox name evidence? Are proposed commands separated from observed results? Are automated, live, performance, and human-review requirements concrete or explicitly inapplicable? Missing access is not inapplicability.
5. Are live scenarios on the real surface/profile and performance comparisons valid? Are numerical budgets agreed or marked proposed for review? Are artifacts tied to the revision under review?
6. Does the execution workflow exist and respect actual permissions? A plan must not silently arm goals, schedules, delegation, commits, pushes, or merges. Keep product and preference decisions with their owner.
7. Can the next worker recover safely from a partial run, stale check, failed prototype, or review pause? Preserve dirty-work ownership, active operations, unresolved feedback, and the next action.
8. Is the plan free of template placeholders presented as facts? Does it accurately mark proposed, blocked, review-pending, and accepted state? Preserve original evidence and reasons for rejected approaches that would otherwise be tried again.
9. Can the worker start the next phase from its read-first set and the current checkpoint without rereading the entire history? Keep raw evidence in linked artifacts, preserve prototype verdicts and failed approaches, and reuse authoritative tracker state instead of duplicating it.

Report which checks were performed and what remains blocked. These are structural and evidence reviews, not a substitute for running the plan's production verification. During execution, revise the relevant phase and checkpoint when evidence changes; technical decision rationale stays with its authoritative document.
