---
name: coding-standards
description: "Use when designing or changing TypeScript or Go code, including Effect and Cloudflare projects. Defines the user's coding policies and routes to topic-specific requirements."
---

These standards apply to TypeScript and Go. For other languages, follow repository precedent unless asked to adapt a principle.

## Required policies

- Parse untrusted, serialized, persisted, and framework-shaped input before core logic; pass refined values inward. A cast is not parsing.
- Encode domain invariants in types, constructors, and transitions. Keep expected failures in typed return channels; reserve throws for defects and boundary translation.
- Keep secrets out of errors, logs, traces, metrics, snapshots, and panic summaries.
- Keep platform bindings and framework types at composition seams or local external adapters. Make dependencies, time, randomness, and ID generation explicit.
- Test observable behavior through module interfaces or real seams. Do not use module mocks or method spies.
- Keep type escape hatches local, justified with `SAFETY:`, and behind precise interfaces. Own every promise by awaiting, returning, collecting, or explicitly handing it to detached-work machinery.
- Add abstractions only to hide complexity, own policy, or translate a real boundary. Follow local conventions where compatible with these policies; isolate existing incompatible contracts at boundaries rather than expanding the change into a migration.
- Do not add backwards compatibility, rollout, backfills, dual-write/read paths, or deployment sequencing without explicit user intent. If a required contract prevents a local change, report the constraint.

## Load the relevant references

Inspect the existing implementation and repository conventions before selecting a pattern or dependency. Read the files matching the touched concerns; this summary does not replace their requirements. Resolve links relative to this skill directory. If a required reference is missing, report it rather than guessing its policy.

- Shared terminology: [VOCABULARY.md](VOCABULARY.md).
- Domain values, invariants, state transitions, optionality, flags: [DOMAIN_MODELING.md](DOMAIN_MODELING.md).
- Expected failures, cancellation, not-found, classification: [ERROR_HANDLING.md](ERROR_HANDLING.md).
- Logs, tracing, telemetry, redaction: [OBSERVABILITY.md](OBSERVABILITY.md).
- Modules, adapters, dependency injection, resource ownership: [DESIGNING_MODULES.md](DESIGNING_MODULES.md).
- HTTP, queue, storage, environment, DTO and runtime-hop parsing: [BOUNDARIES_AND_PARSING.md](BOUNDARIES_AND_PARSING.md).
- Promises, concurrency, retries, transactions, idempotency, detached work: [ASYNC_AND_WORKFLOWS.md](ASYNC_AND_WORKFLOWS.md).
- Tests, fakes, property tests, persistence and runtime verification: [TESTING_AND_VERIFICATION.md](TESTING_AND_VERIFICATION.md).
- Go errors, context, interfaces, goroutines, transactions and toolchain: [GO_CONTRACTS.md](GO_CONTRACTS.md).
- Go names, comments, formatting, imports and declarations: [GO_STYLE.md](GO_STYLE.md).
- TypeScript casts, collections, optionality, exports, comments and toolchain: [TYPESCRIPT_CONTRACTS.md](TYPESCRIPT_CONTRACTS.md).
- Workers, bindings, Durable Objects, Agents, storage and runtime boundaries: [CLOUDFLARE_ARCHITECTURE.md](CLOUDFLARE_ARCHITECTURE.md).
- Effect code: read [EFFECT.md](EFFECT.md) first, then the branches it selects for schema/data, services, configuration, scheduling/retry, caching, streams, HTTP, testing, or Alchemy. Do not load unrelated branches.

Verify changed behavior through the caller-visible seam and required repository checks. Report any policy that could not be applied, the existing contract that prevented it, and the narrower improvement made.
