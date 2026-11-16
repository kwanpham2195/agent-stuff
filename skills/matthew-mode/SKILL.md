---
name: matthew-mode
description: "Explicit task-scoped workflow router for implementation, investigation, planning, evaluation, and authorized automation."
disable-model-invocation: true
---

# matthew-mode

The user invokes it by name with a task, using the active harness's skill invocation, or an RPI implementation phase uses its playbooks. Apply it to that task only; stop when it completes, the user stops it, or a decision or tool failure blocks it. It does not enable a persistent mode or authorize additional actions.

The explicit-only discovery controls remain in place. A direct instruction to read this router selects its guidance; it does not count as the user invoking it by name or activate explicit-only skills linked below.

For a trivial edit, work inline and run the relevant check; no lifecycle reference, playbook, document, or delegation is required. For larger work, read [work lifecycle](../references/work-lifecycle.md) for scope, proportional planning, acceptance, and pauses. Reuse the current outcome and context entry.

Invoking matthew-mode by name authorizes local context capture for investigations and discussions when the lifecycle's durability triggers apply, including before a review pause. Follow [context routing](../references/context-routing.md): reuse the workspace's owning entry or create the smallest local record, link existing authorities, and keep proposals separate from approved decisions. This permission covers context artifacts while application files remain unchanged unless implementation is authorized. "Chat only; save nothing" or "no writes" disables persistence. For ordinary read-only requests, follow the lifecycle's existing permission to save worthwhile findings in the authorized workspace context; other writes need permission. Reaching this skill through the global instructions adds no context-capture permission. Without a by-name invocation, the existing lifecycle permissions apply.

For larger work, read only the matching playbook:

- [Feature](references/feature.md) when adding or changing user-visible behavior.
- [Refactoring](references/refactoring.md) when improving structure while preserving agreed behavior.

When the work item records a `workflow` (`oneshot`, `rpi`, `prd` or `freeform`), [rpi](../rpi/SKILL.md) owns stage order and artifacts. Use this router's playbooks for guidance inside an implementation stage, not to choose a flow.

For other tasks, use [capabilities](references/capabilities.md) to select the matching owner. Do not load the map for a trivial edit or when the feature/refactoring playbook already covers the task. The map routes to existing owners and preserves their invocation policies.

When the harness has a task list, copy the selected playbook's numbered steps into it verbatim before any task-specific items. Keep a step you skip in the list as `skip: <reason>`.

Use existing repository standards, verification commands, and tool owners. Read linked skills with the harness's file-read tool, resolving paths relative to the containing file. Explicit-only owners still require the user's request or agreement; this router does not enable them automatically. Apply the task's delegation requirements through [delegated execution](../delegated-execution/SKILL.md); this router adds no launch requirement or permission. If a required tool is unavailable or fails, report the missing evidence and stop dependent work; do not substitute another agent runner.

Finish with the result, changed paths, acceptance evidence, and remaining blockers.
