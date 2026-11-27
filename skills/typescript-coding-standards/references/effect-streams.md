# Working with Stream

A `Stream<A, E, R>` is a lazily evaluated, pull-driven sequence: it can emit any number of `A`, may end in an `E`, and needs `R` to run. If you only need to repeat one action and nothing flows out of it, use a schedule instead (see the [retry and scheduling notes](effect-scheduling-and-retry.md)).

## Quick review

Delivery semantics match the source. Ordering and parallelism are stated. Anything collected is finite. Buffers are bounded. Long-lived consumers have a scope. Failures reach a deliberate handler.

## Failures and per-key work

Convert errors at the edge with `mapError` and recover specific tags with the `catch*` operators. Whole-cause handling is for supervisors. For work where items with the same key must stay in order but different keys can overlap, keep the fiber bookkeeping in a single helper and settle early whether late arrivals queue, replace, or merge.

## Buffers

Default demand-driven flow is usually enough. When producer and consumer must be decoupled, add a buffer and choose its full-behavior on purpose: wait, drop new, or drop old. Leave a buffer unbounded only if something else caps growth. `debounce` waits for a quiet period, `throttle` caps the rate.

## Where the queue stays

A service interface should expose a `Stream`. The `Queue`, `PubSub`, or ref that feeds it is an internal detail, so replacing it never affects callers.

## Consumers that outlive a request

Run them inside a layer, forked into the layer's scope. Building the layer then completes immediately, the consumer keeps working, and releasing the layer stops it.

```ts
export const AuditTrailLive = Layer.scopedDiscard(
  Effect.forkScoped(
    Effect.flatMap(AuditSource, (source) =>
      Stream.runForEach(source.records, writeRecord),
    ),
  ),
);
```

A service method that must start such work later should capture the scope when the layer is built, fork into it, and keep it private.

## Transform, then run

Use `mapEffect` with an explicit `concurrency` for parallel work; permit unordered output only when callers do not care. Prefer `flatMap` to expand elements, `filter` to drop them, and `mapAccum` for state carried along.

Terminal operations are `runForEach`, `runDrain`, and `runFold`. `runCollect` materializes everything, so reserve it for streams you know will finish.

## Start from the producer

- A callback or push source becomes a stream by offering into a `Queue` and reading it back out.
- To let many listeners each see every message, publish through a `PubSub`.
- If late joiners also need the current value, hold it in a `SubscriptionRef` and expose its changes.
- A cursor-paged remote API maps onto `Stream.paginate`, carrying the cursor as state.
- Building a stream needs services? Wrap the effect that makes it with `Stream.unwrap`.
- For small fixed inputs and async iterators the library has direct constructors; look them up in the installed version.

## Testing

Use a finite list for fixtures and append `Stream.never` to imitate an open connection. Push into a queue you own to script events, and `Stream.take` before collecting anything that stays open. For time and concurrency, see the [Effect testing notes](effect-testing.md).
