# Parsing and evidence

Select parsing from provenance, not a function name or decoder-count target. Preserve owner-provided domain, application, library, and platform types rather than replacing them with broad local approximations.

| Producer evidence | Handling |
| --- | --- |
| Raw body, SQL row, native storage, untyped callback | Parse at its boundary into the strongest meaningful type. |
| Known encoded representation | Preserve its input type and validate contents with a compatible decoder. |
| Already-parsed domain/application value | Pass through with its established type. |
| Computed constrained value or patched state | Establish remaining range, cross-field, and transition invariants at their owner. |

A SQL generic or library declaration describes representation, not runtime integrity. Static field types do not prove cross-field relationships. Do not cast or widen input to force a decoder choice. Identify the producer, established invariants, remaining invariants, and validation removed, retained, or moved for every parsing change. Retyping a decoder preserves validation work; removing a parse is a separate semantic change. Do not encode an established domain value merely to decode it again.

## Boundary ownership

Parse external, serialized, persisted, and framework-shaped input before service/core logic sees it. Return and pass the refined value, not the original validated input. Inner code does not repeatedly shape-check established values unless a new boundary or invariant requires it.

Use separate protocol/persistence representations when fields, naming, encoding, optionality, or semantics differ from application input. Otherwise parse directly into application input. Name symbols for their meaning, such as CreateUserRequest or UserRecord, rather than a generic DTO suffix. Keep each representation and codec private to its boundary; derive representation types from schemas where supported.

```text
Prefer: raw input -> owning parser -> refined application input -> service
Avoid:  decode bytes -> cast to domain value -> service
Avoid:  validate raw input -> discard refined output -> service(raw input)
```

Protocol projections and persistence projections have different owners. Do not reuse an HTTP response as a storage row merely because both serialize. Domain code may expose neutral accessors, deconstruction, and formatting; adapters own consumer-specific projections.

## Parser contracts

Use concrete parsers rather than exporting generic shape guards that spread boundary uncertainty inward. Local object/array checks inside a concrete parser are appropriate. Use local naming conventions that distinguish parsing, smart construction, predicates, assertions, and normalization. Successful parsers return refined values and failures use the language's precise native error contract.

Export a parser only for an intended consumer, with its actual representation-specific input and smallest useful signature. Keep codec-library options private unless deliberately part of a public low-level contract. Prefer the established schema/parser mechanism, or a small handwritten parser when clearer.

Mutating command/request parsers reject unknown fields by default. Allow permissive fields only for deliberately extensible subobjects such as third-party metadata.

## Persistence and runtime hops

Parse every path where less-trusted data re-enters core code, including reads, cache hits, RPC responses, events, workflow replay, and state rehydration, even when this process wrote it. Write-time parsing does not prove stored bytes remain valid. Only a measured performance-critical path with a documented trust invariant may omit read-time parsing; keep unchecked representation inside its boundary.

Values crossing process, RPC, queue, workflow, or serialization boundaries obey the actual transport contract. Do not assume transports preserve class instances, error objects, functions, handles, prototypes, or private state. Encode explicit transport values and reconstruct on receipt, including results and failures.

Unsafe escape hatches require established runtime evidence, a language/tool limitation, focused verification, and a local `SAFETY:` explanation. Keep them at the smallest owner behind precise contracts; convenience or a difficult generic signature is not evidence.

## Completion

Every changed input has known provenance, remaining invariants, an owning parser where required, and a precise failure channel. Established evidence survives transformations; representations remain private; transport contracts are checked; parsing exceptions have measured evidence and containment. Verification distinguishes removed runtime work from type/API substitutions.
