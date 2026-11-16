# Expected failures and defects

Represent known normal-operation failures in explicit native error channels or documented, distinguishable error contracts. Use precise failure categories callers can handle semantically, not a universal application error or unstructured message. This includes domain rejection, parsing, authorization, dependencies, I/O, persistence, configuration, workflows, and cancellation. Do not prescribe one language's union syntax or result library to another language.

A caller handles a failure or returns it upward. The outer boundary translates it into a valid HTTP response, CLI exit, retry, dead letter, or safe startup diagnostic. Keep exception-style framework contracts at their owner rather than leaking them inward. Preserve the required public contract and expose expected variants through its established mechanism.

```text
Prefer: required user lookup returns User or distinguishable NotFound/StoreUnavailable
Avoid:  ordinary absence hidden as a generic crash or unexplained empty value
Prefer: optional lookup explicitly returns absence or StoreUnavailable
```

## Defects

Defects make correct execution impossible: violated internal invariants, impossible branches, temporary unimplemented paths, or catastrophic runtime conditions. Use the established native defect mechanism. Lack of a caller recovery strategy does not turn a known failure into a defect.

Missing/invalid external configuration is an expected failure. The composition root may terminate startup after a safe diagnostic. An impossible internal startup invariant is a defect.

## Error ownership and translation

Errors have stable machine-matchable categories and useful safe context. Keep failure modes distinct unless callers handle them identically, observability is identical, and structured fields preserve useful distinctions. Native mechanisms may expose matching categories rather than statically enumerating an error union.

The error owner constructs a useful, searchable message explaining what failed and actionable recovery when known. Start with a stable literal phrase leading to its definition, then append safe context. Classification uses categories and fields, never message matching. Retain the original cause where useful without exposing unsafe contents.

Broad application-error aggregation belongs near orchestration, entrypoints, logging, and rendering; module contracts remain precise. Required lookup absence is a not-found failure; intentional optional lookup may return absence. Make the difference clear in the operation's contract/name.

Translate at the owner that knows the protocol or recovery policy. Pass already-correct failures unchanged and map each source category by its actual meaning. A generic mapper is appropriate only when the entire source channel intentionally has one meaning and preserves safe context and precise contracts. Classify cancellation before wrapping dependency failures. Defects and interruption stay distinct; cause-level recovery belongs to explicit supervision.

A lost mutation response means uncertainty, not proven failure. Apply [workflow safety](workflows-transactions-and-idempotency.md#uncertain-outcomes-and-compensation).

## Completion

Each known failure has a distinguishable contract or explicit defect classification. Absence has intentional semantics; errors retain safe context and stable matching; outer boundaries render valid outcomes; cancellation, defects, and uncertain remote outcomes stay distinct. Report required incompatible contracts rather than initiating a migration.
