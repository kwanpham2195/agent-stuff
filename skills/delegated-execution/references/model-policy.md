# Delegation model policy

Explicit user choices for the assignment take precedence. Model selection grants no launch or runtime change.

Versioned [model-policy.yaml](../../../model-policy.yaml) is the sole authority for model preferences. This reference owns permissions, fallback conditions, concurrency, budgets and recovery. Read [resolver usage](model-policy-configuration.md) before dispatch. Changing preferences affects future dispatch only; current conversations, children, resumes and recurring jobs retain their stored contracts.

## T3 Code defaults

For confirmed T3 Code work, resolve general tasks through the difficulty procedure below and helpers/specialists through `t3.roles`. Retain the established account bindings and configured role models/effort. Pi is disabled and must not be selected by default for new work. Explicit Opus requests select Claude Code by default. Retain explicit supported harness choices; reconcile requirements or unavailable selections before dispatch. Outside T3 Code, resolve only the active `direct.<harness>.roles` context.

For an explicit Opus request without a harness choice, construct a complete T3 candidate using the existing `claude-default` binding and the live Claude Code Opus model ID. Preserve explicit effort choices through the native `effort` option; otherwise use the configured Opus effort in `t3.difficulties.hardest`, validated against current native descriptors. Use `direct.claude` only for applicable role defaults, not to replace an explicit model choice. Never carry Codex/Pi options into Claude Code or enable fast mode without a request. Validate the complete candidate through the resolver and check task/project constraints. Model selection grants no helper launch, additional spend or permission.

The prior quota fallback specifically used Pi, which is now disabled. Do not execute that path or silently replace it with Claude Code. Ask the user to confirm a replacement quota fallback before using one. An explicit Opus request selects Claude Code as above and does not itself authorize an automatic quota fallback. Invalid config, unavailable models, stale bindings and project conflicts never trigger fallback. Carry no prior model options and report the actual reason when an authorized fallback is used.

### Resolve task and project choices

Resolve a complete selection in this order: explicit task choice, routed workspace override, approved project default, global. Project requirements constrain every level. Read applicable project instructions and classify existing declarations as defaults, requirements, or unresolved. Supply complete defaults and constraints to the resolver; it does not interpret prose or search workspaces. Block unresolved declarations and conflicts.

Each override replaces the entire selection; there is no field merging. For partial human instructions, construct a complete candidate, retain the provider unless changed, and use live advertised defaults for unspecified model-dependent options. Never carry options blindly from another model. Ask when aliases, account identity, or required defaults are ambiguous. Preferences grant no launch, permission, capability or approval authority.

## Direct harness use

Use the active harness's native discovery and delegation path. Do not switch harnesses because of T3 preferences. Supply current native model/option/operation evidence to the resolver and verify that omitted options start from defaults. Direct adapters require this evidence; their presence alone does not establish native support. See [Claude Code routing](claude-code-routing.md) for that harness's protocol.

## General top-level tasks

Classify bounded research, synthesis and coordination as `task-research`; implementation and broader technical work as `task-implementation`. For each new T3 work item, classify task difficulty as `low`, `medium`, `high` or `hardest` before choosing its task model. Use the item's reasoning, uncertainty and consequences, not conversation length or the parent's model. Report the classification and brief reason; ask only when a consequential ambiguity cannot be resolved from the accepted scope. Resolve with `--difficulty` immediately before an authorized launch and verify returned runtime settings under [apply before dispatch](#apply-before-dispatch). The global `t3.difficulties` mapping owns these defaults; no difficulty is inferred from the current model.

Difficulty is a task default below complete explicit task, workspace and approved project selections. Project requirements still constrain it. The resolver blocks general T3 task selection when both difficulty and an overriding selection are absent. Helpers and specialist reviews/advisors retain their independently chosen role selections; do not pass a parent's difficulty to them or automatically assign the hardest task's model to every helper. A helper's complete explicit choice still takes precedence.

Resolve every new item independently, including mixed difficulties in one long conversation. Record item scope, difficulty, winning source/key and requested/resolved settings with its existing work state or bounded inline contract. A choice or approval for one item never authorizes another. Existing parent and child runs keep their recorded models. Resolution emits a candidate for future execution; it does not switch this conversation. If an item needs another runtime, use only an already-authorized supported launch path or ask for the missing authority; never create a thread, helper or paid probe merely to match a difficulty. Inline work on an existing parent must report its actual runtime separately from the recommended candidate. No automatic quota fallback is authorized by difficulty selection.

These defaults do not override specialist review, specialist advisor, or task-owned subagent policy below. Recurring jobs keep their separately selected provider and model and their current run effort contract. Codex Luna for cron work is not a universal effort assignment. Editing this policy does not change existing threads or scheduler settings.

## Subagents and specialists

Classify task-owned helpers as `exploration` or `implementation`, and specialist assignments as `review` or `advisor` regardless of thread level. Resolve their complete configuration entry for the worker's execution context. For other roles retain configured defaults and report migration coverage; do not invent new assignments.

## Resolve models and roles

- Resolve configured IDs and aliases through the active harness's live catalog. A short catalog is incomplete; use targeted lookup before claiming a model unavailable. Bind logical providers explicitly to current instance IDs and expected drivers; never guess an account or substitute personal/company providers.
- Pi role mapping: exploration = `scout`; implementation = `worker`; review = `reviewer`; advisor = `oracle`.
- Specialist classification is independent of thread level. Recurring jobs retain their own selections and effort contracts.
- Size each brief to the resolved model. `gpt-6.1-terra` often stops with nothing done when a brief has several steps. Give it one step per brief, such as one commit, one draft, one publish or one probe, with exact files and a stop condition. `gpt-6.1-sol` completes multi-file changes, several review fixes or a long review in one brief.
- When an explicit choice puts Terra on work that resolves to Sol, keep Terra and split the work into ordered single-step briefs. Do not send the whole task in one brief.

## Concurrent subagents

Across all workflows owned by one parent session, keep simultaneously running children within these separate role caps:

- Exploration: 2, initially at most 10 minutes each.
- Review: 1, initially at most 15 minutes; only the [code-review exception](#code-review-exception) permits two axis reviewers.
- Implementation: 3.
- Advisor: 1.

Keep at most 3 children running in total per parent session, in addition to the role caps. Count all roles and child harnesses toward this total, by assigned task rather than agent name. Lower task, role, and harness limits and the one-writer-per-checkout rule win. These caps are ceilings, not a delegation budget. Apply the [shared outcome accounting and role exceptions](../SKILL.md#outcome-and-delegation-authority) across parent work, children, retries, corrections, and replacement sessions.

For [T3 exploration nesting](../SKILL.md#t3-exploration-nesting), apply these same caps across the root owner's entire reserved descendant tree, not afresh per child: at most two exploration agents and three total descendants that are active, waiting, or uncertain. A depth-1 helper and its exploration leaf both consume exploration slots. Reserve subtree capacity before dispatch; unknown state holds its reservation. Keep any stricter native per-parent limits as well. All levels share the original effort and launch allowance; depth does not reset it.

For bounded read-only exploration or independent review, resolve the corresponding role for the worker's context. Explicit assignment choices retain precedence. The initial time bounds above consume cumulative outcome effort.

A child the user asks to both review and change work counts as review and implementation. Reserve a slot in each role, count it once toward the total, and allow one writer per checkout, so the parent makes no overlapping edits while it runs. The brief names the paths the child may edit and forbids commits, pushes and installs unless the user allowed them. An explicit model choice from the user replaces both role defaults.

Before launch or resume, reconcile active children against both total and role capacity. Queue excess work until the required capacity is available. Retain a child's slot until it finishes or is confirmed stopped; unknown runtime state, a steering receipt, or a stop request does not release capacity. For a task spanning roles, reserve a slot in each applicable role and count the child once toward the total. Changing fixed concurrency and runtime launch caps needs separate authorization, which an owner budget notification does not supply. Do not evade them by changing models, agent names, or workflows.

Use native role limits where supported. Otherwise, the parent must schedule within these caps and track active children across its workflows. Pi's `globalConcurrencyLimit` caps all children in one workflow. It does not enforce separate role caps or a session-wide total. Do not describe these instructions as native enforcement.

## Code-review exception

An authorized [code-review](../../code-review/SKILL.md) task may run TWO read-only reviewers concurrently, exactly one Standards reviewer and one Spec reviewer. Missing Spec means no Spec child, and the unused slot does not go to another reviewer. All other review work retains the one-reviewer cap. This exception remains within the existing total-child cap of 3, the cumulative task budget, the initial review time limit, lower task and runtime caps, and source permissions. It grants no extra launches, models, configuration changes, edits, independent reviewer messages, or descendant slots. Exploration descendants require the separate T3 nesting contract and its already-reserved tree capacity.

The review task owns dispatch, axis evidence, and reconciliation. The requester retains acceptance. Separate task threads still require an authorized request or standing launch scope. Lower capacity serializes the axes. Missing nonbudget delegation authority or tools prevents dispatch and may leave sequential inline review to the authorized task owner.

Optional adversarial synthesis uses existing evidence, or later independent rounds run one at a time under the normal one-reviewer cap after the axis reviewers finish or are confirmed stopped. It does not add a third concurrent reviewer. For T3 independent rounds, follow [T3 routing](t3-routing.md) with fresh tasks, full prior context, and distinct stable round request IDs.

## Token use

- Keep small lookups inline and small edits with the authorized execution owner. Delegate exploration only for independent substantial questions, within the [concurrent caps](#concurrent-subagents) and remaining budget. Give each child a narrow brief and a concise output contract.
- Another review or correction consumes the same outcome allowance. Advisors retain their separate consent policy.
- Reuse exploration findings during implementation. Avoid duplicate investigations or repeating a review after unchanged code has passed.
- Prefer fresh context for independent exploration and review, with only relevant source pointers and evidence. Preserve context needed for implementation and ongoing advisor dialogue.
- Pi defaults: `globalConcurrencyLimit: 3`, `maxActiveAsyncRunsPerSession: 1`, `maxSubagentSpawnsPerRun: 8`, `maxSubagentSpawnsPerSession: 100`, configured in `~/.pi/agent/extensions/subagent/config.json`. The first two bound concurrent work, and the latter two bound cumulative launches. Ask before raising or overriding these limits. Concurrency alone does not cap total token use.

## Apply before dispatch

1. Check the authorized outcome and source scope and the consumed and remaining cumulative delegation allowance. If no effort or launch reservation exists, the assigning parent sets and records a finite bound, informs the user, and proceeds within otherwise authorized scope and fixed caps. Extensions preserve cumulative usage and follow the same notification rule. For children, check the role capacity above. For top-level tasks, check the authorized conversation scope and the fixed concurrency and runtime limits alongside owner-set launch reservations, and do not apply subagent caps. Read the selected harness's configuration and discover its supported models and thinking and effort controls. Follow its required launch protocol.
2. Run the resolver with the role, execution context, explicitly routed workspace, complete task/project inputs and fresh capability evidence. Retain its winning source/key, input hashes, requested selection and emitted native arguments. Re-resolve if any input changes before launch. Check launch authority and limits separately. Copy native model/options arguments exactly; `{}` must clear inherited options. A prompt does not configure the model.
3. If the model or requested level is unavailable, unsupported, or cannot be selected through the permitted launch path, stop that dispatch and ask before substituting. Do not switch execution modes to work around the limitation.
4. Report role, winning source/key and selected model/options at launch. Run the resolver's runtime comparison on returned metadata. Report mismatch and follow the harness recovery protocol without automatically launching a duplicate. Missing metadata means requested but unverified. This is workflow control, not native enforcement.
5. On resume, check the stored run contract. If it differs from the intended selection and cannot be changed, ask before starting a replacement run.

YAML is the sole preference authority at cutover. The resolver launches nothing. Native configuration and runtime evidence establish whether a request is applied. Future dispatch re-reads configuration without a watcher; existing runs and schedules are never rewritten.
