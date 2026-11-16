# Go error handling

Apply [shared expected failures](../coding-standards/references/errors.md), including intentional optional lookup semantics, safe configuration failures, cancellation, and uncertain remote outcomes. Go exposes precise documented categories through native `error`, not a TypeScript Result union.

```go
var ErrMerchantNotFound = errors.New("merchant not found")
type InvalidMerchantIDError struct { /* safe structured context */ }
func (e InvalidMerchantIDError) Error() string { return "invalid merchant id" }
```

Callers classify with `errors.Is`/`errors.As`, never message strings. Context cancellation remains distinct via `context.Canceled`/`context.DeadlineExceeded`. Public functions return the `error` interface as their last result, not a concrete error pointer, to avoid typed-nil interface bugs.

## Wrapping and strings

Use `%w` when underlying errors are intentionally matchable parts of the contract, and `%v` or canonical translation when they are not, especially across system/RPC/storage boundaries. Retaining cause context does not require exposing all dependency categories as public matching contracts.

```go
return fmt.Errorf("load merchant %s: %w", safeID, err)
// %w normally comes last; category sentinel may come first:
return fmt.Errorf("%w: invalid header", ErrParse)
```

Error strings are lowercase with no trailing punctuation. Full displayed logs/API/test messages may be capitalized. Avoid redundant context already provided by the underlying error and meaningless `"failed: %v"` annotations. Stable owning phrases must remain searchable; use safe context only.

Do not use in-band sentinel values for errors. Return `(value, ok bool)` for deliberate optionality or `(value, error)` for failures. Handle `err` before normal flow rather than nesting success in `else`.

## Defects and startup

Expected failures, including missing/invalid external configuration, return `error`. Startup may safely report and terminate. Impossible internal invariants retain Go's termination/panic guidance in [Go style](GO_STYLE.md#panics); do not recover corruption merely to continue.
