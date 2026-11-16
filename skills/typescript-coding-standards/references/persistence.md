# TypeScript persistence

Apply [shared persistence](../../coding-standards/references/persistence.md), [parsing](parsing-and-schemas.md), and [testing](testing.md). Keep ORM-generated rows inside the owning adapter; inferred row types are representation evidence, not domain proof.

```ts
type InvoiceRow = typeof invoices.$inferSelect;
function parseInvoiceRow(row: InvoiceRow): Result<Invoice, InvalidStoredInvoice> {
  // reconstruct domain values and reject contradictory states
}
// Avoid passing InvoiceRow directly as Invoice or service input.
```

Use schema-inferred row/insert/update DTOs where supported and named storage projections, such as `UserStorage.toRow(user)`, distinct from `UserHttp.toPublicJson(user)`. Effect codecs follow [schema/data](effect-schema-and-data.md); cache mechanisms follow [Effect caching](effect-caching.md). Runtime-backed Durable Object/Alchemy ownership follows [Effect Alchemy](effect-alchemy.md). Database reconstruction is not proof of native eviction/alarm recovery.
