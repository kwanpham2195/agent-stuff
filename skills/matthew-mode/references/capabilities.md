# Capability owners

Read this map after selecting a task. Load only the section for the selected capability. The map routes to current owners; it does not enable an explicit-only skill or grant an external operation.

## Diagnostics and visual evidence

For bugs, CPU, heap, runtime, or trace work, follow [work lifecycle](../../references/work-lifecycle.md#plan-act-verify-accept) for diagnostic evidence and verification. Reproduce the original scenario and verify the fix on the same surface/profile using the actual [browser](~/.agents/skills/agent-browser/SKILL.md) or [terminal](~/.agents/skills/terminal-control/SKILL.md) owner. Distinguish observed results from source inference and report blocked runtime proof.

Fix the first place the system went wrong, not the place the symptom surfaced. Ask whether the triggering state is legitimate. If the system may be in that state, handle it where the code broke. If the state should never exist, a guard there hides the bug, so find what produced the state. When a failure appears only after a restart, check persisted state first, such as config, caches and lock files. Search for the same fault elsewhere. Fix every instance within the task's scope and report the rest. If a workaround needs a paragraph-long comment to justify it, fix the code instead. Remove changes made for a hypothesis that runtime evidence refuted. After two fixes that share a premise fail the same gate, write the premise down and test it directly before a third fix.

For a captured trace or heap snapshot, reduce it to queryable rows, one per sample, frame or node, and trace hot frames or retainers to source. A leak diagnosis needs the retainer chain from the leaked object to a GC root. Confirm a cause by diffing captures from before and after the fix. Without that pair, call the cause the strongest hypothesis the capture supports.

When the question is what happens if events arrive in another order, such as a retry after a timeout, two callers at once or a write that lands after the caller gave up, model the flow and check every order with [statechart](~/.agents/skills/statechart/SKILL.md). Use it for that question only. A test answers a mapping, validation or straight-line question better. Iterate in a scratch folder, then store what the skill produced in the owning work item's `evidence/<yyyymmdd>-<slug>/` under [context routing](../../references/context-routing.md#local-work-audience-layout): the spec, config and view module, the generated chart and report, the checker output, the rendered SVG and the command that regenerates them. Add a short README with the question, the results and the assumptions the model makes. Link the bundle from the finding that cites it. When no work item owns the question, choose or create one under context routing. The repository gets none of it. Report the shortest bug path in the code's words, then replay it against the real code, and suspect the model first when the bug does not occur. File the lasting finding as a rule or open question in the repository's existing docs and tests, and add no model to the repository unless the same flow keeps failing. When it does, use [create-formal-verification-skill](~/.agents/skills/create-formal-verification-skill/SKILL.md) to verify that flow's promise and leave a project skill with its covered code and sync commit, and [maintain-formal-verification-skill](~/.agents/skills/maintain-formal-verification-skill/SKILL.md) to keep it true after later changes. Draft their output in the same evidence folder, and ask the user before adding the project skill to the repository, because it needs upkeep. The installed copies of both skills tell you to read a Claude Code adapter file that is not installed. Skip that line, since neither skill uses subagents or tools it maps.

## Planning and design

For a multi-phase or technically uncertain change, read [work lifecycle](../../references/work-lifecycle.md#plan-act-verify-accept) for proportional planning and verification. For a costly design decision, read [write-design-doc](../../write-design-doc/SKILL.md). Use [show-me](../../show-me/SKILL.md) when a diagram, contract, or structural comparison will settle a review question. Do not load all three for a small feature.

For a throwaway experiment about logic or appearance, use [prototype](../../prototype/SKILL.md). For consequential unknowns about design mechanisms, use RPI's research steps to gather missing evidence within approved bounds. An experiment does not authorize production adoption.

## Metric improvement

For repeated improvement of one measured outcome, read [optimize-metric](../../optimize-metric/SKILL.md). Keep its bounds, parent review, and unverified evidence explicit.

## PR maintenance and landing

For PR inspection, bounded fixes, or watch mode, read [pr](../../pr/SKILL.md) and its [maintenance reference](../../pr/references/maintenance.md). Read [landing](../../pr/references/landing.md) only after an explicit landing request. Use the installed `gh-stack` owner for stack topology when available; if it is unavailable, report that capability gap instead of inventing stack operations. Use [write-pr](../../write-pr/SKILL.md) for descriptions and the comment sweep.

## Queue, unattended work, and cleanup

For a parent-owned dependency frontier, read [queue orchestration](../../delegated-execution/references/queue-orchestration.md). For bounded unattended progress, read [autonomous runs](../../delegated-execution/references/autonomous-runs.md). For worktree ownership audits or cleanup plans, read [worktree cleanup](../../delegated-execution/references/worktree-cleanup.md). Launches and cleanup planning follow [delegated execution](../../delegated-execution/SKILL.md) and its model policy. For ready-for-agent packets and lanes, read [agent-pickup](../../agent-pickup/SKILL.md). These references do not authorize deletion, remote writes, or a fallback runner.

## Recall and handoff

For history reconstruction, read [recall](../../recall/SKILL.md) and keep the workspace, topic, and date scope explicit. For a restartable checkpoint, read [work lifecycle checkpoints](../../references/work-lifecycle.md#checkpoint-before-context-is-lost). Verify stored claims against current state before resuming.

## Intake, staged flows and tickets

For an unclear idea or a staged Research-Plan-Implement flow, read [rpi](../../rpi/SKILL.md); its design discussion settles open choices one at a time. To implement a GitHub issue end to end, read [take](../../take/SKILL.md); to file one, read [issue](../../issue/SKILL.md). For a backlog review, read [triage-work](../../triage-work/SKILL.md). The Desk owns intake only under an explicit assignment or reconciled resumption. Ordinary tasks stay direct to the user; this map does not assign Desk duties.

## Commits, upstream source and writing

For commits, read [commit](../../commit/SKILL.md). For upstream dependency or repository source, read [librarian](../../librarian/SKILL.md). For human-facing writing, apply [unslop](../../unslop/SKILL.md) and, for docs, PR text or commit messages, [technical-writing](../../technical-writing/SKILL.md).

## Optional skills for the user

Use this section with the current catalog when choosing a suggestion in a direct conversation. Reading this map does not invoke matthew-mode. Explicit-only skills may be absent from a provider's catalog; read the selected entry to confirm its purpose, availability and invocation policy before suggesting it. A pointer is not permission to run it.

| Current need | Skill the user can request | Expected result |
| --- | --- | --- |
| The task prompt needs sharper methods or proof | [sharpen](../../sharpen/SKILL.md) | A revised prompt, without starting the task |
| The user wants to check the agent's understanding of a long or drifting task | [in-your-own-words](../../in-your-own-words/SKILL.md) | The agent restates the goal for the user to check |
| The last answer is hard to read | [bro](../../bro/SKILL.md) | A short plain-language restatement |
| The user returns and needs what changed plus open calls | [ketchup](../../ketchup/SKILL.md) | Changes since the user's last message and every decision still waiting, with recommendations and risks |
| The same repository mistake keeps returning | [correct](../../correct/SKILL.md) | History review, prevention changes, checks, commits and an enforcement table for repeated mistake classes |
| Session evidence suggests a workflow or rule needs review | [retro](../../retro/SKILL.md) | Recorded findings and proposals; eligible improvements may run within an authorized scope and budget |

These are explicit-only options, not a menu to append to replies. Suggest one for an open uncertainty or decision after completing the authorized work or at an existing decision point. Omit suggestions after routine work with no open uncertainty. State the reason, result and complete text to send, for example: `Use the sharpen skill on this task prompt; leave the task unstarted.` For `correct`, disclose that it changes the repository and name the intended mistake class, for example: `Use the correct skill for the repeated missing tenant filter mistakes in this repository only.` Omit unavailable skills unless the user asked for them. Do not repeat a declined or unanswered suggestion without a new reason.

When you are unsure about the goal, clarify it directly or use required `define-outcome` guidance. When your own answer is unclear, rewrite it. Suggestions do not transfer these duties to the user.

Use plain explicit requests in T3 across providers. Use a slash or dollar invocation only when verified for the current provider. A user-supplied skill attachment is an explicit invocation. Required skills are those selected by applicable instructions or an already authorized workflow; run them directly within their permissions rather than suggesting that the user do your required work.

A suggestion alone creates no question, wait, status change, `next_action` or `brief_attention` item. It grants no execution, new thread, installation, or external action. Helpers, unattended lanes and scheduled runs do not offer these suggestions. Advisor offers follow [advisor consent](../../delegated-execution/advisor.md) and count as the one optional suggestion; a required consent question retains its normal gate.

## Retrospectives

For a session retrospective, read [retro](../../retro/SKILL.md) and load [preference review](../../retro/references/preference-review.md) only when preference evidence is involved. Keep observations, hypotheses, and approved policy changes separate.

## Skill authoring

For creating or revising a skill, use [writing-for-agents](../../writing-for-agents/SKILL.md) to select one skill-creator owner and its validation procedure. Keep the skill self-contained and preserve invocation policy under [skill mechanics](../../writing-for-agents/SKILL-MECHANICS.md).

For reusable project verification, use [create-verification-skill](../../create-verification-skill/SKILL.md) or [maintain-verification-skill](../../maintain-verification-skill/SKILL.md) when explicitly requested or agreed. For approved model setup, use the [delegation model policy](../../delegated-execution/references/model-policy.md); routing does not authorize installations or global model changes.
