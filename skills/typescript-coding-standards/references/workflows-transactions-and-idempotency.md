# TypeScript async work and workflows

Apply [shared work ownership and workflow safety](../../coding-standards/references/workflows-transactions-and-idempotency.md). Effect code uses native scopes/concurrency and [scheduling/retry](effect-scheduling-and-retry.md), not Promise orchestration mixed into core workflows.

Plain TypeScript cancellable interfaces accept a final options object with `signal?: AbortSignal`. Propagate it through fetch, retry, sleep, and adapters. Do not replace it with hidden AbortController lifetimes. For uncancellable dependencies check before/after and document the limitation.

```ts
await users.findActiveByEmail(email, { signal });
// Avoid positional signals or boolean cancellation flags.
await fetch(url, { signal });
```

Collect promises immediately. Known small batches may use `Promise.allSettled`; user/data-sized work uses a shared bounded-concurrency helper with a bottleneck-derived limit. Use `Promise.all` only for an all-or-nothing dependency group; it does not cancel peers. `allSettled` preserves useful successes and per-item classification.

```ts
await mapConcurrentBounded(users, { concurrency: emailProviderConcurrency }, sendEmail);
// Avoid: users.map(sendEmail); void sendEmail(user); // unowned promises
```

Detached work uses a runtime/project owner such as `ctx.waitUntil` or `runDetached`, with rejection handling and observability. Cloudflare/Alchemy durable workflows and two-phase runtime composition follow [Effect Alchemy](effect-alchemy.md).

## When the outcome is unknown

The [shared uncertainty contract](../../coding-standards/references/workflows-transactions-and-idempotency.md#uncertain-outcomes-and-compensation) owns timeout/lost-response semantics and durable compensation evidence. A rejected Promise after a remote mutation does not prove rollback.
