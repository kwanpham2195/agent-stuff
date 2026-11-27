# TypeScript domain types and state

Apply the [shared domain policy](../../coding-standards/references/domain-types-and-state.md).

## Branded and refined types

Give brands or refined types to domain identifiers, quantities that could be mixed up (such as units), and constrained scalars. When the owning schema library can brand or refine, let it do so rather than casting by hand. Ordinary display text and plain counters stay primitive.

```ts
function parseOrderId(input: string): Result<OrderId, InvalidOrderId> {
  if (!looksLikeOrderId(input)) return err(new InvalidOrderId(input));
  // SAFETY: the check above establishes the invariant the brand stands for.
  return ok(input as OrderId);
}
// Never: const id = request.orderId as OrderId;
```

## Inputs and options

`Partial<T>` expresses real partiality in the domain, not a shortcut for command arguments. Keep the primary input positional and add a named options object for deliberate policy knobs, for example `placeOrder(draft, { notify: false })`. Boolean predicates such as `isOverdue(invoice)` are fine.

## Variants

Prefer string-literal or discriminated unions over TypeScript `enum`s; numeric enums are only for external interoperability. Use `_tag` as the discriminant unless another field is already domain vocabulary. Model lifecycle stages as separate variants, so impossible combinations cannot be represented:

```ts
type Shipment =
  | { readonly _tag: "Pending"; readonly id: ShipmentId; readonly parcels: NonEmptyArray<Parcel> }
  | { readonly _tag: "InTransit"; readonly id: ShipmentId; readonly departedAt: Instant }
  | { readonly _tag: "Delivered"; readonly id: ShipmentId; readonly deliveredAt: Instant };
// Not: { inTransit: boolean; delivered: boolean; departedAt?: Date; deliveredAt?: Date }
function markDelivered(shipment: InTransitShipment, at: Instant): DeliveredShipment;
```

Use `switch` for three or more closed variants, finishing with the `never` helper described in the [error guide](errors.md) so a new variant is a compile error and is not swallowed by `default`. Open external protocols need the shared, tested fallback policy instead. Within Effect, `Option` may represent deliberate absence.

## Value classes

An immutable value class has a private constructor, is created through parsers or smart constructors, and contains only pure behavior on the value. It must not reserve rows in a database or hide dependencies.
