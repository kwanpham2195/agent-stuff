# Go contracts

Apply the [shared workflow](../coding-standards/references/workflow.md) and matching references. Go contracts use named domain values, native `error`, consumer-side interfaces, explicit constructors, and caller-owned `context.Context`, not TypeScript tagged-result syntax.

## Contract chooser

- Named values, constructors, and lifecycle: [domain modeling](DOMAIN_MODELING.md).
- HTTP/RPC/JSON, env, storage, and framework input: [boundaries and parsing](BOUNDARIES_AND_PARSING.md).
- Sentinel/type matching, wrapping, returned error interface, optionality, and defects: [error handling](ERROR_HANDLING.md).
- Narrow interfaces, constructors, and required ADRs: [module design](DESIGNING_MODULES.md).
- Context propagation, goroutine ownership, bounded work, and native transactions: [async work](ASYNC_AND_WORKFLOWS.md).
- Protected secrets, safe fields, and correlated telemetry: [observability](OBSERVABILITY.md).
- Caller-visible tests, native test conventions, and gates: [testing and verification](TESTING_AND_VERIFICATION.md).
- Package names, comments, imports, literals, globals, and native termination: [Go style](GO_STYLE.md).

## Interface example

```go
type CustomerStore interface {
    FindByID(ctx context.Context, id CustomerID) (Customer, error)
}
func NewService(store CustomerStore, clock Clock, log *slog.Logger) *Service
```

The method documents stable categories callers can handle with `errors.Is`/`errors.As`; required absence returns not-found, intentional optionality uses an explicit `(value, ok)` or documented optional result. The adapter parses rows and returns domain values, preserving safe causes deliberately. Each I/O path propagates caller context. An interface earns its place through meaningful translation, variation, or substitution, not merely existence of one implementation.

Complete when every touched contract is checked against its owning addition and shared reference, native error/cancellation semantics remain precise, and verification/constraints are reported under the shared workflow.
