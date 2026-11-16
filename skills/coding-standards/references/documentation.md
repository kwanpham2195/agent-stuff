# Documentation and public language

Document public contracts at their original declaration using the language's native documentation convention. State the sharpest caller-visible fact the signature cannot show. Add detail for constraints, expected failures, effects, ownership, invariants, trade-offs, non-obvious domain rules, and safety justifications. Language additions define exact coverage and syntax.

Document internal behavior when safe maintenance depends on non-obvious intent or invariants. Explain why, not a restatement of code. Keep documentation authoritative at its owner rather than duplicating it at re-exports.

Names, documentation, UI copy, and rendered errors use durable vocabulary appropriate to their audience and ordinary domain phrases readers search for. Internal tickets, migration phases, storage fields, framework mechanics, and planning language stay internal.

Update documentation and changelogs for user-visible changes. Keep lasting design rationale beside owning code or existing decision documentation and follow repository ADR rules.

## Completion

Changed public contracts and non-obvious internal constraints have useful native documentation, audience vocabulary is durable, and user-visible documentation/changelog updates match actual behavior.
