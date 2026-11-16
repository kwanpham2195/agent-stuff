# Persistence

Define persistence boundaries around cohesive domain capabilities, not tables. Keep table layout, queries, schema, raw records, and ORM mechanics private. Stored rows and cache hits follow [parsing and evidence](parsing-and-evidence.md); transactions/retries follow [workflow safety](workflows-transactions-and-idempotency.md).

## Representation authority

Select a codec from storage source, explicit version, or discriminator evidence before decoding. Current storage uses the current contract; identified legacy storage uses its explicit compatibility translation. Malformed data fails under the selected representation rather than falling through to a weaker schema that drops recovery fields.

```text
Prefer: version evidence -> selected decoder -> reject malformed authority unchanged
Avoid:  current decoder fails -> permissive legacy decoder -> discard recovery fields
```

Keep original invalid authority available for safe diagnosis. Migration/import commits only after all required validation succeeds, with no partial writes. Translated field types may still require cross-field/state-transition refinement before receipts/checkpoints become valid evidence. Preserve durable identity, intent, and compensation evidence under workflow rules.

Use storage constraints and atomic guarded writes where practical to enforce persisted invariants. A read followed by unconditional write is not a concurrency guard. Preserve original transition metadata on retries. Derive claimed delete results from the atomic delete, not stale pre-reads; make idempotent deletion semantics explicit.

Exercise valid imports and corrupt/hybrid evidence through the real storage interface. Service reconstruction over the same database proves persistence behavior, not native eviction, alarm recovery, or production adoption. Follow [testing](testing.md) for representative database/runtime evidence.

## Completion

Each operation has a cohesive owner; representations remain private; read-time parsing and representation selection preserve authority; rejected imports do not partially commit; refinements, constraints, and guarded writes protect persisted invariants; evidence claims match the actual runtime exercised.
