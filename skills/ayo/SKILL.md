---
name: ayo
description: "Explicit shortcut that maps the user's situation, such as a lost agent, a stubborn bug, a feature, a refactor or a return to old work, to the skill or playbook that handles it."
disable-model-invocation: true
---

# ayo

The user types `ayo` with a situation, such as "ayo, agent seems lost" or "ayo, refactor this". An `rpi` implementation phase also uses its playbooks. Pick the first row that fits, read its owner and apply it to that task only. Stop when the task completes, the user stops it, or a decision or tool failure blocks it. When no row fits, handle the task directly. For a trivial edit, work inline and run the relevant check.

| Situation | Read | Result |
| --- | --- | --- |
| Resuming after compaction, a model or harness change, or a new thread | [recall](../recall/SKILL.md) | Work state rebuilt from records, with stored claims checked against the current state |
| The agent seems lost or states things it cannot back | [recall](../recall/SKILL.md), then cite evidence | Each claim tied to a file and line or command output; the rest marked as guesses |
| The user is back and needs what changed | [ketchup](../ketchup/SKILL.md) | Changes since their last message and every decision still waiting |
| The goal, scope or acceptance is unclear | [define-outcome](../define-outcome/SKILL.md) | An agreed outcome with observable criteria |
| An unclear idea or work with stages | `rpi` | Research, plan and implementation, one open choice at a time |
| Adding or changing user-visible behavior | [feature playbook](references/feature.md) | Six steps from outcome to review |
| Improving structure without changing behavior | [refactoring playbook](references/refactoring.md) | Baseline, sketch, slice and before-and-after comparison |
| A bug, crash, slow path, leak or trace | [diagnostics](references/diagnostics.md) | Root cause with runtime evidence, and the same fault searched for elsewhere |
| Two fixes with the same premise failed | [diagnostics](references/diagnostics.md) | The premise written down and tested before a third fix |
| Events in another order: retries, timeouts, concurrent callers | `statechart`, as [diagnostics](references/diagnostics.md) describes | Every order checked and the shortest bug path replayed against the real code |
| A costly design decision | [write-design-doc](../write-design-doc/SKILL.md) | A design for review |
| A throwaway check of logic or appearance | [prototype](../prototype/SKILL.md) | An answer from a disposable experiment |
| A diagram or contract would settle a review question | [show-me](../show-me/SKILL.md) | The flow, structure or input and output shown |
| Repeated improvement of one measured outcome | [optimize-metric](../optimize-metric/SKILL.md) | Measured, reviewed iterations |
| A GitHub issue to implement | [take](../take/SKILL.md) | The issue implemented, verified and opened as a PR |
| A request or handoff to file | [issue](../issue/SKILL.md) | A local or tracker issue |
| PR fixes, CI or review follow-up | [pr](../pr/SKILL.md) and its [maintenance reference](../pr/references/maintenance.md) | Bounded fixes; [landing](../pr/references/landing.md) only on an explicit request |
| A backlog or stale checkpoints | [triage-work](../triage-work/SKILL.md) | One decision at a time with verified owner updates |
| An unattended run | [Readiness and stop conditions](../delegated-execution/references/autonomous-runs.md) | Verified progress under [delegated execution](../delegated-execution/SKILL.md) |
| The same repository mistake keeps returning | [correct](../correct/SKILL.md) | History review, prevention changes and checks for that mistake class |
| A rule or workflow seems to cost more than it gives | [retro](../retro/SKILL.md) | Findings and proposals, kept apart from approved changes |
| The task prompt needs sharper methods or proof | [sharpen](../sharpen/SKILL.md) | A revised prompt, with the task unstarted |
| Checking the agent understands a long or drifting task | [in-your-own-words](../in-your-own-words/SKILL.md) | The goal restated for the user to check |
| The last answer is hard to read | [bro](../bro/SKILL.md) | A short plain-language restatement |
| Upstream dependency or repository source | [librarian](../librarian/SKILL.md) | A cached local copy to read |
| Creating or revising a skill | [writing-for-agents](../writing-for-agents/SKILL.md) | One skill-creator owner and its validation |
| Reusable project verification | [create-verification-skill](../create-verification-skill/SKILL.md) or [maintain-verification-skill](../maintain-verification-skill/SKILL.md) | A verification skill, when requested or agreed |

Typing `ayo` with a situation counts as asking for that row's skill, including an explicit-only one. Each skill keeps its own rules and permissions. If a required tool is unavailable or fails, report the missing evidence and stop dependent work; do not substitute another agent runner.

When the work item records a `workflow` (`oneshot`, `rpi`, `prd` or `freeform`), `rpi` owns stage order and artifacts; the playbooks guide work inside an implementation stage. For larger work, read [work lifecycle](../references/work-lifecycle.md) for scope, planning, acceptance and pauses. When the harness has a task list, copy the chosen playbook's numbered steps into it before task-specific items, and keep a skipped step as `skip: <reason>`.

Typing `ayo` also allows saving investigation and discussion notes to the workspace context record, under [context routing](../references/context-routing.md), when the lifecycle's durability triggers apply. "Chat only; save nothing" or "no writes" turns that off. Reaching a playbook through `rpi` adds no such permission.

Finish with the result, changed paths, acceptance evidence and remaining blockers.

## Suggesting a skill

In a direct conversation, an agent may suggest one explicit-only skill from the table, such as `sharpen`, `bro`, `ketchup`, `correct` or `retro`, after finishing the authorized work or at an existing decision point. Omit suggestions after routine work with no open uncertainty, and when the skill is unavailable. State the reason, the result and the complete text to send, for example: `Use the sharpen skill on this task prompt; leave the task unstarted.` For `correct`, say that it changes the repository and name the mistake class. Do not repeat a declined or unanswered suggestion without a new reason.

A suggestion is not a question: it creates no wait, status change or pending ask, and grants no execution, thread, installation or external action. An unclear goal is clarified directly, and an unclear answer is rewritten; neither is handed to the user as a suggestion. Helpers, unattended lanes and scheduled runs make no suggestions. Advisor offers follow [advisor consent](../delegated-execution/advisor.md) and count as the one suggestion.
