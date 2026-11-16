# Go concurrency and workflows

Apply [shared cancellation, work ownership, retries, and workflows](../coding-standards/references/workflows-transactions-and-idempotency.md) and [atomic persistence guards](../coding-standards/references/persistence.md).

`context.Context` is the first parameter for I/O, blocking, retrying, and long-running operations. Propagate it downstream; do not replace caller lifetimes with hidden background contexts. Derived dependency timeouts still compose with the caller. Call the returned cancel function when ownership requires it.

```go
func (s *Service) Find(ctx context.Context, id MerchantID) (Merchant, error) {
    return s.store.FindByID(ctx, id)
}
// Avoid context.Background() here, which drops caller cancellation.
```

Own goroutines with an explicit lifecycle: context, errgroup/wait group, bounded pool, error/rejection path, and observability. Use `errgroup.Group` or the repository's bounded worker helper. User/database/file/queue-sized inputs must not launch unbounded goroutines. A wait group alone does not define cancellation or error policy.

```text
Prefer: bounded worker pool -> propagate context -> join -> classify failures
Avoid: launch one unowned goroutine per row and return
```

Use native transaction ownership and persisted inbox/outbox, guards, or stable identity for retry-safe mutations. Shared workflow selection, lost-response uncertainty, durable progress, and compensation rules apply directly; do not translate them into Promise/AbortSignal or Cloudflare-specific machinery.
