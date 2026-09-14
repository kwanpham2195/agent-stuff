# Effect

These defaults target Effect v4.

Load this file when changed behavior is already organized around Effect or uses Effect-specific semantics: Services, Tags, Layers, typed error channels, Schema, Redacted values, Streams, Schedules, Caches, Effect HTTP clients, Effect-aware tests, or scoped resources.

## Source rule

Inspect the project's pinned `effect` package version and source before selecting APIs. Prefer vendored or pinned examples over remembered APIs. Consult current upstream source only when the pinned package does not answer the question.

## Adoption boundary

Do not require Effect adoption for code that is not already organized around Effect. General standards still apply: typed expected failures, boundary parsing, deep modules, real-seam tests, cancellation, observability, and TypeScript contracts.

When a local responsibility is Effect-based, preserve the local Effect style unless it violates a settled standard here.

## Non-negotiables

- A responsibility already organized around Effect continues using the established Effect mechanisms for dependency provision, schemas, and Effect-aware testing.
- Do not introduce parallel constructor-injection, schema, or testing architecture inside an Effect responsibility without a concrete interoperability need or explicit architectural rationale.
- Dependency-bearing modules in Effect architecture use Effect Services/Tags/Layers rather than ad hoc dependency bags.
- Expected failures in Effect-based modules use Effect's typed error channel. Do not convert ordinary domain, parse, authorization, dependency, persistence, or workflow failures into unchecked defects merely because an Effect can die.
- Effect custom errors use the repository's established Effect tagged-error mechanism, such as `Schema.TaggedErrorClass`.
- When Effect is the established schema model, use Effect Schema for refined values and schema-derived domain construction.
- Sensitive values use Effect's Redacted value type in Effect codebases.
- Layers that construct cleanup-requiring resources own acquisition and cleanup.
- Effect-specific version assumptions are checked against installed versions before applying version-specific examples.

## Branch chooser

Read every branch that matches the changed behavior.

| If the change touches... | Load... |
|---|---|
| Data models, schemas, brands, variants, optional keys, decoders, tagged errors | [`EFFECT_SCHEMA_AND_DATA.md`](EFFECT_SCHEMA_AND_DATA.md) |
| Services, module surfaces, Layers, runtime wiring, `Effect.fn`, test Layers | [`EFFECT_SERVICES.md`](EFFECT_SERVICES.md) |
| Runtime config, environment variables, `ConfigProvider`, `layerConfig` | [`EFFECT_CONFIGURATION.md`](EFFECT_CONFIGURATION.md) |
| Retry, repeat, polling, backoff, jitter, rate limits, timeouts, pass loops | [`EFFECT_SCHEDULING_AND_RETRY.md`](EFFECT_SCHEDULING_AND_RETRY.md) |
| Memoization, TTL caches, concurrent lookup deduplication, request batching | [`EFFECT_CACHING.md`](EFFECT_CACHING.md) |
| Streams, event sources, async iterables, queues, pubsubs, pagination, backpressure | [`EFFECT_STREAMS.md`](EFFECT_STREAMS.md) |
| Outgoing HTTP, Effect `HttpClient`, status handling, HTTP rate limiting | [`EFFECT_HTTP_CLIENTS.md`](EFFECT_HTTP_CLIENTS.md) |
| Effect tests, time, sleeps, concurrency synchronization, fakes, property tests | [`EFFECT_TESTING.md`](EFFECT_TESTING.md) |
| Alchemy Workers, Durable Objects, Workflows, bindings, two-phase Effectful Constructors | [`EFFECT_ALCHEMY.md`](EFFECT_ALCHEMY.md) |

Cloudflare platform placement itself lives in [`CLOUDFLARE_ARCHITECTURE.md`](CLOUDFLARE_ARCHITECTURE.md).

## Cross-cutting defaults

- Compose workflows with `Effect.gen(function* () { ... })` and the project's established `Effect.fn` patterns.
- Recover from the typed error channel at the narrowest boundary with a truthful response; preserve defects and interruption.
- Use native Effect workflows. Isolate unavoidable Promise or platform APIs in their owning Adapter.
- Keep error unions precise at module boundaries. Broad app-level failures belong near orchestration, rendering, logging, and entrypoints.
- Domain operations should not construct production Layers as part of ordinary business behavior. Raw config parsing remains a boundary/composition concern.

## Redacted values

Use Effect's Redacted value type for tokens, credentials, API keys, passwords, and secrets.

Wrap secrets at the boundary and unwrap only inside the adapter that needs the raw value. [`OBSERVABILITY.md`](OBSERVABILITY.md) still owns no-leak behavior and safe summaries.

## Effect RPC

If a codebase already uses Effect RPC, use its schema and transport model consistently for applicable typed RPC seams.

This standard does not require adopting Effect RPC where another established RPC model exists.

## Cloudflare and Effect

For a new Cloudflare project selecting Effect, or an Effect project selecting a new Cloudflare resource/config/deployment model, use Alchemy V2 for that modeling. See [`EFFECT_ALCHEMY.md`](EFFECT_ALCHEMY.md) for the composition rules.

Do not duplicate Alchemy-owned declarations in ad hoc Wrangler configuration, one-off scripts, or parallel infrastructure models unless a documented tooling gap requires small compatibility glue.

## Rejected framings

- **"Effect is present somewhere, so all new code must use Effect."** Only use this file for responsibilities that depend on Effect-specific semantics or established Effect architecture.
- **"Effect lets failures die."** Expected failures stay in the typed error channel.
- **"Any Layer shape is fine."** Follow [`EFFECT_SERVICES.md`](EFFECT_SERVICES.md) and keep resource ownership explicit.
- **"Fast-Check integration is the same in Effect."** Use `@effect/vitest` and Effect's testing exports in Effect 4 projects.
- **"Version-specific examples are universal."** Check installed versions before applying version-specific guidance.

## Review checklist

Every matching branch above has been read, every chosen Effect API has been verified in the pinned package source, every cross-cutting default has been checked against each changed Effect path, and each loaded branch's own completion check passes. Report any exception with concrete evidence.

## Known gaps

This file intentionally does not settle:

- observability integration details beyond spans on `Effect.fn` boundaries;
- Effect RPC adoption criteria;
- transaction integration with Effect;
- native fiber interruption conventions, beyond general cancellation propagation and cancellation classification in [`ASYNC_AND_WORKFLOWS.md`](ASYNC_AND_WORKFLOWS.md).
