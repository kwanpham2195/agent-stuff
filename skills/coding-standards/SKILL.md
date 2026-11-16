---
name: coding-standards
description: "Use when designing or changing code in any language. Apply shared engineering standards and the additions for each language touched."
---

# Coding standards

Build correct by construction: preserve evidence, parse meaningful values, expose expected failures through precise native contracts, keep effects behind cohesive owners, and test observable behavior.

Read and apply the [shared workflow and reference chooser](references/workflow.md), including every reference triggered by the changed behavior. Shared references own engineering policy; language skills add native contracts, syntax, libraries, and tooling.

Then load additions for every language touched:

- TypeScript or Effect: [TypeScript standards](../typescript-coding-standards/SKILL.md). Read its files directly; this does not alter its explicit-only invocation policy.
- Go: [Go standards](../go-coding-standards/SKILL.md).
- Mixed changes: load each applicable language's additions and keep prescriptions scoped to that language.
- Other languages: apply shared rules through native precise contracts/error channels and compatible local conventions. Report the precedent followed; do not import TypeScript/Effect/Go syntax or libraries.

Standalone language skills load the plain shared workflow and references without entering this router. Do not re-enter a skill already loaded. Report incompatible required contracts and blocked local changes under the shared workflow rather than weakening policy or initiating an unrelated migration.
