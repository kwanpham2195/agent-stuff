# Models and decoding with Schema

Use `Schema` to describe data, derive types from it, and decode untrusted input. Function names here are the common ones; verify them in the installed release because constructors are renamed from time to time.

## Define once, derive the type

```ts
export const Invoice = Schema.Struct({
  id: InvoiceId,
  customer: Schema.NonEmptyString,
  note: Schema.optional(Schema.String),
});
export type Invoice = typeof Invoice.Type;
```

- Add `identifier` annotations only if some tool reads them (API docs, JSON Schema).
- To build a new value with its rules checked, use the schema's constructor; choose the failing-in-Effect form when callers should handle the failure.
- Whether data must be checked at all depends on its origin: [parsing guide](parsing-and-schemas.md#provenance).

## Errors

See [error guide](errors.md) for what errors mean and how to translate them. Schema-based tagged error classes are the accepted class form for typed Effect failures:

```ts
export class LedgerWriteError extends Schema.TaggedError<LedgerWriteError>()(
  "LedgerWriteError",
  { operation: Schema.String, cause: Schema.Defect },
) {}
```

Use a union of such classes for errors that cross an API. A defect schema transports the cause but does not redact it, so keep raw causes internal and apply [sensitive-data guide](sensitive-data-and-observability.md) before logging or returning them.

## Unions

```ts
// internal state machine, never serialized
type Job = Data.TaggedEnum<{
  Queued: { readonly at: number };
  Done: { readonly output: string };
}>;
const Job = Data.taggedEnum<Job>();

// decoded or persisted
const Created = Schema.TaggedStruct("Created", { id: InvoiceId });
const Voided = Schema.TaggedStruct("Voided", { id: InvoiceId, reason: Schema.String });
const InvoiceEvent = Schema.Union(Created, Voided);
```

`Data.TaggedEnum` is for in-process states: it provides constructors, guards, and exhaustive matching. Anything decoded, encoded, stored, or documented as JSON Schema should be a schema union. If an outside format discriminates on another field, model it as a literal on each member.

## Brands

Apply constraints, then `Schema.brand`. If the codebase already has `Brand` constructors, adapt those.

## Missing, undefined, null

Decide the meaning first ([domain types guide](domain-types-and-state.md)). Then:

- A key that can be absent: optional key.
- An explicit `undefined`: only if the contract says so.
- `null`: only if the external format uses it.
- Defaults: keep a required field in the normalized type and fill it during decoding.

## Reusing parts

Build related schemas from shared fields (`Invoice.fields.customer`) and use the library's extension and key-renaming helpers when the relationship is real. When translation involves logic, joins, or validation, write a plain mapping function.

## Pick the decoder by the input you hold

| You hold | Use |
| --- | --- |
| Data from outside (HTTP body, parsed JSON, storage) | an `unknown`-input decoder |
| A value already typed as the schema's encoded side | the typed-input decoder |
| JSON text | a schema that parses the string, then decodes |

Do not cast something to the encoded type just to reach the typed decoder; a general `string` is not a literal union. Use the synchronous variants only where throwing is fine (scripts, tests, startup). Option-returning variants drop the reason for failure.

Keep unknown-input decoders private to the adapter that receives the data, and export a small named parser instead of the raw decoder, whose parse-options argument would leak into callers:

```ts
const decodeRaw = Schema.decodeUnknown(OrderRequest);
// inside the adapter
const request = yield* decodeRaw(rawBody);
```

```ts
const decodeCountry = Schema.decode(CountryCode);

/** Validate a country code string. */
export const parseCountryCode = (code: string) => decodeCountry(code);
```

Rules that span fields (such as a start before an end) must still be checked at runtime; `satisfies` and field types do not prove them.

## Quick review

Do models derive from one schema? Are optional and null states deliberate? Does each decoder fit its input? Do public parsers hide parse options? Are cross-field rules enforced at runtime? Do serialized errors follow [error guide](errors.md)?
