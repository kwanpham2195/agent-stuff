---
name: writing-for-agents
description: "Use when writing skills, agent instructions, operational notes, or references consumed by agents."
---

Write for a fresh agent with no conversation history. Preserve the actions, inputs, permission boundaries, completion criteria, and references it needs to execute correctly. Remove general explanations only when the remaining instructions are sufficient; familiarity with a concept is not proof the agent will follow the required procedure.

- Give each rule one authoritative home. Prefer executable checks for enforceable constraints and existing configuration for cheaply discoverable facts.
- State the action, trigger, and completion condition. Keep examples only when they resolve ambiguity; remove tutorials, persuasion, repeated checklists, and unsupported claims about model behavior.
- Preserve a consistent execution flow and recognizable result format. For workflows, retain the sequence, decision points, evidence gates, and a compact output shape. For standards, retain contrasting examples where they change interpretation. Templates and examples can reduce uncertainty more than another rule; optimize for reliable execution, not minimum word count.
- Always-loaded instructions and skill descriptions have the highest context cost. Descriptions name distinct trigger cases; avoid synonym lists and generic invitations to load more material.
- Keep common steps inline. Link branch-specific reference with an explicit condition for reading it. Split only when independent invocation or selective loading pays for another file.
- Keep related constraints together. Use familiar terminology; do not invent labels that require their own explanation.
- Preserve personal intent and safety boundaries. Surface contradictions for a decision rather than silently choosing the weaker rule.
- Verify paths, tool names, and references. Treat claimed behavioral improvements as hypotheses until tested on representative tasks; document checks actually run.

For workspace work records, follow [context-routing](../references/context-routing.md#local-work-audience-layout) for audience and authority, and [work-lifecycle](../references/work-lifecycle.md#checkpoint-before-context-is-lost) for state retention. Keep detailed specialist report formats and raw evidence intact; a concise state links them rather than replacing them.

Before accepting a substantial trim, walk through a normal request, an ambiguous or blocked case, and a handoff/resume case when relevant. Check that the reader can select the starting action, branch on evidence, recognize completion, and return the expected result without reconstructing removed guidance. Inspect the before/after text; static metadata validation alone does not establish these properties. Report walkthroughs as instruction checks, not behavioral tests.

For skill maintenance, select one skill-creator owner: the explicitly requested skill, otherwise the active harness's bundled skill-creator when available, otherwise the installed shared skill-creator. Read that owner's instructions and use its validator; do not load another authoring workflow merely because a router also links it. If no owner is available, report that limitation. Read [SKILL-MECHANICS.md](SKILL-MECHANICS.md) for invocation policy, including supported cross-harness fields that a validator may reject.
