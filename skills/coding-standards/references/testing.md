# Testing and verification

Tests prove observable behavior through interfaces callers use, not private helpers or incidental call order. A test must fail when its claimed behavior is absent.

Match evidence to changed invariants, failures, boundaries, async behavior, persistence/runtime assumptions, and user-visible consequences. Focused changes verify behavior through the owning interface; elevated changes also exercise affected external, persistence, concurrency, or runtime seams. Critical flows verify the end-to-end path when a representative environment exists. Language additions may require broader coverage.

Prefer the highest-confidence proof that remains proportionate: end-to-end tests, integration through real interfaces, focused/property tests for pure domain behavior, or unit tests for meaningful behavior. Exercise important failures at the closest reliable real interface. Report concrete blockers from unavailable environments, unreliable third parties, or unreasonable setup/runtime/cost. Do not demand tests merely because lines changed.

## Real seams

Do not patch/mock modules. Replace behavior through intentional production seams: injected dependencies, managed services, real local databases, faithful in-memory implementations, or fake external adapters. Prefer recording implementations for observable interactions; language additions govern any narrow spy allowance/prohibition.

```text
Prefer: request reset -> returned queued result and recorded email through injected adapter
Avoid:  patch imported send function -> assert its private call count
```

Assert values/failures, persisted state, emitted messages, rendered responses, or public recording-adapter records. Control time, randomness, IDs, external dependencies, and cancellation when they affect deterministic claims. Avoid sleep-based synchronization, assertion-free execution, retries hiding flakiness, unstable snapshots, and mutable shared fixtures.

## Properties and fixtures

Assess property tests for each changed invariant, transition, normalization, equivalence, ordering, idempotence, or roundtrip. Add them when generated inputs meaningfully exceed short example lists. Keep reusable generators with their domain owner, sharing entrypoints only for multiple consumers.

Valid domain fixtures use production parsers/constructors. Invalid boundary fixtures independently construct corrupt input before entering the real boundary; deriving them from the schema under test can erase the defect when that schema weakens. Property callbacks must actually fail on counterexamples.

## Persistence, parsing, and recovery

Test owned transformations, cross-field filters, source precedence, representation selection, and public failure behavior, not a library's ordinary mechanics. Include accepted/rejected parser cases, positive current/legacy cases, and malformed/hybrid evidence where applicable. Rejected stored authority stays intact; migration/state writes do not partially commit.

Use representative local databases with real migrations when correctness depends on queries, schema, constraints, serialization, or transactions. A handwritten fake proves the capability contract, not SQL/driver behavior. Runtime-specific claims require the actual representative runtime, not a different runtime with matching APIs.

When removing a read/parse/checkpoint, verify its distinct invariant and observable work through the owner. A deliberate regression probe may establish that a test fails when the refinement/source-precedence check disappears. Database reconstruction, native restart, and deployed recovery establish different claims. Name unproven claims when representative environments are unavailable.

## Test implementations and public contracts

A dependency interface reflects real ownership/variation, not merely a desire to mock. Keep one-off fakes local; share reusable implementations only when their complete behavior is useful. Names such as RecordingEmailSender, FailingEmailSender, or InMemoryCache must describe the full tested contract. Production branches/exports/flags stay determined by production needs; use existing public interfaces or faithful inert harnesses.

When public typing/inference is behavior, test ordinary accepted and rejected call sites without rescue annotations/casts. Assert the entire contract: input, arity/options, success, failures, and dependency requirements where supported. Parameter-only checks can miss widened result/error channels.

## Completion

Each material behavior and failure has proportionate evidence through the highest reliable real interface or a concrete blocker. Properties were assessed; fixtures preserve/challenge appropriate invariants; runtime/database claims match the environments exercised; tests avoid module patching and implementation coupling; public contracts and complete reusable test behavior are verified.
