# TypeScript type safety

## Checklist

- Code compiles under the project's strict settings.
- Mutation is contained, and type information survives each changed boundary and helper.
- Exported surfaces have explicit return types, with named types only where justified.
- Every cast other than `as const`, and every `any`, has runtime evidence, a stated compiler limit, focused verification, and a safety comment.
- No widen-and-cast chain or newly added `!` remains.

## Immutability first

```ts
type NewOrder = {
  readonly customerId: CustomerId;
  readonly items: ReadonlyArray<OrderItem>;
};
```

Default to values that cannot change. Mutation is acceptable inside a small area such as an imperative shell, a hot loop, a builder, or an adapter, as long as callers only see a precise interface.

## Casts, `any`, and `!`

The shared guidance on unsafe escapes sets the bar. When unsure, narrow with a branch, parse the data, or give the function a better signature. Never widen a value and cast it back, including via `unknown` or `any`.

`as const` needs no comment. Every other cast carries a note stating the runtime fact that makes it safe and the compiler limit that forces it:

```ts
// SAFETY: the compiler cannot see the brand. parseSku validated the string
// just above, and it is the only code that produces a Sku.
return value as Sku;
```

A truly unavoidable `any` meets the same bar, has a specific justification, and includes any lint suppression the repository requires. Prefer a type exported by the owning module or a generic signature. A stricter repository lint rule overrides broader shared permission. For optional values, narrow so the required value is present rather than asserting with `!`.

## Keep the type information you have

See [shared guidance on keeping evidence](../../coding-standards/references/parsing-and-evidence.md). Before making up a local stand-in type, look for the real schema, public type, constructor, or generic parameter. Reserve `unknown` for cases where the representation really is uncertain.

`satisfies` and explicit return annotations verify an already-built value without widening it. Both are compile-time only, so any remaining runtime requirement follows the [provenance guidance](parsing-and-schemas.md#provenance). Helpers you extract should preserve the exact success, error, and requirement types.

## Explicit return types

Annotate the return type of methods on exported interfaces, public class methods, and exported functions that return an object, union, or collection. A short one goes inline. Introduce a named exported type when the name adds domain meaning or several declarations share it, and derive it from the runtime schema if one exists rather than writing both. Private helpers and local callbacks may rely on inference when it keeps the full contract.

## Compiler flags

For a new or edited `tsconfig`, enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, and `noFallthroughCasesInSwitch`. An older project that cannot adopt one yet should limit the exemption to that config and record the errors blocking it and where the migration stops.
