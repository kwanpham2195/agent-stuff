# Engineering workflow

Read nearest repository instructions, package/tool configuration, architecture docs, runtime/library versions, and local conventions for errors, parsing, dependencies, observability, tests, and files.

1. Trace each caller-visible operation from input through decisions/effects to outcome. Identify governing files/versions, compatible patterns, and incompatible required contracts.
2. Read applicable shared and language references completely. Map every changed input, output, failure, dependency, state, representation, and test to an owner.
3. Confirm public inputs, outputs, expected native failure contracts, and meaningful capabilities before implementation. Preserve domain evidence; keep calculations pure and effect order visible. Check existing owners and the deletion test before adding abstractions.
4. Implement complete changed behavior, including failures, translations, diagnostics, and resource lifetimes, preserving compatible telemetry and unrelated behavior.
5. Verify through public interfaces and required repository gates. Add individual checks only when not already covered. Re-read applicable rules; fix exceptions or report concrete blocking evidence. Compare behavior, recovery, runtime work, and public inference rather than decoder/branch counts alone.

Decision priority: correctness, safety, and debuggability first; apply standards to new code and complete changed behavior; follow compatible local architecture; contain incompatible older contracts at their nearest owner; avoid unrelated migrations; record meaningful trade-offs at their owner or existing decision documentation.

Do not add compatibility aliases, rollout/backfill, dual paths, or deployment sequencing without explicit user intent. An actual required public/API/config/data/security/production contract remains a constraint. Report a blocked local change rather than inventing a weaker standard or broad migration.

## Shared reference chooser

Read all matching references:

- IDs, units, constrained values, inputs, state, transitions: [domain values and state](domain-types-and-state.md).
- External/serialized/persisted input, schemas, type provenance: [parsing and evidence](parsing-and-evidence.md).
- Failures, absence, cancellation classification, translation: [errors](errors.md).
- Ownership, helpers, complexity, interfaces, dependencies: [modules and dependencies](modules-and-dependencies.md).
- Config, resources, import effects, globals, time, randomness, IDs: [configuration and resources](configuration-and-resources.md).
- Databases, caches, ORM records, imports, storage authority: [persistence](persistence.md).
- Concurrency, retries, transactions, redelivery, resumption, compensation: [workflows and idempotency](workflows-transactions-and-idempotency.md).
- Secrets, personal data, logs, traces, metrics, reporting: [sensitive data and observability](sensitive-data-and-observability.md).
- Behavior, public contracts/inference, tests: [testing](testing.md).
- Exports, comments, public text, rendered errors: [documentation](documentation.md).

Complete when applicable shared and language rules are checked, every concern has an owner, new abstractions have existing-owner/deletion-test evidence, checks pass or have concrete blockers, public contracts are documented/tested proportionately, and scope remains authorized. Report changed behavior, exact checks, constraints/exceptions, and unproven claims. This reference does not route to language skills; a standalone language invocation stays in that language.
