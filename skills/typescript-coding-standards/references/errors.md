# TypeScript errors

Follow the [shared rules on failures and defects](../../coding-standards/references/errors.md). Every expected failure must appear in the return type as a custom tagged error, even if the immediate caller cannot do anything about it.

## Defining errors

Extend `Error`, extend `better-result`'s `TaggedError`, or use the [schema-based error class](effect-schema-and-data.md#errors) from Effect. Give each class a stable `as const` tag, safe structured fields, a helpful fixed message, and an optional `cause: unknown`.

```ts
export class PaymentGatewayDown extends Error {
  readonly _tag = "PaymentGatewayDown" as const;
  constructor(
    readonly step: "authorize" | "capture",
    readonly cause: unknown,
  ) {
    super(`Payment gateway unavailable during ${step}`);
  }
}
```

A lookup that must succeed returns a not-found error. A lookup where absence is normal may return `T | undefined` or Effect's `Option`. Describe each operation's failures precisely; avoid a catch-all `AppError`.

## Choosing a mechanism

- In an Effect project use the typed error channel.
- Elsewhere use `better-result` if it is already present or accepted for the task; otherwise reuse whatever result type exists, or a small local tagged union. Do not add a dependency for taste.
- Outside Effect, `better-result`'s `TaggedError` is a good base class for expected errors even if you do not use its `Result`.

```ts
type Outcome<A, E extends Error> =
  | { readonly ok: true; readonly value: A }
  | { readonly ok: false; readonly error: E };

// Do this:
declare function loadOrder(id: OrderId): Promise<Outcome<Order, OrderMissing | OrderStoreDown>>;
// Not this: a Promise<Order> that rejects for a missing order or a dead database
```

A rejected promise is a thrown error. The code that directly calls a third-party API must catch the unknown rejection and classify it before it leaves the module, checking for cancellation first. Where a framework requires throwing, do that only at the framework edge and still make the public expected variants distinguishable.

## Defects

Reuse the project's existing helpers for impossible states if they have enough use to justify themselves; otherwise keep the code local or native:

```ts
casesHandled(value: never): never;
shouldNeverHappen(message?: string): never;
notYetImplemented(message?: string): never;
```

Known configuration problems remain typed until startup can report them safely and stop.

## Boundary translation

With tagged Effect unions, prefer `Effect.catchTag` or `catchTags`: they keep each category's policy explicit and leave unrelated errors alone, and any new tag shows up in inference. Use `mapError` or a shared mapper only when every member of the incoming error type should mean the same thing, and keep the concrete error and requirement types. Defects, interruption, and cause-level handling follow the shared rules.
