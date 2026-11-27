---
name: typescript-coding-standards
description: Engineering rules specific to TypeScript and Effect, layered on the shared coding standards. Use when writing, changing, or reviewing TypeScript or Effect code, or when another skill needs these standards.
disable-model-invocation: true
---

# TypeScript and Effect coding standards

Start with the [shared workflow and reference chooser](../coding-standards/references/workflow.md) and apply every shared reference it triggers. This skill is a plain reference outside the language router, so loading it on its own pulls in the shared rules without looping back.

Then read in full each file below that matches the work.

| Work involves | Read |
| --- | --- |
| Comments, exported symbols, public text | [JSDoc](references/comments-and-jsdoc.md) |
| Environment, resources, time, randomness, globals | [configuration](references/configuration-and-resources.md) |
| IDs, units, constrained values, inputs, lifecycle states | [domain types](references/domain-types-and-state.md) |
| Effect code | [Effect](references/effect.md), which indexes its branches; check APIs against the installed package |
| Alchemy infrastructure and runtime composition | [Effect Alchemy](references/effect-alchemy.md) |
| Expected failures and absent values | [errors](references/errors.md) |
| Imports, exports, file names, helper placement | [imports and files](references/imports-exports-and-files.md) |
| Lint configuration, custom rules, cleanup tools | [lint policy](references/lint-and-policy.md) |
| Who owns what: services, helpers, dependencies, complexity | [modules](references/modules-services-and-adapters.md) |
| Untrusted or serialized input, schemas, parsers | [parsing](references/parsing-and-schemas.md) |
| Databases, caches, ORMs, stored records | [persistence](references/persistence.md) |
| Secrets, personal data, telemetry | [sensitive data](references/sensitive-data-and-observability.md) |
| Tests, inference checks, behavior verification | [testing](references/testing.md) |
| Type signatures, mutation, assertions, compiler flags | [TypeScript safety](references/typescript-safety.md) |
| Async work, retries, transactions, resuming, compensation | [workflows](references/workflows-transactions-and-idempotency.md) |

Finish and report evidence under the shared workflow. For TypeScript that includes inference of public types, complete error and Effect requirement channels, useful JSDoc, and a reason for every abstraction and cast. Keep this skill explicit-invocation only.
