# Go Contracts

Go should make dependencies, failure modes, cancellation, and ownership obvious at package boundaries. Prefer small packages, explicit constructors, narrow interfaces, typed domain values, boring errors, and tests through real seams.

## Vocabulary

**Domain Package** — A package centered on one domain concept or tightly related type family. It exposes named types, constructors/parsers, predicates, transitions, formatting helpers, and neutral projections. It avoids I/O and hidden process state.

**Service Package** — A dependency-bearing package that coordinates a cohesive use case. It accepts parsed domain/service values, calls dependency interfaces, owns use-case policy, classifies dependency failures, and returns typed results plus `error`.

**Adapter Package** — A package at an external boundary: HTTP/RPC handlers, persistence, queue consumers, platform bindings, SDK clients, or third-party services. It parses inbound data, projects outbound data, and implements service-facing interfaces.

**Named Domain Type** — A Go `type` that distinguishes a semantic value from its primitive representation, created by a parser or constructor: `type MerchantID string`.

**Typed Error Match** — An error contract callers can handle with `errors.Is` or `errors.As`: sentinel errors for stable categories, concrete error types for structured context, and `%w` wrapping to preserve causes.

## Non-negotiables

- `context.Context` is the first parameter on I/O, blocking, retrying, or long-running operations, and is propagated downstream.
- Boundary packages parse HTTP bodies, queue payloads, env/config, third-party responses, and database rows before service/domain logic sees them.
- Service and domain packages do not accept raw `http.Request`, ORM rows, framework contexts, env maps, SDK clients, or unparsed JSON.
- Expected failures return `error`; panics are for unrecoverable defects only.
- Errors keep stable matching behavior with `errors.Is`/`errors.As`; wrapping uses `%w`.
- Package-level mutable state is avoided unless it is immutable configuration, an explicitly synchronized cache, or a documented singleton at composition.
- Goroutines are owned by an explicit lifecycle: context, errgroup/wait group, bounded worker pool, rejection/error path, and observability.
- Tests exercise package or adapter seams callers use; avoid monkey-patching globals, sleep-based timing, and mocks that only assert implementation calls.

## Domain values

Use named types for semantic primitives:

```go
type MerchantID string

func ParseMerchantID(raw string) (MerchantID, error) {
	if raw == "" {
		return "", ErrInvalidMerchantID
	}
	return MerchantID(raw), nil
}
```

Do not pass bare strings when multiple IDs or codes can be mixed up.

For lifecycle state, avoid optional-field bags. Prefer state-specific structs or a single state tag with transition functions that own legal transitions. If the persisted representation can be contradictory, parse it at the storage boundary and reject impossible rows.

## Boundaries

Keep DTOs at adapters:

```go
type createMerchantRequest struct {
	MerchantID string `json:"merchant_id"`
}

func (h *Handler) CreateMerchant(w http.ResponseWriter, r *http.Request) {
	var req createMerchantRequest
	// decode, parse, call service with domain values
}
```

Repository rows are boundary data too. Convert rows into domain/service values before returning them from the adapter. Do not let service packages depend on ORM-generated row types unless the repository package is itself the service boundary.

## Errors

Use errors callers can handle:

```go
var ErrMerchantNotFound = errors.New("merchant not found")

type InvalidMerchantIDError struct {
	Value string
}

func (e InvalidMerchantIDError) Error() string { return "invalid merchant id" }
```

Wrap causes with operation context:

```go
return fmt.Errorf("load merchant %s: %w", id, err)
```

Do not match on error strings. Avoid logging raw request bodies, credentials, tokens, or arbitrary serialized structs inside errors.

### Wrapping: `%v` vs `%w`

`%v` for annotation where the caller doesn't need to unwrap (boundary translation, logging, fresh errors). `%w` when the caller should be able to `errors.Is`/`errors.As` the underlying error (documented contract, internal helpers). At system boundaries (RPC, storage), prefer `%v` or canonical error translation over `%w`.

### `%w` placement

Place `%w` at the end so the error text mirrors the chain (newest to oldest):

```go
return fmt.Errorf("load merchant %s: %w", id, err)
```

Exception: sentinel/category errors at the beginning so the category is immediately visible:

```go
return fmt.Errorf("%w: invalid header", ErrParse)
```

### Error strings

Lowercase, no trailing punctuation (`"merchant not found"`, not `"Merchant not found."`). Full displayed messages (logs, test failures, API responses) are typically capitalized.

### Adding information

Don't add redundant info the underlying error already provides (`"launch codes unavailable: %v"`, not `"could not open settings.txt: %v"` — `os.Open` already includes the path). Don't add annotations whose sole purpose is to indicate failure (`fmt.Errorf("failed: %v", err)` — just return `err`).

### In-band errors

Don't return sentinel values (-1, nil, "") for errors. Return `(value, ok bool)` or `(value, error)`. This prevents `Parse(Lookup(missingKey))` bugs.

### Indent error flow

Handle errors before proceeding; don't wrap normal code in `else`:

```go
// Good
if err != nil {
    return err
}
doWork()

// Bad
if err != nil {
    return err
} else {
    doWork()
}
```

### Exported functions return `error` interface

Not concrete error types. A concrete `nil` pointer wrapped in an interface becomes non-nil. Return `error` as the last result parameter.

## Interfaces and dependencies

Define small interfaces where the consumer needs variation:

```go
type MerchantStore interface {
	FindByID(ctx context.Context, id MerchantID) (Merchant, error)
}
```

Prefer constructors with explicit dependencies:

```go
func NewService(store MerchantStore, clock Clock, log *slog.Logger) *Service
```

Avoid package globals for time, randomness, loggers, clients, and configuration. If a package-level variable exists for compatibility, isolate it at the composition seam.

### Avoid unnecessary interfaces

Don't create an interface before a real need exists (behavior varies, boundary translates, test substitutes). A single implementation doesn't justify an interface.

### Don't export interfaces unnecessarily

If only used internally, keep it unexported. Consumer-side interfaces stay near the consumer.

### Small interfaces

The larger the interface, the harder to implement and use. Prefer 1-3 method interfaces. Compose small interfaces into larger ones when needed.

## Async and transactions

Use `errgroup.Group` or a project-standard bounded worker helper for concurrent work. Unbounded goroutines over user, database, file, or queue-sized inputs are not acceptable.

Do not hold database transactions open across network calls or long-running work. For retryable mutating operations, use idempotency keys, unique constraints, guarded state transitions, inbox/outbox records, or equivalent persisted deduplication.

## Tests

Prefer:

- table tests for pure domain behavior;
- `httptest` for HTTP adapter behavior;
- temp dirs/files for filesystem boundaries;
- real parser/codec tests for DTOs and rows;
- focused integration tests for persistence behavior that SQL or driver semantics can change.

Avoid tests that only prove a mock method was called. A good test observes returned values, persisted state, emitted messages, HTTP responses, or stable logs/metrics through the same seam callers use.

### `t.Error` vs `t.Fatal`

`t.Error` keeps going (preferred for most checks); `t.Fatal` stops the test (use in setup helpers or when further checks are meaningless after failure).

### Don't call `t.Fatal` from goroutines

`t.FailNow`/`t.Fatal` must be called from the test goroutine, not from spawned goroutines. Use a channel or `errgroup` to propagate the error back.

### Use field names in test struct literals

```go
tests := []struct {
    input string
    want  []string
}{
    {input: "x", want: []string{"x"}},  // good: field names
}
```

### Keep setup scoped

Scope setup to specific tests where possible; avoid global `TestMain` setup when per-test setup suffices.

### Use real transports

For integration tests, prefer real HTTP/RPC transports over mocked transports.

### Assertion style

Use `t.Errorf("Func(%v) = %v, want %v", input, got, want)` with got-before-want. Avoid third-party assertion libraries. Use `go-cmp/cmp` (`cmp.Equal`, `cmp.Diff`) for struct comparisons, not hand-coded field-by-field checks.

### Identify function and input

Failure messages should include the function name and inputs, even when "obvious" from the test name.

## Toolchain

Use the repository's established gate first. If absent, default to:

```bash
gofmt
go test ./...
go vet ./...
```

Run `golangci-lint` when the repo already uses it. Do not add a new lint stack just to enforce these standards unless the user asks.

## Rejected framings

- **"It's typed because it is a struct."** DTOs and rows can still violate domain invariants.
- **"The interface should live with the implementation."** Put small behavior-shaped interfaces near the consumer unless repo convention says otherwise.
- **"A goroutine is fire-and-forget."** Background work needs ownership, cancellation, error handling, and observability.
- **"We can inspect the error string."** Stable matching goes through `errors.Is` or `errors.As`.
- **"A table test with mocks proves it."** Tests should prove observable behavior through the relevant seam.
