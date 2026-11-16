---
name: typescript-coding-standards
description: Correct-by-construction TypeScript and Effect standards. Use for TypeScript engineering, Effect code, or when another skill needs the user's coding standards.
disable-model-invocation: true
---

# TypeScript and Effect coding standards

Apply the [shared workflow and reference chooser](../coding-standards/references/workflow.md) first, including all triggered shared references. This plain reference does not enter the language router, so standalone invocation loads shared rules without recursion.

Read every matching addition completely:

- Effect code: [Effect](references/effect.md) and all matching branches. Verify APIs against the pinned package source.
- Alchemy Workers, Durable Objects, Workflows, bindings, two-phase composition: [Effect Alchemy](references/effect-alchemy.md).
- Failures or absence: [errors](references/errors.md).
- Secrets, personal data, telemetry: [sensitive data](references/sensitive-data-and-observability.md).
- External/serialized inputs, schemas, parsers: [parsing](references/parsing-and-schemas.md).
- IDs, units, constrained values, inputs, lifecycle: [domain types](references/domain-types-and-state.md).
- Ownership, services, helpers, dependencies, complexity: [modules](references/modules-services-and-adapters.md).
- Database/cache/ORM/durable records: [persistence](references/persistence.md).
- Async work, retries, transactions, resumption, compensation: [workflows](references/workflows-transactions-and-idempotency.md).
- Config, resources, time/randomness, globals: [configuration](references/configuration-and-resources.md).
- Behavior, inference, tests: [testing](references/testing.md).
- Types, signatures, mutation, assertions, compiler settings: [TypeScript safety](references/typescript-safety.md).
- Lint config, rules, cleanup tooling: [lint policy](references/lint-and-policy.md).
- Imports, exports, files, helpers: [imports and files](references/imports-exports-and-files.md).
- Exports, comments, public text, errors: [JSDoc](references/comments-and-jsdoc.md).

Complete and report evidence under the shared workflow, including public inference, complete expected-error and Effect requirement channels, useful JSDoc, and justified abstractions/casts. Preserve explicit-only invocation metadata.
