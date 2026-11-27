# Go domain modeling

Apply [shared domain values and state](../coding-standards/references/domain-types-and-state.md). Use defined Go types for IDs, units, and constrained values; constructors/parsers establish invariants before values enter services.

```go
type CustomerID string

func ParseCustomerID(raw string) (CustomerID, error) {
    if raw == "" { return "", ErrInvalidCustomerID }
    return CustomerID(raw), nil
}
// Avoid using bare string for interchangeable customer/user IDs.
// Avoid converting unparsed input directly to CustomerID at call sites.
```

Go defined types alone do not prevent explicit conversion or invalid zero values. Keep construction disciplined at package boundaries and test invariants; do not claim compile-time impossibility the language does not provide.

Use state-specific structs or a state tag with transition functions that own legal transitions. Go does not supply TypeScript closed unions; express legal state coverage with precise native contracts and tests. Persisted contradictory state is rejected by the storage parser and protected by constraints/guarded writes where practical.

Keep value behavior pure and mutation private behind the package contract. Prefer operation-specific structs over broad entity/optional-field bags. For meaningful architectural decisions follow [Go module rationale](DESIGNING_MODULES.md) and the repository glossary.
