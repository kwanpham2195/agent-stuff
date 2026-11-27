# Caches and batching

Before writing a `Map` with expiry timestamps or a table of in-flight promises, check whether the library already covers the need.

## Choosing

| Need | Tool |
| --- | --- |
| One value, computed once | `Effect.cached` |
| One value that should go stale | `Effect.cachedWithTTL` |
| Many keys loaded lazily | `Cache` |
| Entries that must be closed when evicted | `ScopedCache` |
| Backend answers several keys per call | `Effect.request` with a resolver |
| One backend call per key | `Effect.forEach` with a concurrency limit |

## Quick review

- Does the tool fit how keys arrive and what the backend can do?
- Does each cache state a size limit, an entry lifetime, and how entries are invalidated?
- Was each cache created once, by the layer or scope that owns it?

## Batching

A request resolver collects requests made at about the same time and sends them as one backend call. Limit the batch size with the library's helper, and split by destination when requests go to different places. A backend with no multi-key endpoint gains nothing from a resolver; bound the parallelism of single calls instead.

## Never share request-bound values

A handle that is only valid during one request must not sit in a process-wide cache, however stable its key looks. See [per-request clients](effect-alchemy.md#per-request-clients).

## The keyed cache

- Making one is itself an effect. Do it in the owner's layer and hand out the handle.
- Concurrent readers of an absent key share one load, so a separate deduplication table is redundant.
- The size limit is required and is effectively the memory budget. Choose it deliberately.
- Remove stale entries with `invalidate`; reload with `refresh`.
- Lifetimes can be computed from the load outcome. Failed or degraded results should expire immediately so the next caller retries. A short lifetime for "not found" protects the backend from repeated misses.

```ts
const program = Effect.gen(function* () {
  const profiles = yield* Cache.make({
    capacity: 200,
    timeToLive: "10 minutes",
    lookup: (id: UserId) => loadProfile(id),
  });
  return yield* profiles.get(userId);
});
```

Signatures vary by release, including the variant that takes a lifetime function; check the installed one.
