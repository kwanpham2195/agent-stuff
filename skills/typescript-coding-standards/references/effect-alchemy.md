# Alchemy and Effect

Alchemy lets you declare cloud infrastructure and runtime handlers in Effect. Its API is young and changes, so this file records only general design rules. Take exact names from the installed package and its docs.

Related: [services and layers notes](effect-services.md) (layers), [configuration and resources guide](configuration-and-resources.md) (lifetimes), [module and adapter guide](modules-services-and-adapters.md) (where wiring lives).

## Quick review

- Planning succeeds without real storage.
- Back-to-back invocations never reuse a stale handle.
- Deploying, adopting existing resources, or moving data between namespaces has its own explicit approval; passing local tests does not grant it.

## Per-request clients

A client or stub tied to one request cannot be kept in an application-wide layer or cache, even if you can derive a stable key for its target. Create it inside the request. If one request needs the same client repeatedly, memoize for that request only, with a small bounded cache.

## Rules

1. Learn which parts of a definition run at deploy or plan time and which run inside the deployed runtime. The same definition can be evaluated in both.
2. At plan time, declare and resolve references. Do not open connections, run migrations, or start background work, because storage there may be a placeholder.
3. Do those side-effecting steps in the runtime part, before handlers begin serving.
4. Satisfy a capability by providing its existing layer. Do not call the layer's internal construction effect directly; you would skip its sharing and replacement behavior.
5. To pass an already-resolved service into an inner layer, wrap it with `Layer.succeed(Tag, value)`.

```ts
const worker = Effect.gen(function* () {
  const queue = yield* JobQueue;
  return { handle: makeHandler(queue) };
}).pipe(Effect.provide(JobQueueLive));
```
